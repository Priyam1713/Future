import array
import math
from pathlib import Path
import wave

root = Path(__file__).resolve().parents[1]
original = root / "fate/web/public/art/fate_ambient_loop.wav"
output = original.with_name("fate-ambient-v2.wav")
with wave.open(str(original), "rb") as wav:
    assert wav.getsampwidth() == 2
    channels, rate = wav.getnchannels(), wav.getframerate()
    data = array.array("h", wav.readframes(wav.getnframes()))
fade = min(rate // 2, len(data) // (channels * 4))
seam = []
for i in range(fade):
    mix = .5 - .5 * math.cos(math.pi * i / (fade - 1))
    for channel in range(channels):
        seam.append(data[len(data) - fade * channels + i * channels + channel] * (1 - mix) +
                    data[i * channels + channel] * mix)
samples = list(data[fade * channels:-fade * channels]) + seam
rms = math.sqrt(sum(x*x for x in samples) / len(samples))
gain = min(10 ** (-20/20) * 32767 / rms, 30000 / max(abs(x) for x in samples))
with wave.open(str(output), "wb") as wav:
    wav.setparams((channels, 2, rate, 0, "NONE", "not compressed"))
    wav.writeframes(array.array("h", (round(x * gain) for x in samples)).tobytes())
print(f"Loop remaster: {len(samples)/channels/rate:.2f}s, RMS {(20*math.log10(rms*gain/32767)):.1f} dBFS")
