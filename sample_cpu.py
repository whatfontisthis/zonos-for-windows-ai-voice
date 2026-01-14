import torch
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

# Force CPU usage to avoid RTX 5090 compatibility issue
device = torch.device("cpu")

print("Loading model on CPU (this may take a moment)...")
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

print("Loading example audio...")
wav, sampling_rate = torchaudio.load("assets/exampleaudio.mp3")
speaker = model.make_speaker_embedding(wav, sampling_rate)

torch.manual_seed(421)

print("Generating speech...")
cond_dict = make_cond_dict(text="Hello, world!", speaker=speaker, language="en-us")
conditioning = model.prepare_conditioning(cond_dict)

codes = model.generate(conditioning)

print("Decoding audio...")
wavs = model.autoencoder.decode(codes).cpu()
torchaudio.save("sample_cpu.wav", wavs[0], model.autoencoder.sampling_rate)

print("Done! Audio saved to sample_cpu.wav")
