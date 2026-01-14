# Voice Generation Guide - Finding Your Perfect Voice

**Date:** January 4, 2026
**Purpose:** Generate and discover unique voices without voice cloning

---

## Table of Contents
1. [Male/Female Voice Generation](#malefemale-voice-generation)
2. [Generating Consistent Voices](#generating-consistent-voices)
3. [Finding Your Ideal Voice](#finding-your-ideal-voice)
4. [Practical Workflows](#practical-workflows)
5. [Quick Reference](#quick-reference)

---

## Male/Female Voice Generation

### Understanding Voice Gender Control

The model's voice gender is controlled by the **Speaker Audio** you upload, NOT by an explicit "male/female" switch.

### Method 1: Using Speaker Reference (Voice Cloning)
```
Male Voice:
- Upload audio of a male speaker
- Model will clone that male voice

Female Voice:
- Upload audio of a female speaker
- Model will clone that female voice
```

### Method 2: Random Voice Generation (No Reference)

If you want the model to generate a random voice:

1. Go to **Advanced Parameters** → **Unconditional Keys**
2. **Check ☑ speaker**
3. Leave **"Speaker Audio"** field **empty** (don't upload anything)
4. Model will auto-generate voices (gender based on parameters + randomness)

**Important:** The model doesn't have a direct "male/female" slider. Gender characteristics come from:
- Your speaker reference audio (if provided)
- Random generation influenced by pitch_std and other parameters (if speaker is unconditional)

---

## Generating Consistent Voices

### Getting Identical Output Every Time

To get **100% identical** output:

#### Required Settings:

1. **Same Speaker Reference (if cloning):**
   - Upload the SAME audio file every time
   - File path matters: `recording1.wav` ≠ `recording2.wav` even if content is identical
   - Speaker embedding is cached per file path

2. **Disable Randomize Seed:**
   ```
   Generation Parameters:
   - Randomize Seed: OFF ⬜
   - Seed: Set to specific number (e.g., 420)
   ```
   - Same seed = same randomness = same output

3. **Keep All Parameters Identical:**
   - Text (exact same)
   - Language code
   - Pitch Std
   - Speaking Rate
   - CFG Scale
   - All other sliders
   - Unconditional keys selection

### Example for Perfect Consistency:

```
Session 1:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Speaker Audio: my_voice.wav
Text: "Hello world"
Language: en-us
Seed: 420
Randomize Seed: OFF ⬜
pitch_std: 45
speaking_rate: 15
CFG Scale: 2.0
All other settings: default

Session 2 (hours/days later):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
(Use EXACT same settings as above)

Result: BYTE-FOR-BYTE IDENTICAL audio
```

### Different Variations of Same Voice

For **similar voice** but **different delivery**:

```
Fixed:
- Speaker Audio: my_voice.wav (same)
- All parameters: same

Vary:
- Text: "Different text each time"
- Seed: 420 → 421 → 422 (change seed)
- OR: Enable "Randomize Seed" ✓

Result: Same voice character, different natural variations
```

---

## Finding Your Ideal Voice

### ⚠️ Critical First Step

**Before exploring voices, you MUST:**

1. Go to **Advanced Parameters** → **Unconditional Keys**
2. **Check ☑ speaker** ← THIS IS ESSENTIAL!
3. Leave **"Speaker Audio"** empty
4. Now seeds will generate different voice characters

**Without this:** Changing seed only varies delivery, not the voice itself!

---

### Strategy 1: Rapid Random Search (Fast Discovery)

**Best for:** Quick exploration, finding general voice types

```
Setup:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Speaker Audio: (leave empty)
✓ Unconditional Keys: ☑ speaker (CHECKED!)
✓ Randomize Seed: ON ✓
✓ Text: "This is a test of my voice generation."
✓ Language: en-us
✓ pitch_std: 45 (start here)
✓ speaking_rate: 15 (start here)
✓ All other settings: default

Process:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Click "Generate Audio"
2. Listen to output
3. Like it? Note the seed number! (shown after generation)
4. Don't like it? Click "Generate" again → new random seed
5. Repeat 20-50 times
6. Keep notes of good seeds

Result: Fast exploration, each click = new voice character
```

---

### Strategy 2: Systematic Seed Search (Reproducible)

**Best for:** Methodical exploration, building a voice library

```
Setup:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Speaker Audio: (empty)
✓ Unconditional Keys: ☑ speaker
✓ Randomize Seed: OFF ⬜
✓ Seed: 1 (will increment manually)
✓ Text: "Hello, my name is Assistant."
✓ pitch_std: 45
✓ speaking_rate: 15

Process:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Set Seed = 1, generate, listen
2. Set Seed = 2, generate, listen
3. Set Seed = 3, generate, listen
4. Keep notes: "Seed 23 = warm male, Seed 67 = professional female"
5. Test seeds 1-100 (good coverage)
6. Optional: Jump to 1000-1100, 5000-5100 for variety

Result: Reproducible, can revisit exact voices anytime
```

---

### Strategy 3: Parameter Grid Search (Best Results)

**Best for:** Finding specific voice characteristics

Just varying seed isn't enough! These parameters dramatically affect voice character:

#### Key Parameters That Shape Voice:

**1. Pitch Std** (Most Important!)
```
Range: 0-300
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20-30   = Monotone, flat, robotic
35-45   = Lower pitch, often sounds more masculine
50-60   = Normal conversational, neutral
65-80   = Higher pitch, often sounds more feminine
90-150  = Very expressive, dramatic
150+    = Theatrical, exaggerated
```

**2. Speaking Rate**
```
Range: 5-30 phonemes/second
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8-12    = Slow, deliberate, narrator-like
13-16   = Normal conversational pace
17-22   = Fast, energetic, excited
23-30   = Very fast (may sound rushed)
```

**3. Fmax** (Subtle but noticeable)
```
Options: 22050 or 24000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
22050   = Warmer, slightly mellower tone
24000   = Brighter, crisper tone
```

#### Recommended Exploration Grid:

```
MALE-ISH VOICES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Configuration 1:
- pitch_std: 35
- speaking_rate: 12
- fmax: 22050
- Test seeds: 1-50

Configuration 2:
- pitch_std: 40
- speaking_rate: 14
- fmax: 22050
- Test seeds: 1-50

FEMALE-ISH VOICES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Configuration 3:
- pitch_std: 55
- speaking_rate: 15
- fmax: 24000
- Test seeds: 1-50

Configuration 4:
- pitch_std: 65
- speaking_rate: 14
- fmax: 24000
- Test seeds: 1-50

DRAMATIC/EXPRESSIVE VOICES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Configuration 5:
- pitch_std: 120
- speaking_rate: 10
- fmax: 24000
- Test seeds: 1-50

Configuration 6:
- pitch_std: 100
- speaking_rate: 13
- fmax: 22050
- Test seeds: 1-50
```

**Total voices tested:** 6 configurations × 50 seeds = 300 voices
**Much more effective than testing 10,000 seeds with same parameters!**

---

## Practical Workflows

### Complete Voice Discovery Workflow

#### Phase 1: Broad Search (Find Voice Type)

**Goal:** Determine which pitch_std range you prefer

```
Setup:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Speaker: unconditional ☑
✓ Text: "Hello, my name is Assistant. I'm here to help you."
✓ Randomize Seed: ON ✓
✓ speaking_rate: 15 (keep constant)

Process:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Set pitch_std = 30
   - Generate 5 times (randomize seed)
   - Note general character: "Too flat, monotone"

2. Set pitch_std = 40
   - Generate 5 times
   - Note: "Nice and warm, slightly masculine"

3. Set pitch_std = 50
   - Generate 5 times
   - Note: "Neutral, professional"

4. Set pitch_std = 60
   - Generate 5 times
   - Note: "Bright, slightly feminine" ← I LIKE THIS!

5. Set pitch_std = 70
   - Generate 5 times
   - Note: "Too high-pitched"

Decision: pitch_std = 60 is my preferred range!
```

---

#### Phase 2: Narrow Search (Find Exact Voice)

**Goal:** Find the perfect seed in your preferred range

```
Setup:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Speaker: unconditional ☑
✓ Text: "Hello, my name is Assistant. I'm here to help you."
✓ pitch_std: 60 (locked from Phase 1)
✓ speaking_rate: 15
✓ Randomize Seed: OFF ⬜

Process:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Seed 1:  Generate → "Too breathy"
Seed 2:  Generate → "Meh, average"
Seed 3:  Generate → "Nice, but too young"
...
Seed 23: Generate → "PERFECT! Warm, professional female" ★
...
Seed 67: Generate → "Also great! Energetic, friendly" ★
...
Seed 89: Generate → "Good backup option" ★
...
(Continue to seed 100)

Winners: Seeds 23, 67, 89
```

---

#### Phase 3: Refine (Polish Your Favorite)

**Goal:** Fine-tune the best voice to perfection

```
Setup:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Speaker: unconditional ☑
✓ Seed: 23 (locked - your favorite from Phase 2)
✓ Randomize Seed: OFF ⬜
✓ Text: "Hello, my name is Assistant. I'm here to help you."

Experiment 1: Speaking Rate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- speaking_rate 13: "Too slow"
- speaking_rate 14: "Just right!" ★
- speaking_rate 15: "Slightly too fast"

Experiment 2: CFG Scale
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- CFG 1.8: "Too loose, inconsistent"
- CFG 2.0: "Perfect!" ★
- CFG 2.2: "Too rigid"

Experiment 3: Pitch Std Fine-tuning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- pitch_std 58: "Slightly flat"
- pitch_std 60: "Still great!" ★
- pitch_std 62: "Too varied"

FINAL PERFECT SETTINGS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Seed: 23
pitch_std: 60
speaking_rate: 14
CFG Scale: 2.0
fmax: 24000
Language: en-us
All else: default

SAVE THESE! Write them down or screenshot!
```

---

### Time-Saving Tips

#### 1. Use Consistent Test Phrase

**Always use the same text for testing:**
```
"Hello, my name is Assistant. I'm here to help you today."
```

**Why?**
- Easier to compare voices objectively
- Same phonemes = fair comparison
- Can focus on voice, not content

**Alternative test phrases:**
```
Short: "The quick brown fox jumps over the lazy dog."
Medium: "Welcome to today's presentation on artificial intelligence."
Long: "Good morning everyone. Today we'll explore the fascinating world of voice synthesis technology."
```

---

#### 2. Keep a Voice Discovery Log

Create a text file: `my_voices.txt`

```
VOICE DISCOVERY LOG
Created: January 4, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL FEMALE NARRATOR
  Seed: 23
  pitch_std: 60
  speaking_rate: 14
  CFG Scale: 2.0
  fmax: 24000
  Notes: Warm, clear, perfect for tutorials
  ★★★★★

FRIENDLY ASSISTANT
  Seed: 67
  pitch_std: 55
  speaking_rate: 15
  CFG Scale: 2.0
  fmax: 24000
  Notes: Energetic, approachable, great for guides
  ★★★★☆

CALM MALE NARRATOR
  Seed: 142
  pitch_std: 35
  speaking_rate: 12
  CFG Scale: 2.0
  fmax: 22050
  Notes: Deep, slow, perfect for meditations
  ★★★★★

DRAMATIC STORYTELLER
  Seed: 89
  pitch_std: 120
  speaking_rate: 10
  CFG Scale: 2.5
  fmax: 24000
  Notes: Very expressive, use for fiction/drama
  ★★★☆☆

NEUTRAL ASSISTANT
  Seed: 456
  pitch_std: 50
  speaking_rate: 15
  CFG Scale: 2.0
  fmax: 24000
  Notes: Balanced, professional, general purpose
  ★★★★☆
```

---

#### 3. Test in Smart Batches

**Don't test seeds 1-10000 sequentially!**

Instead, use strategic sampling:

```
Batch 1: Seeds 1-100
  → Covers most common voice types
  → 90% of unique voices appear here

Batch 2: Seeds 1000-1100 (if needed)
  → Different random space
  → Often produces variations of Batch 1

Batch 3: Seeds 5000-5100 (if needed)
  → Further exploration
  → Diminishing returns

Batch 4: Random jumps (if needed)
  → Seeds: 234, 789, 1337, 2468, 9999
  → Just for fun/lucky numbers
```

**Reality:** Most users find their perfect voice in first 50-100 seeds when combined with parameter variation!

---

#### 4. Focus on Pitch Std First

**Pitch Std has the BIGGEST impact on voice character.**

Efficient exploration strategy:

```
Round 1: Test pitch_std values
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
pitch_std: 30 → Generate 10 random seeds
pitch_std: 40 → Generate 10 random seeds
pitch_std: 50 → Generate 10 random seeds
pitch_std: 60 → Generate 10 random seeds
pitch_std: 70 → Generate 10 random seeds
pitch_std: 80 → Generate 10 random seeds
pitch_std: 100 → Generate 10 random seeds

Total: 70 voices tested
Result: You'll know which pitch_std you prefer!

Round 2: Deep dive into winner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preferred pitch_std = 60
Test seeds 1-100 systematically

Total additional: 100 voices
Grand total: 170 voices tested

This is MUCH more effective than:
Testing 10,000 seeds all at pitch_std=45!
```

---

#### 5. Use Emotion Unconditional (Default)

**Keep "emotion" checked as unconditional** (default setting)

**Why?**
- Emotion sliders are complex and entangled
- Unconditional lets model choose naturally
- More consistent voice character
- Less weird artifacts

**Only change emotions if:**
- You specifically want angry/sad/happy delivery
- You understand the complexity (see GRADIO_UI_GUIDE.md)
- You're willing to experiment extensively

---

## Quick Reference

### Voice Consistency Matrix

| Goal | Speaker Audio | Speaker Unconditional | Randomize Seed | Result |
|------|---------------|----------------------|----------------|--------|
| Clone voice, same output | Upload file | ⬜ No | ⬜ OFF | 100% identical |
| Clone voice, variations | Upload file | ⬜ No | ✓ ON | Same voice, different delivery |
| Generate voice, same output | Empty | ✓ Yes | ⬜ OFF | 100% identical generated voice |
| Generate voice, variations | Empty | ✓ Yes | ✓ ON | Different voices each time |
| Explore many voices | Empty | ✓ Yes | ✓ ON | Random discovery mode |

---

### Parameter Cheat Sheet

```
VOICE CHARACTER QUICK GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MALE-SOUNDING:
  pitch_std: 30-45
  speaking_rate: 12-14
  fmax: 22050

FEMALE-SOUNDING:
  pitch_std: 55-70
  speaking_rate: 14-16
  fmax: 24000

NEUTRAL/PROFESSIONAL:
  pitch_std: 45-55
  speaking_rate: 14-16
  CFG Scale: 2.0

EXPRESSIVE/DRAMATIC:
  pitch_std: 90-150
  speaking_rate: 10-13
  CFG Scale: 2.5

CALM/MEDITATIVE:
  pitch_std: 25-35
  speaking_rate: 8-12
  CFG Scale: 2.0

ENERGETIC/EXCITED:
  pitch_std: 65-85
  speaking_rate: 17-22
  CFG Scale: 2.0
```

---

### Essential Checklist for Voice Generation

**Before you start exploring:**

- [ ] Advanced Parameters → Unconditional Keys → **Check ☑ speaker**
- [ ] Leave **Speaker Audio field empty**
- [ ] Choose a **consistent test phrase**
- [ ] Create a **log file** to track favorites
- [ ] Start with **randomize seed ON** for discovery
- [ ] Test **different pitch_std values** (30, 40, 50, 60, 70)
- [ ] Keep **other parameters default** initially
- [ ] When you find a good voice, **note the seed!**
- [ ] Switch to **randomize seed OFF** to lock it in
- [ ] **Fine-tune** parameters with locked seed

---

### Recommended Workflow Summary

```
PHASE 1: BROAD SEARCH (30 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal: Find preferred pitch_std range
Method: Test pitch_std 30, 40, 50, 60, 70
Action: Generate 10 times per pitch_std (randomize ON)
Output: "I prefer pitch_std=60!"

PHASE 2: NARROW SEARCH (30-60 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal: Find specific seeds you love
Method: Lock pitch_std=60, test seeds 1-100
Action: Randomize OFF, increment seed manually
Output: "Seeds 23, 67, 142 are my favorites!"

PHASE 3: REFINEMENT (15 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal: Perfect your top 3 voices
Method: Lock favorite seed, vary other parameters
Action: Test speaking_rate, CFG scale
Output: Final polished settings saved!

TOTAL TIME: 1.5-2 hours
RESULT: 3-5 perfect voices you can use forever!
```

---

### Understanding the Caching System

**From the code (gradio_interface.py:148-158):**

```python
if speaker_audio != SPEAKER_AUDIO_PATH:
    print("Recomputed speaker embedding")
    # Creates new embedding
    SPEAKER_AUDIO_PATH = speaker_audio
```

**What this means:**

| Scenario | Embedding Created? | Speed |
|----------|-------------------|-------|
| First upload of `voice1.wav` | ✓ Yes | Slow (~5 sec) |
| Re-using same `voice1.wav` | ✗ No (cached) | Instant |
| Upload `voice2.wav` | ✓ Yes | Slow (~5 sec) |
| Upload `voice1.wav` again | ✓ Yes (cache uses file path!) | Slow (~5 sec) |

**Pro Tip:** Keep your speaker reference files in a stable location with consistent names for best caching!

---

### Common Mistakes to Avoid

**❌ WRONG: Testing 10,000 seeds with same parameters**
```
Seed 1-10000, all at pitch_std=45
Result: Mostly similar voices, wasted time
```

**✅ CORRECT: Testing parameter combinations**
```
5 pitch_std values × 50 seeds each = 250 voices
Result: Huge variety, efficient use of time
```

---

**❌ WRONG: Forgot to make speaker unconditional**
```
speaker: conditional (unchecked)
Randomize seed: ON
Result: Same voice, different delivery (not what you want!)
```

**✅ CORRECT: Speaker set to unconditional**
```
speaker: unconditional ☑
Randomize seed: ON
Result: Different voices each time
```

---

**❌ WRONG: No logging/notes**
```
"I heard a great voice 30 minutes ago, but forgot the seed!"
Result: Can never recreate it
```

**✅ CORRECT: Keep a log**
```
Voice Discovery Log with seeds, parameters, notes
Result: Can recreate any voice anytime
```

---

**❌ WRONG: Changing text while testing**
```
Seed 1: "Hello world"
Seed 2: "Testing voice generation"
Seed 3: "This is a sample"
Result: Can't compare fairly
```

**✅ CORRECT: Consistent test phrase**
```
All seeds: "Hello, my name is Assistant."
Result: Easy to compare objectively
```

---

## Advanced Tips

### Creating a Voice Library

Once you've found several great voices, organize them:

**Create preset files or documents:**

```
VOICE LIBRARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use Case: Tutorial Videos
  Voice: Professional Female Narrator
  Seed: 23
  Settings: pitch_std=60, rate=14, CFG=2.0

Use Case: Meditation/Relaxation
  Voice: Calm Male Voice
  Seed: 142
  Settings: pitch_std=35, rate=12, CFG=2.0

Use Case: Audiobook Fiction
  Voice: Dramatic Storyteller
  Seed: 89
  Settings: pitch_std=120, rate=10, CFG=2.5

Use Case: Customer Service Bot
  Voice: Friendly Assistant
  Seed: 67
  Settings: pitch_std=55, rate=15, CFG=2.0

Use Case: News/Announcements
  Voice: Neutral Professional
  Seed: 456
  Settings: pitch_std=50, rate=16, CFG=2.0
```

---

### Multi-Speaker Projects

**For projects needing multiple distinct voices:**

```
Dialogue Scene: Two Characters
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Character A (Male):
  - Seed: 142
  - pitch_std: 35
  - speaking_rate: 13

Character B (Female):
  - Seed: 23
  - pitch_std: 60
  - speaking_rate: 15

Both use:
  - speaker: unconditional ☑
  - Randomize seed: OFF ⬜
  - Same CFG, same language

Result: Consistent distinct voices for each character
```

---

### Reproducing Voices on Different Machines

**Settings are universal!**

If you find a voice on Computer A, you can recreate it on Computer B:

```
Computer A (Discovery):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found perfect voice:
- Seed: 23
- pitch_std: 60
- speaking_rate: 14
- All other settings: default

Computer B (Recreation):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enter exact same settings:
- speaker: unconditional ☑
- Seed: 23
- pitch_std: 60
- speaking_rate: 14
- Randomize seed: OFF ⬜

Result: IDENTICAL VOICE!
```

**This works because:**
- Seed controls randomness
- Same seed + same parameters = same output
- Model weights are deterministic

---

## Troubleshooting

### "I set speaker to unconditional but voices sound the same"

**Check:**
- Is "Randomize Seed" ON? ✓
- Did you change the seed number if randomize is OFF?
- Are you varying other parameters (pitch_std)?
- Did you wait for new generation? (not using cached audio)

---

### "I found a great voice but can't recreate it"

**Solution:**
1. Check the seed number (shown after generation completes)
2. Write down ALL parameters used
3. Set Randomize Seed: OFF ⬜
4. Enter exact seed and parameters
5. Generate again - should be identical

**Prevention:**
- Always note seed immediately when you like a voice!
- Keep a running log

---

### "Voices sound robotic/unnatural"

**Try:**
- Increase pitch_std (try 50-70 range)
- Set emotion to unconditional ✓ (default)
- Lower CFG scale to 1.8-2.0
- Increase speaking_rate slightly
- Try different seeds

---

### "I can't find any good voices"

**Recommendations:**
1. You're probably not testing enough parameter variety
2. Try the Phase 1 workflow (test different pitch_std values)
3. Make sure speaker is unconditional ☑
4. Test at least 50-100 different seeds
5. Use consistent test phrase for fair comparison
6. Lower your standards initially, then refine

---

## Related Documentation

For more detailed information:

- **GRADIO_UI_GUIDE.md** - Complete UI parameter explanations
- **CONDITIONING_README.md** - Technical conditioning details
- **RTX5090_SETUP_SUMMARY.md** - Environment setup and troubleshooting

---

## Quick Start Template

**Copy this into Gradio to start exploring:**

```
VOICE DISCOVERY SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: [Today's date]

SETTINGS:
✓ Speaker Audio: (empty)
✓ Unconditional Keys: ☑ speaker, ☑ emotion
✓ Text: "Hello, my name is Assistant. I'm here to help you today."
✓ Language: en-us
✓ Randomize Seed: ON ✓

ROUND 1: pitch_std=40
  - Generate 10 times
  - Note favorites: [write here]

ROUND 2: pitch_std=50
  - Generate 10 times
  - Note favorites: [write here]

ROUND 3: pitch_std=60
  - Generate 10 times
  - Note favorites: [write here]

WINNER: pitch_std=___
NOW: Lock seed, fine-tune!
```

---

**Happy voice hunting!** 🎙️

Remember: The perfect voice is out there - it just takes a bit of systematic exploration to find it!

**Last Updated:** January 4, 2026
