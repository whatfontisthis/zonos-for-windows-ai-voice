import torch
import soundfile as sf
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

print(f"Using device: {device}")
print(f"PyTorch version: {torch.__version__}")

# model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-hybrid", device=device)
print("Loading Zonos model...")
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

print("Loading example audio with soundfile...")
wav_data, sampling_rate = sf.read("assets/exampleaudio.mp3")
# Convert to torch tensor and add batch dimension if needed
wav = torch.from_numpy(wav_data).float()
if wav.dim() == 1:
    wav = wav.unsqueeze(0)  # Add channel dimension
elif wav.dim() == 2:
    wav = wav.T  # soundfile uses (frames, channels), we need (channels, frames)

print("Creating speaker embedding...")
speaker = model.make_speaker_embedding(wav, sampling_rate)

torch.manual_seed(421)

print("Generating speech...")
cond_dict = make_cond_dict(text="Hello, world!", speaker=speaker, language="en-us")
conditioning = model.prepare_conditioning(cond_dict)

codes = model.generate(conditioning, disable_torch_compile=True)

print("Decoding audio...")
wavs = model.autoencoder.decode(codes).cpu()

print("Saving to sample_rtx5090.wav...")
# Use soundfile to save
import numpy as np
audio_np = wavs[0].numpy().T  # Convert back to (frames, channels)
sf.write("sample_rtx5090.wav", audio_np, model.autoencoder.sampling_rate)

print("✓ Done! Audio saved to sample_rtx5090.wav")
print(f"RTX 5090 test successful with PyTorch {torch.__version__}!")
