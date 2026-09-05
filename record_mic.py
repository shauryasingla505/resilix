import sounddevice as sd
from scipy.io.wavfile import write

sample_rate = 16000  # 16kHz matches Whisper's expected sample rate
duration = 8          # Record for 8 seconds

print("[*] Recording starting in 1 second... Speak your emergency message clearly!")
sd.sleep(1000)

print("[>>>] RECORDING NOW... (Speak into your mic)")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished

write("sample_emergency.wav", sample_rate, recording)
print("[+] Recording saved as 'sample_emergency.wav'!")