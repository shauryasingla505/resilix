import pyttsx3

engine = pyttsx3.init()
emergency_script = (
    "Help! Help! Emergency! There is a huge fire near the main bus stand in Vellore. "
    "Smoke is spreading rapidly and people are trapped inside. Send help immediately!"
)

print("[*] Generating speech sample...")
engine.save_to_file(emergency_script, "sample_emergency.wav")
engine.runAndWait()
print("[+] Created clean 'sample_emergency.wav'!")