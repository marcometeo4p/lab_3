import numpy as np
import soundcard as sc

speakers = sc.all_speakers()
print("Speaker disponibili: ", speakers, "\n")
default_speaker = sc.default_speaker()
print(f"Speaker selezionato: {default_speaker}\n")

mics = sc.all_microphones()
print("Microfoni disponibili: ", mics, "\n")
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
  normalized_data=normalized_data[::2]
  default_speaker.play(normalized_data, samplerate=samplerate)
else:
  print(
      "L'audio registrato è completamente silenzioso (nessun picco rilevato)."
  )

import matplotlib.pyplot as plt
# Assumendo che 'data' sia già stato acquisito e 'samplerate = 48000'

if data.ndim > 1:
  audio_signal = data[:, 0]
else:
  audio_signal = data

duration = len(audio_signal) / samplerate
time_axis = np.linspace(0, duration, len(audio_signal))

plt.figure(figsize=(10, 4))
plt.plot(time_axis, audio_signal, color='b', alpha=0.6)
plt.title('Segnale Audio nel Dominio del Tempo')
plt.xlabel('Tempo (secondi)')
plt.ylabel('Ampiezza')
plt.grid(True)
plt.xlim(0, duration)
plt.savefig("audio_plot.png")
plt.show(block=False)

time_axis = np.linspace(0, duration/2, len(audio_signal))

plt.figure(figsize=(10, 4))
plt.plot(time_axis, audio_signal, color='b', alpha=0.6)
plt.title('Segnale Audio (x2)')
plt.xlabel('Tempo (secondi)')
plt.ylabel('Ampiezza')
plt.grid(True)
plt.xlim(0, duration/2)
plt.savefig("audio_plot_2x.png")
plt.show(block=False)