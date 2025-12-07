import numpy as np
import matplotlib.pyplot as plt

# ler o CSV, ignorando o cabeçalho
data = np.loadtxt("wifi_scan_log.csv", delimiter=",", skiprows=1)

# colunas: timestamp, freq_hz, power, thr, is_24, wifi_hit
timestamps = data[:, 0]
freqs_hz   = data[:, 1]
powers     = data[:, 2]

# vamos tratar cada linha como um "instante" (índice)
N = len(timestamps)
time_idx = np.arange(N)

# frequências únicas (os canais do sweep)
unique_freqs = np.unique(freqs_hz)
F = len(unique_freqs)

# matriz [freq_index, time_index]
heat = np.zeros((F, N))

for j in range(N):
    f = freqs_hz[j]
    p = powers[j]
    i = np.where(unique_freqs == f)[0][0]
    heat[i, j] = p

plt.figure(figsize=(10, 4))

# mostrar em GHz no eixo Y
extent = [0, N, unique_freqs[0] / 1e9, unique_freqs[-1] / 1e9]

plt.imshow(
    heat,
    aspect='auto',
    origin='lower',
    extent=extent,
    interpolation='nearest',
    cmap='jet'
)

plt.colorbar(label="Potência (|s|²)")
plt.xlabel("Índice de amostra (tempo)")
plt.ylabel("Frequência (GHz)")
plt.title("Heatmap do sweep Wi-Fi (PlutoSDR)")

plt.tight_layout()
plt.show()
