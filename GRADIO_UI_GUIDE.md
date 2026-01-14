# Zonos Gradio UI - Complete Guide to Conditioning Parameters

**Last Updated:** January 4, 2026
**Zonos Version:** v0.1 (Transformer Model)

---

## Table of Contents
1. [UI Overview](#ui-overview)
2. [Basic Controls](#basic-controls)
3. [Conditioning Parameters Explained](#conditioning-parameters-explained)
4. [Generation Parameters](#generation-parameters)
5. [Advanced Features](#advanced-features)
6. [Tips & Best Practices](#tips--best-practices)
7. [Common Use Cases](#common-use-cases)

---

## UI Overview

When you open the Gradio interface at `http://127.0.0.1:7860`, you'll see several sections:

1. **Model Selection** - Choose transformer or hybrid model
2. **Text Input** - What to synthesize
3. **Audio Inputs** - Speaker reference and audio prefix
4. **Conditioning Parameters** - Control voice quality/characteristics
5. **Generation Parameters** - CFG scale and seed
6. **Advanced** - Sampling methods, emotions, unconditional toggles

---

## Basic Controls

### 1. Model Selection
```
Dropdown: "Zonos Model Type"
```
**Options:**
- `Zyphra/Zonos-v0.1-transformer` ✅ (Currently available for RTX 5090)
- `Zyphra/Zonos-v0.1-hybrid` (Requires mamba-ssm - not yet compatible)

**What it does:** Selects which architecture to use. Stick with transformer for now.

---

### 2. Text to Synthesize
```
Textbox: "Text to Synthesize"
Max: ~500 characters
```
**What to enter:** The text you want spoken.

**Tips:**
- Keep it under 500 characters for best results
- Use punctuation for natural pauses
- Model will clean and phonemize the text automatically

**Example:**
```
Hello, world! This is a test of the Zonos voice cloning system.
```

---

### 3. Language Code
```
Dropdown: "Language Code"
Default: en-us
```
**Supported Languages:**
- `en-us` - English (US)
- `en-gb` - English (UK)
- `ja` - Japanese
- `zh` - Chinese (Mandarin)
- `fr-fr` - French
- `de` - German
- And many more...

**What it does:** Controls phoneme pronunciation and text processing via eSpeak.

---

### 4. Speaker Audio (Voice Cloning)
```
Audio Upload: "Optional Speaker Audio (for cloning)"
```
**What to upload:**
- 10-30 second clean audio clip of the voice you want to clone
- WAV, MP3, or other common formats accepted

**Best Practices:**
- ✅ Use **clean recordings** (no background noise, music, or overlapping voices)
- ✅ Speech-only clips work best
- ✅ Can concatenate multiple clips from same speaker for better results
- ✅ If you have a noisy clip, check "Denoise Speaker?" box
- ❌ Avoid clips with background music (use source separation first)
- ❌ Don't use clips with multiple speakers

**Denoise Speaker Checkbox:**
- Enable if your speaker reference has noise/echo
- Works with VQScore to clean the embedding
- Check this if output sounds echoey or weird

---

### 5. Prefix Audio (Audio Continuation)
```
Audio Upload: "Optional Prefix Audio (continue from this audio)"
Default: assets/silence_100ms.wav
```
**What it does:**
- Model continues generating from the END of this audio
- Useful for matching the exact prosody/tone at a specific moment
- Default is 100ms of silence (neutral start)

**Use Cases:**
- Continue a sentence from where it was cut off
- Match the exact emotional tone of a moment
- Create seamless audio concatenations

---

## Conditioning Parameters Explained

These parameters control the **characteristics** of the generated voice.

### DNSMOS Overall
```
Slider: 1.0 - 5.0
Default: 4.0
Available: Hybrid model only (grayed out for transformer)
```
**What it is:** [Deep Noise Suppression Mean Opinion Score](https://arxiv.org/abs/2110.01763) - a quality metric for speech.

**How to use:**
- **4.0** = Very clean, neutral English speech
- **Lower values** = More expressive but potentially noisier
- **Higher values** = Maximum cleanliness

**Important Notes:**
- Strong correlation with emotions (neutral speech scores higher)
- Strong correlation with language (optimized for English)
- For expressive speech, set to **unconditional** (see Advanced)

---

### Fmax (Maximum Frequency)
```
Slider: 0 - 24000 Hz
Default: 24000
```
**What it is:** The maximum frequency content in the output audio.

**How to use:**
- **22050 Hz** = 44.1 kHz audio (Recommended for voice cloning)
- **24000 Hz** = 48 kHz audio
- **Lower values** = Lower quality, muffled sound

**Why it matters:**
- Model trained at 44.1 kHz sampling rate
- Different values represent different training data slices
- Both 22050 and 24000 work well, but have slightly different voicing

**Best Practice:** Use **22050** for voice cloning.

---

### VQ Score
```
Slider: 0.5 - 0.8
Default: 0.78
Available: Hybrid model only (grayed out for transformer)
```
**What it is:** [VQScore](https://github.com/JasonSWFu/VQscore) - unsupervised speech quality estimation.

**How to use:**
- **0.78** = High-quality, clean speech
- **Lower values** = Lower quality but more expressive
- Values are per-chunk (8 chunks for 8-second audio)

**Important Notes:**
- Strong negative correlation with expressiveness
- For expressive/emotional speech, set to **unconditional**
- Better generalization than DNSMOS

**In Gradio:** All 8 dimensions set to the same value (simplified interface).

---

### Pitch Std (Pitch Standard Deviation)
```
Slider: 0.0 - 300.0
Default: 45.0
```
**What it is:** Standard deviation of pitch variation in the output.

**How to use:**
- **20-45** = Normal conversational speech
- **60-150** = Expressive, emotional speech
- **>150** = Very dramatic/theatrical speech

**What it affects:**
- Higher values = more pitch variation = more expressive
- Lower values = monotone, flat delivery
- Correlated with emotion (emotional speech has higher pitch variation)

**Examples:**
- Reading a book: 25-35
- Excited storytelling: 80-120
- Dramatic narration: 150-200

---

### Speaking Rate
```
Slider: 5.0 - 30.0 phonemes/second
Default: 15.0
```
**What it is:** Number of phonemes (sound units) spoken per second.

**How to use:**
- **10-15** = Normal conversational pace
- **15-20** = Slightly faster, energetic
- **20-25** = Fast speech (news anchor)
- **25-30** = Very fast (may sound unnatural)

**Critical for long texts:**
```
Formula: phonemes_per_second = total_phonemes / generation_length

Example:
- Text has 300 phonemes
- Generation length: 30 seconds (model max)
- Minimum speaking rate: 300/30 = 10 phonemes/sec

If you set speaking rate too low for long text:
- Model may not finish
- May sound unnaturally slow
```

**Best Practice:**
- For long texts, calculate required rate
- Cut text into chunks rather than using unrealistically slow rates

---

## Generation Parameters

### CFG Scale (Classifier-Free Guidance)
```
Slider: 1.0 - 5.0
Default: 2.0
```
**What it is:** Controls how strictly the model follows conditioning.

**How to use:**
- **1.0** = Ignore conditioning, more random (currently broken, don't use)
- **2.0** = Balanced adherence to conditioning (recommended)
- **3.0-4.0** = Stronger conditioning, more controlled
- **5.0** = Maximum conditioning adherence

**What it affects:**
- Higher = more predictable, follows your parameters closely
- Lower = more creative, may deviate from parameters
- Too high = can cause artifacts or over-fitting

**Recommended:** Start with **2.0** and adjust if needed.

---

### Seed
```
Number Input
Default: 420
```
**What it is:** Random number generator seed for reproducibility.

**How to use:**
- **Same seed** = Same output (given same inputs)
- **Different seed** = Different output variation

**Randomize Seed Checkbox:**
- ✅ Checked = Generate new seed each time (different outputs)
- ⬜ Unchecked = Use specified seed (reproducible outputs)

**Use Cases:**
- **Randomize ON**: Exploring different variations
- **Randomize OFF**: Reproducing exact output, iterating on parameters

---

## Advanced Features

### Sampling Methods

There are **two sampling methods**: NovelAI's Unified Sampler (modern) and Legacy Sampling (traditional).

#### NovelAI's Unified Sampler (Recommended)

**Linear Slider**
```
Range: -2.0 to 2.0
Default: 0.5
```
- **0** = Disable unified sampling (fallback to legacy)
- **Positive values** = Less random (more deterministic)
- **Negative values** = More random
- **Recommended:** 0.3 - 0.7

**Confidence Slider**
```
Range: -2.0 to 2.0
Default: 0.40
```
- Controls randomness of already-random outputs
- **Low values** = Random outputs become MORE random
- **High values** = Random outputs become MORE predictable
- Theoretical range: -2 × Quadratic to 0
- **Recommended:** 0.3 - 0.5

**Quadratic Slider**
```
Range: -2.0 to 2.0
Default: 0.00
```
- Affects low-probability tokens
- **High values** = Low probabilities become MUCH lower (more conservative)
- **Low/Negative** = Low probabilities stay relevant
- **Recommended:** 0.0 (neutral)

---

#### Legacy Sampling

**Top P (Nucleus Sampling)**
```
Range: 0.0 - 1.0
Default: 0 (disabled)
```
- Keeps tokens that cumulatively sum to P probability
- **0.9** = Keep top 90% probable tokens
- **0** = Disabled

**Min K**
```
Range: 0 - 1024
Default: 0 (disabled)
```
- Keep at least K top tokens
- Prevents too much filtering

**Min P**
```
Range: 0.0 - 1.0
Default: 0 (disabled)
```
- Remove tokens below P × max_probability
- **0.1** = Remove tokens <10% of top token's probability

**Note:** Unified sampler is recommended. Only use legacy if you have specific requirements.

---

### Emotion Sliders

```
Located in: Advanced Parameters > Emotion Sliders
```

**⚠️ Warning:** These sliders are **not intuitive** and require experimentation!

**8 Emotion Dimensions:**
1. **Happiness** (default: 1.0)
2. **Sadness** (default: 0.05)
3. **Disgust** (default: 0.05)
4. **Fear** (default: 0.05)
5. **Surprise** (default: 0.05)
6. **Anger** (default: 0.05)
7. **Other** (default: 0.1)
8. **Neutral** (default: 0.2)

**How they work:**
- Values are relative weights, not absolute emotions
- **Heavily entangled** with:
  - Text sentiment (angry text → easier to make angry)
  - Pitch std (higher pitch std correlates with more emotion)
  - VQScore/DNSMOS (favor neutral speech)

**Best Practices:**
- ✅ **Default:** Set "emotion" to unconditional (recommended)
- ✅ For specific emotion: Increase that dimension, decrease others
- ✅ Start with presets, adjust gradually
- ❌ Don't expect linear control
- ❌ Certain combinations can cause instability

**Advanced Technique: Negative Prompting**
- Set unconditional to highly neutral emotion vector
- CFG will push AWAY from neutral
- Exaggerates emotions in output

**Recommended:** Unless you have specific needs, keep emotion **unconditional**.

---

### Unconditional Toggles

```
Located in: Advanced Parameters > Unconditional Keys
```

**What "Unconditional" means:**
- Model **ignores** that conditioning parameter
- Model **auto-fills** appropriate value based on other context
- Gives model more creative freedom for that attribute

**Available Toggles:**
- ☐ speaker
- ☑ emotion (checked by default)
- ☐ vqscore_8
- ☐ fmax
- ☐ pitch_std
- ☐ speaking_rate
- ☐ dnsmos_ovrl
- ☐ speaker_noised

**When to use:**

| Toggle | When to Use | Effect |
|--------|-------------|--------|
| **emotion** | Default (always) | Model chooses emotion from text/context |
| **speaker** | Generate random voice | Ignores speaker reference, creates new voice |
| **vqscore_8** | Expressive speech | Prevents quality conditioning from suppressing emotion |
| **pitch_std** | Let model decide | Auto-adjusts to text expressiveness |
| **speaking_rate** | Auto-pacing | Model chooses natural pace for text |
| **dnsmos_ovrl** | Expressive speech | Prevents quality bias toward neutral |

**Recommended defaults:**
- ✅ emotion = unconditional (checked)
- ⬜ Everything else = conditional (unchecked)

---

## Tips & Best Practices

### For Voice Cloning

1. **Speaker Reference Audio:**
   - Use 15-30 seconds of clean speech
   - Single speaker only
   - No background music or noise
   - Can concatenate multiple clips from same speaker

2. **Conditioning Settings:**
   - fmax: **22050**
   - pitch_std: Match reference or use **unconditional**
   - speaking_rate: **15** for normal speech
   - CFG scale: **2.0**
   - emotion: **unconditional** (default)

3. **If clone sounds wrong:**
   - ✅ Check "Denoise Speaker?"
   - ✅ Set VQScore higher (0.78)
   - ✅ Try different speaker reference clip
   - ✅ Ensure reference is single speaker, clean audio

---

### For Expressive Speech

1. **Settings:**
   - pitch_std: **80-150**
   - emotion: **unconditional** OR specific emotion boosted
   - vqscore_8: **unconditional** (if hybrid)
   - dnsmos_ovrl: **unconditional** (if hybrid)

2. **Why:**
   - Quality metrics (VQ/DNSMOS) bias toward neutral speech
   - Setting them unconditional allows expressiveness
   - Higher pitch_std enables variation

---

### For Clean, High-Quality Speech

1. **Settings:**
   - fmax: **22050** or **24000**
   - pitch_std: **30-45**
   - speaking_rate: **12-15**
   - dnsmos_ovrl: **4.0** (if hybrid)
   - vqscore_8: **0.78** (if hybrid)
   - emotion: **unconditional** or neutral-heavy

2. **Why:**
   - High quality metrics suppress artifacts
   - Moderate pitch_std keeps it natural
   - Normal speaking rate sounds professional

---

### For Long Text

1. **Calculate phonemes:**
   ```
   Most models phonemize ~2 characters = 1 phoneme
   500 characters ≈ 250 phonemes
   ```

2. **Set speaking rate:**
   ```
   Max generation: 30 seconds
   250 phonemes / 30 sec = 8.3 phonemes/sec (too slow!)

   Better: Split into 2 chunks
   125 phonemes / 30 sec = 4.2 phonemes/sec per chunk
   Or use 15 phonemes/sec with shorter generation
   ```

3. **Recommendation:**
   - Keep generations under 30 seconds
   - Split long text into natural paragraphs
   - Use realistic speaking rates (10-20)

---

## Common Use Cases

### 1. Simple Voice Cloning
```
Text: "Hello, this is my cloned voice."
Language: en-us
Speaker Audio: <upload your voice sample>
Denoise Speaker: ☐
fmax: 22050
pitch_std: 45
speaking_rate: 15
CFG Scale: 2.0
emotion: unconditional ✓
Randomize Seed: ✓
```

---

### 2. Expressive Storytelling
```
Text: "And then, the dragon roared with terrible fury!"
Language: en-us
Speaker Audio: <dramatic voice>
pitch_std: 120
speaking_rate: 12
CFG Scale: 2.5
emotion: anger=0.7, fear=0.3, neutral=0.1
        (or keep unconditional)
vqscore_8: unconditional ✓ (if hybrid)
```

---

### 3. Professional Narration
```
Text: <your narration script>
Language: en-us
Speaker Audio: <professional voice>
fmax: 24000
pitch_std: 35
speaking_rate: 14
dnsmos_ovrl: 4.0 (if hybrid)
CFG Scale: 2.0
emotion: unconditional ✓
```

---

### 4. Multi-Language Speech
```
Text: "Bonjour, comment allez-vous?"
Language: fr-fr  ← Important!
Speaker Audio: <French speaker preferred>
pitch_std: 40
speaking_rate: 15
All other settings: default
```

---

### 5. Audio Continuation
```
Prefix Audio: <upload audio to continue>
Text: "...and that's how the story ends."
[Adjust speaking_rate/pitch_std to match prefix audio]
```

---

## Reference Documentation

For detailed technical explanations of each conditioning parameter, see:
- **CONDITIONING_README.md** (in project root)
- Official Zonos docs: https://github.com/Zyphra/Zonos

For code-level details:
- `gradio_interface.py` - UI implementation
- `zonos/conditioning.py` - Conditioning logic
- `zonos/model.py` - Model generation

---

## Quick Troubleshooting

### Output sounds robotic/monotone
- ✅ Increase pitch_std (60-100)
- ✅ Set emotion to unconditional
- ✅ Try expressive speaker reference

### Output is noisy/echoey
- ✅ Check "Denoise Speaker?"
- ✅ Increase VQScore (0.78)
- ✅ Use cleaner speaker reference
- ✅ Increase dnsmos_ovrl (4.0-4.5)

### Doesn't sound like speaker reference
- ✅ Use longer reference (20-30 sec)
- ✅ Ensure reference is single speaker
- ✅ Try concatenating multiple clips
- ✅ Make sure "speaker" is NOT unconditional

### Generation is too fast/slow
- ✅ Adjust speaking_rate slider
- ✅ Calculate: text_phonemes / speaking_rate = duration
- ✅ Split long text into chunks

### Model crashes or errors
- ✅ Check text length (<500 chars)
- ✅ Verify speaker audio format (WAV/MP3)
- ✅ Restart Gradio interface
- ✅ Check RTX5090_SETUP_SUMMARY.md for environment issues

---

**Happy voice cloning!** 🎙️

For environment setup and PyTorch issues, see **RTX5090_SETUP_SUMMARY.md**
