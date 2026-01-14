"""
Narration Studio - Batch TTS with Multi-Voice Support
A Gradio application for narrating scripts with Zonos voice cloning.
"""

import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import Literal

import gradio as gr
import numpy as np
import soundfile as sf
import torch
import torchaudio

from zonos.conditioning import make_cond_dict, supported_language_codes
from zonos.model import DEFAULT_BACKBONE_CLS as ZonosBackbone
from zonos.model import Zonos
from zonos.utils import DEFAULT_DEVICE as device

# =============================================================================
# Global State (Model Caching)
# =============================================================================

CURRENT_MODEL_TYPE = None
CURRENT_MODEL = None


def load_model_if_needed(model_choice: str):
    """Load model if not already loaded or if different model requested."""
    global CURRENT_MODEL_TYPE, CURRENT_MODEL
    if CURRENT_MODEL_TYPE != model_choice:
        if CURRENT_MODEL is not None:
            del CURRENT_MODEL
            torch.cuda.empty_cache()
        print(f"Loading {model_choice} model...")
        CURRENT_MODEL = Zonos.from_pretrained(model_choice, device=device)
        CURRENT_MODEL.requires_grad_(False).eval()
        CURRENT_MODEL_TYPE = model_choice
        print(f"{model_choice} model loaded successfully!")
    return CURRENT_MODEL


# =============================================================================
# Data Structures
# =============================================================================


@dataclass
class VoiceProfile:
    """Represents a loaded voice sample with its speaker embedding."""
    name: str
    audio_path: str
    embedding: torch.Tensor = None


@dataclass
class SentenceItem:
    """Represents a single sentence in the narration."""
    index: int
    text: str
    voice_name: str = None
    audio_data: np.ndarray = None
    sample_rate: int = 44100
    status: Literal["pending", "generating", "done", "error"] = "pending"


@dataclass
class NarrationSession:
    """Main session state containing all narration data."""
    sentences: list = field(default_factory=list)
    voices: dict = field(default_factory=dict)
    default_voice: str = None

    def to_dataframe(self):
        """Convert sentences to DataFrame format for Gradio."""
        rows = []
        for s in self.sentences:
            text_preview = s.text[:60] + "..." if len(s.text) > 60 else s.text
            voice = s.voice_name if s.voice_name else "(default)"
            rows.append([s.index + 1, text_preview, voice, s.status])
        return rows

    def get_voice_names(self):
        """Get list of available voice names."""
        return list(self.voices.keys())


def create_empty_session():
    """Create a new empty session dictionary."""
    return {"session": NarrationSession()}


# =============================================================================
# Script Processing
# =============================================================================


def split_script_to_sentences(text: str) -> list:
    """
    Split text into sentences for TTS.
    Handles standard punctuation while preserving common abbreviations.
    """
    if not text or not text.strip():
        return []

    # Normalize whitespace
    text = " ".join(text.split())

    # Common abbreviations to protect
    abbreviations = [
        "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "Sr.", "Jr.",
        "vs.", "etc.", "i.e.", "e.g.", "a.m.", "p.m.",
        "St.", "Ave.", "Blvd.", "Rd.",
    ]

    # Replace abbreviations with placeholders
    placeholders = {}
    for i, abbr in enumerate(abbreviations):
        placeholder = f"__ABBR{i}__"
        placeholders[placeholder] = abbr
        text = text.replace(abbr, placeholder)

    # Split on sentence-ending punctuation followed by space and capital
    # Also split on punctuation at end of string
    pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])$'
    sentences = re.split(pattern, text)

    # Restore abbreviations and clean up
    result = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        # Restore abbreviations
        for placeholder, abbr in placeholders.items():
            s = s.replace(placeholder, abbr)
        result.append(s)

    return result


# =============================================================================
# Voice Management
# =============================================================================


def compute_speaker_embedding(audio_path: str, model) -> torch.Tensor:
    """Compute speaker embedding from audio file."""
    wav_data, sr = sf.read(audio_path)
    wav = torch.from_numpy(wav_data).float()
    if wav.dim() == 1:
        wav = wav.unsqueeze(0)
    elif wav.dim() == 2:
        wav = wav.T  # soundfile uses (frames, channels), we need (channels, frames)
    embedding = model.make_speaker_embedding(wav, sr)
    embedding = embedding.to(device, dtype=torch.bfloat16)
    return embedding


# =============================================================================
# Audio Generation
# =============================================================================


def generate_single_sentence(
    text: str,
    speaker_embedding: torch.Tensor,
    model,
    language: str,
    cfg_scale: float,
    speaking_rate: float,
    pitch_std: float,
    progress_callback=None,
) -> tuple:
    """Generate audio for a single sentence."""
    cond_dict = make_cond_dict(
        text=text,
        language=language,
        speaker=speaker_embedding,
        speaking_rate=speaking_rate,
        pitch_std=pitch_std,
        device=device,
    )
    conditioning = model.prepare_conditioning(cond_dict)

    max_new_tokens = 86 * 30  # ~30 seconds max

    codes = model.generate(
        prefix_conditioning=conditioning,
        max_new_tokens=max_new_tokens,
        cfg_scale=cfg_scale,
        batch_size=1,
        callback=progress_callback,
        disable_torch_compile=True,
    )

    wav_out = model.autoencoder.decode(codes).cpu().detach()
    sr_out = model.autoencoder.sampling_rate

    if wav_out.dim() == 2 and wav_out.size(0) > 1:
        wav_out = wav_out[0:1, :]

    return sr_out, wav_out.squeeze().numpy()


# =============================================================================
# Audio Merging and Export
# =============================================================================


def merge_audio_segments(session: NarrationSession, silence_gap_ms: int = 500) -> tuple:
    """Merge all generated audio segments with silence gaps."""
    sample_rate = 44100
    silence_samples = int(silence_gap_ms * sample_rate / 1000)
    silence = np.zeros(silence_samples, dtype=np.float32)

    segments = []
    for sentence in session.sentences:
        if sentence.audio_data is not None and sentence.status == "done":
            segments.append(sentence.audio_data)
            segments.append(silence)

    if not segments:
        return sample_rate, np.zeros(0, dtype=np.float32)

    # Remove trailing silence
    if len(segments) > 1:
        segments = segments[:-1]

    merged = np.concatenate(segments)
    return sample_rate, merged


def export_audio(audio_data: np.ndarray, sample_rate: int, output_format: str) -> str:
    """Export audio to file. Returns the file path."""
    # Create output directory if needed
    output_dir = os.path.join(os.path.dirname(__file__), "narration_output")
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    if output_format == "WAV":
        output_path = os.path.join(output_dir, f"narration_{timestamp}.wav")
        sf.write(output_path, audio_data, sample_rate)
    else:  # MP3
        # First write WAV to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_wav_path = tmp.name
            sf.write(tmp_wav_path, audio_data, sample_rate)

        output_path = os.path.join(output_dir, f"narration_{timestamp}.mp3")

        # Convert to MP3 using ffmpeg
        try:
            subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-i", tmp_wav_path,
                    "-acodec", "libmp3lame",
                    "-b:a", "192k",
                    output_path,
                ],
                check=True,
                capture_output=True,
            )
        finally:
            os.unlink(tmp_wav_path)

    return output_path


# =============================================================================
# Gradio Event Handlers
# =============================================================================


def handle_script_split(script_text: str, script_file, state):
    """Handle script input and split into sentences."""
    # Get text from file or textbox
    text = ""
    if script_file is not None:
        with open(script_file.name, "r", encoding="utf-8") as f:
            text = f.read()
    elif script_text:
        text = script_text

    if not text.strip():
        return state, [], gr.update(value="No script provided"), gr.update(choices=[])

    # Split into sentences
    sentences = split_script_to_sentences(text)

    # Create session
    session = NarrationSession()
    session.sentences = [
        SentenceItem(index=i, text=s) for i, s in enumerate(sentences)
    ]
    state["session"] = session

    # Update UI
    df_data = session.to_dataframe()
    info = f"Split into {len(sentences)} sentences"

    return state, df_data, gr.update(value=info), gr.update(choices=[])


def handle_add_voice(voice_name: str, voice_audio, model_choice: str, state):
    """Add a new voice profile."""
    if not voice_name or not voice_audio:
        return state, [], "Please provide voice name and audio"

    session = state.get("session", NarrationSession())

    # Load model and compute embedding
    model = load_model_if_needed(model_choice)
    embedding = compute_speaker_embedding(voice_audio, model)

    # Add to session
    session.voices[voice_name] = VoiceProfile(
        name=voice_name,
        audio_path=voice_audio,
        embedding=embedding,
    )

    # Set as default if first voice
    if session.default_voice is None:
        session.default_voice = voice_name

    # Assign default voice to sentences without voice
    for sentence in session.sentences:
        if sentence.voice_name is None:
            sentence.voice_name = session.default_voice

    state["session"] = session

    # Update voice list display
    voice_list = [[name, "Ready"] for name in session.voices.keys()]

    return state, voice_list, f"Added voice: {voice_name}"


def handle_sentence_select(evt: gr.SelectData, state):
    """Handle sentence row selection."""
    session = state.get("session")
    if not session or not session.sentences:
        return gr.update(), gr.update(), gr.update(choices=[]), None

    row_idx = evt.index[0] if isinstance(evt.index, (list, tuple)) else evt.index
    if row_idx >= len(session.sentences):
        return gr.update(), gr.update(), gr.update(choices=[]), None

    sentence = session.sentences[row_idx]
    voice_choices = session.get_voice_names()

    # Get audio if available
    audio_output = None
    if sentence.audio_data is not None:
        audio_output = (sentence.sample_rate, sentence.audio_data)

    return (
        gr.update(value=sentence.text),
        gr.update(value=sentence.voice_name, choices=voice_choices),
        gr.update(choices=voice_choices),
        audio_output,
    )


def handle_voice_assign(selected_idx: int, voice_name: str, state):
    """Assign voice to selected sentence."""
    session = state.get("session")
    if not session or selected_idx is None or selected_idx < 0:
        return state, []

    if selected_idx < len(session.sentences):
        session.sentences[selected_idx].voice_name = voice_name
        state["session"] = session

    return state, session.to_dataframe()


def handle_generate_all(
    model_choice: str,
    language: str,
    cfg_scale: float,
    speaking_rate: float,
    pitch_std: float,
    state,
    progress=gr.Progress(),
):
    """Generate audio for all sentences."""
    session = state.get("session")
    if not session or not session.sentences:
        return state, [], "No sentences to generate"

    if not session.voices:
        return state, session.to_dataframe(), "Please add at least one voice first"

    model = load_model_if_needed(model_choice)
    total = len(session.sentences)

    for i, sentence in enumerate(session.sentences):
        # Skip already done
        if sentence.status == "done" and sentence.audio_data is not None:
            progress((i + 1) / total, desc=f"Skipping {i+1}/{total} (already done)")
            continue

        # Get voice embedding
        voice_name = sentence.voice_name or session.default_voice
        if voice_name not in session.voices:
            sentence.status = "error"
            continue

        voice = session.voices[voice_name]
        sentence.status = "generating"

        progress((i + 0.5) / total, desc=f"Generating {i+1}/{total}: {sentence.text[:30]}...")

        try:
            sr, audio = generate_single_sentence(
                text=sentence.text,
                speaker_embedding=voice.embedding,
                model=model,
                language=language,
                cfg_scale=cfg_scale,
                speaking_rate=speaking_rate,
                pitch_std=pitch_std,
            )
            sentence.audio_data = audio
            sentence.sample_rate = sr
            sentence.status = "done"
        except Exception as e:
            print(f"Error generating sentence {i}: {e}")
            sentence.status = "error"

        progress((i + 1) / total, desc=f"Completed {i+1}/{total}")

    state["session"] = session
    done_count = sum(1 for s in session.sentences if s.status == "done")

    return state, session.to_dataframe(), f"Generated {done_count}/{total} sentences"


def handle_regenerate(
    selected_idx: int,
    model_choice: str,
    language: str,
    cfg_scale: float,
    speaking_rate: float,
    pitch_std: float,
    state,
    progress=gr.Progress(),
):
    """Regenerate a single sentence."""
    session = state.get("session")
    if not session or selected_idx is None or selected_idx < 0:
        return state, [], None, "No sentence selected"

    if selected_idx >= len(session.sentences):
        return state, session.to_dataframe(), None, "Invalid selection"

    sentence = session.sentences[selected_idx]
    voice_name = sentence.voice_name or session.default_voice

    if voice_name not in session.voices:
        return state, session.to_dataframe(), None, "No voice assigned"

    model = load_model_if_needed(model_choice)
    voice = session.voices[voice_name]

    progress(0.5, desc=f"Regenerating: {sentence.text[:30]}...")

    try:
        sr, audio = generate_single_sentence(
            text=sentence.text,
            speaker_embedding=voice.embedding,
            model=model,
            language=language,
            cfg_scale=cfg_scale,
            speaking_rate=speaking_rate,
            pitch_std=pitch_std,
        )
        sentence.audio_data = audio
        sentence.sample_rate = sr
        sentence.status = "done"
    except Exception as e:
        print(f"Error regenerating: {e}")
        sentence.status = "error"
        return state, session.to_dataframe(), None, f"Error: {e}"

    state["session"] = session
    audio_output = (sentence.sample_rate, sentence.audio_data)

    return state, session.to_dataframe(), audio_output, "Regenerated successfully"


def handle_preview_merged(silence_gap: int, state):
    """Preview the merged audio."""
    session = state.get("session")
    if not session:
        return None, "No session"

    sr, merged = merge_audio_segments(session, int(silence_gap))

    if len(merged) == 0:
        return None, "No audio to preview"

    duration = len(merged) / sr
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    return (sr, merged), f"Duration: {minutes:02d}:{seconds:02d}"


def handle_export(silence_gap: int, output_format: str, state):
    """Export the final audio."""
    session = state.get("session")
    if not session:
        return None, "No session"

    sr, merged = merge_audio_segments(session, int(silence_gap))

    if len(merged) == 0:
        return None, "No audio to export"

    try:
        output_path = export_audio(merged, sr, output_format)
        return output_path, f"Exported to: {output_path}"
    except Exception as e:
        return None, f"Export error: {e}"


# =============================================================================
# Build Gradio Interface
# =============================================================================


def build_interface():
    """Build the Narration Studio Gradio interface."""
    # Get supported models
    supported_models = []
    if "transformer" in ZonosBackbone.supported_architectures:
        supported_models.append("Zyphra/Zonos-v0.1-transformer")
    if "hybrid" in ZonosBackbone.supported_architectures:
        supported_models.append("Zyphra/Zonos-v0.1-hybrid")

    with gr.Blocks(title="Narration Studio") as demo:
        # Session state
        state = gr.State(create_empty_session())
        selected_sentence_idx = gr.State(-1)

        gr.Markdown("# Narration Studio")
        gr.Markdown("Batch TTS with multi-voice support for script narration")

        # =====================================================================
        # Panel 1: Setup
        # =====================================================================
        gr.Markdown("## 1. Setup")

        with gr.Row():
            # Script Input
            with gr.Column(scale=1):
                gr.Markdown("### Script Input")
                script_file = gr.File(
                    label="Upload Script (.txt)",
                    file_types=[".txt"],
                )
                script_text = gr.Textbox(
                    label="Or Paste Script",
                    lines=6,
                    placeholder="Paste your script here...",
                )
                split_btn = gr.Button("Split into Sentences", variant="primary")
                split_info = gr.Textbox(label="Status", interactive=False)

            # Voice Management
            with gr.Column(scale=1):
                gr.Markdown("### Voice Management")
                voice_name_input = gr.Textbox(
                    label="Voice Name",
                    placeholder="e.g., Narrator, Character1",
                )
                voice_audio_input = gr.Audio(
                    label="Voice Sample",
                    type="filepath",
                )
                add_voice_btn = gr.Button("Add Voice")
                voice_list = gr.Dataframe(
                    headers=["Voice Name", "Status"],
                    label="Loaded Voices",
                    interactive=False,
                )
                voice_info = gr.Textbox(label="Voice Status", interactive=False)

        # Global Settings
        gr.Markdown("### Generation Settings")
        with gr.Row():
            model_choice = gr.Dropdown(
                choices=supported_models,
                value=supported_models[0] if supported_models else None,
                label="Model",
            )
            language = gr.Dropdown(
                choices=supported_language_codes,
                value="en-us",
                label="Language",
            )
            cfg_scale = gr.Slider(1.0, 5.0, value=2.0, step=0.1, label="CFG Scale")
            speaking_rate = gr.Slider(5.0, 30.0, value=15.0, step=0.5, label="Speaking Rate")
            pitch_std = gr.Slider(0.0, 300.0, value=45.0, step=1, label="Pitch Variation")

        # =====================================================================
        # Panel 2: Sentence Editor
        # =====================================================================
        gr.Markdown("## 2. Sentence Editor")

        sentences_df = gr.Dataframe(
            headers=["#", "Sentence", "Voice", "Status"],
            label="Sentences",
            interactive=False,
            wrap=True,
        )

        with gr.Row():
            with gr.Column(scale=2):
                selected_text = gr.Textbox(
                    label="Selected Sentence",
                    interactive=False,
                    lines=2,
                )
                sentence_voice = gr.Dropdown(
                    label="Assign Voice",
                    choices=[],
                )
            with gr.Column(scale=1):
                sentence_audio = gr.Audio(
                    label="Preview",
                    type="numpy",
                    autoplay=False,
                )
                regenerate_btn = gr.Button("Regenerate Selected")

        with gr.Row():
            generate_all_btn = gr.Button("Generate All", variant="primary")
            generation_status = gr.Textbox(label="Generation Status", interactive=False)

        # =====================================================================
        # Panel 3: Export
        # =====================================================================
        gr.Markdown("## 3. Export")

        with gr.Row():
            with gr.Column(scale=1):
                silence_gap = gr.Slider(
                    0, 2000,
                    value=500,
                    step=50,
                    label="Silence Gap (ms)",
                )
                output_format = gr.Radio(
                    ["MP3", "WAV"],
                    value="MP3",
                    label="Output Format",
                )
            with gr.Column(scale=1):
                preview_btn = gr.Button("Preview Merged")
                merged_audio = gr.Audio(
                    label="Full Narration Preview",
                    type="numpy",
                )
                preview_info = gr.Textbox(label="Duration", interactive=False)

        with gr.Row():
            export_btn = gr.Button("Export", variant="primary")
            export_file = gr.File(label="Download")
            export_info = gr.Textbox(label="Export Status", interactive=False)

        # =====================================================================
        # Event Handlers
        # =====================================================================

        # Script splitting
        split_btn.click(
            fn=handle_script_split,
            inputs=[script_text, script_file, state],
            outputs=[state, sentences_df, split_info, sentence_voice],
        )

        # Voice management
        add_voice_btn.click(
            fn=handle_add_voice,
            inputs=[voice_name_input, voice_audio_input, model_choice, state],
            outputs=[state, voice_list, voice_info],
        )

        # Sentence selection
        sentences_df.select(
            fn=handle_sentence_select,
            inputs=[state],
            outputs=[selected_text, sentence_voice, sentence_voice, sentence_audio],
        )

        # Track selected index
        def update_selected_idx(evt: gr.SelectData):
            return evt.index[0] if isinstance(evt.index, (list, tuple)) else evt.index

        sentences_df.select(
            fn=update_selected_idx,
            inputs=[],
            outputs=[selected_sentence_idx],
        )

        # Voice assignment
        sentence_voice.change(
            fn=handle_voice_assign,
            inputs=[selected_sentence_idx, sentence_voice, state],
            outputs=[state, sentences_df],
        )

        # Generate all
        generate_all_btn.click(
            fn=handle_generate_all,
            inputs=[model_choice, language, cfg_scale, speaking_rate, pitch_std, state],
            outputs=[state, sentences_df, generation_status],
        )

        # Regenerate single
        regenerate_btn.click(
            fn=handle_regenerate,
            inputs=[
                selected_sentence_idx,
                model_choice,
                language,
                cfg_scale,
                speaking_rate,
                pitch_std,
                state,
            ],
            outputs=[state, sentences_df, sentence_audio, generation_status],
        )

        # Preview merged
        preview_btn.click(
            fn=handle_preview_merged,
            inputs=[silence_gap, state],
            outputs=[merged_audio, preview_info],
        )

        # Export
        export_btn.click(
            fn=handle_export,
            inputs=[silence_gap, output_format, state],
            outputs=[export_file, export_info],
        )

    return demo


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    demo = build_interface()
    demo.launch(server_name="0.0.0.0", inbrowser=True)
