import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

CSV_FILE = "wifi_scan_log.csv"

# mapa freq(hz) -> canal Wi-Fi
wifi_channels = {
    2412e6: "Ch 1",
 
    2437e6: "Ch 6",
  
    2462e6: "Ch 11",
  }

fig, ax = plt.subplots(figsize=(12, 6))

im = None
cbar = None
unique_freqs = None
yticks_labels = []


def update(_frame):
    global im, cbar, unique_freqs, yticks_labels

    if not os.path.exists(CSV_FILE):
        return

    try:
        data = np.loadtxt(CSV_FILE, delimiter=",", skiprows=1)
    except Exception:
        # ficheiro a ser escrito → esperar próxima atualização
        return

    if data.size == 0:
        return

    # se só houver uma linha, np.loadtxt devolve 1D
    if data.ndim == 1:
        data = data.reshape(1, -1)

    # colunas: timestamp, freq_hz, power, thr, is_24, wifi_hit
    timestamps = data[:, 0]
    freqs_hz   = data[:, 1]
    powers     = data[:, 2]

    N = len(timestamps)
    unique_freqs = np.unique(freqs_hz)
    F = len(unique_freqs)

    heat = np.zeros((F, N))
    for j in range(N):
        f = freqs_hz[j]
        p = powers[j]
        i = np.where(unique_freqs == f)[0][0]
        heat[i, j] = p

    # construir labels de canais
    yticks_labels = []
    for f in unique_freqs:
        if f in wifi_channels:
            label = f"{wifi_channels[f]} ({f/1e9:.3f} GHz)"
        else:
            label = f"{f/1e9:.3f} GHz"
        yticks_labels.append(label)

    # primeira vez: criar imagem + colorbar
    if im is None:
        im = ax.imshow(
            heat,
            aspect='auto',
            origin='lower',
            interpolation='nearest',
            cmap='jet'
        )
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("Potência (|s|²)")
    else:
        # atualizar apenas os dados e limites
        im.set_data(heat)
        im.set_clim(vmin=np.min(heat), vmax=np.max(heat))

    ax.set_xlabel("Índice temporal (amostras do sweep)")
    ax.set_ylabel("Frequência / Canal Wi-Fi")
    ax.set_title("Heatmap em tempo quase real do sweep Wi-Fi (PlutoSDR)")

    ax.set_yticks(np.arange(F))
    ax.set_yticklabels(yticks_labels)

    # para o eixo X, mostramos só o número de amostras (0..N-1)
    ax.set_xlim(0, max(N - 1, 1))

    plt.tight_layout()


ani = FuncAnimation(fig, update, interval=1000)  # 1 atualização por segundo

plt.show()

