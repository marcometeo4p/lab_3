import numpy as np
import soundcard as sc

# Elenco e stampa dei dispositivi disponibili
speakers = sc.all_speakers()
print(f"Speaker disponibili: {speakers}\n")

default_speaker = sc.default_speaker()
print(f"Speaker selezionato: {default_speaker}\n")

mics = sc.all_microphones()
print(f"Microfoni disponibili: {mics}\n")

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
  print("Riproduzione x1.5...")
  default_speaker.play(normalized_data, samplerate=samplerate*1.5)
  print("Riproduzione x2...")
  default_speaker.play(normalized_data, samplerate=samplerate*2)
  print("indovina")
  default_speaker.play(normalized_data, samplerate=samplerate*4)
else:
  print(
      "L'audio registrato è completamente silenzioso (nessun picco rilevato)."
  )