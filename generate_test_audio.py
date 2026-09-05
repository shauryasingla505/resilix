import wave
import struct

# Create a 2-second dummy WAV file
with wave.open("sample_emergency.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    for _ in range(44100 * 2):
        f.writeframes(struct.pack('h', 0))

print("[+] sample_emergency.wav generated successfully!")