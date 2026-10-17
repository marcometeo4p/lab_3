import numpy as np
import soundcard as sc

default_speaker = sc.default_speaker()
print(f"Speaker selezionato: {default_speaker}\n")

default_mic = sc.default_microphone()
print(f"Microfono selezionato: {default_mic}\n")

# Acquisizione di 1 secondo di audio (48000 frame a 48kHz)
samplerate = 48000
numframes = 480000
print("Registrazione in corso...")
data = default_mic.record(samplerate=samplerate, numframes=numframes)
print("Array acquisito:")
print(data)
print(f"\nL'array dei dati registrati è lungo {len(data)}\n")

# Riproduzione sicura dei dati
max_val = np.max(np.abs(data))
if max_val > 0:
  normalized_data = data / max_val
  print("Riproduzione in corso...")
  default_speaker.play(normalized_data, samplerate=samplerate)
else:
  print(
      "L'audio registrato è completamente silenzioso (nessun picco rilevato)."
  )