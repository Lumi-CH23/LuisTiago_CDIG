import csv
from collections import defaultdict
import matplotlib.pyplot as plt

LOG_FILE = "wifi_scan_log.csv"

sum_power = defaultdict(float)
count = defaultdict(int)

with open(LOG_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        is_24 = int(row["is_24"])
        if not is_24:
            continue

        freq = float(row["freq_hz"])
        power = float(row["power"])

        sum_power[freq] += power
        count[freq] += 1

freqs = sorted(sum_power.keys())
avg_power = [sum_power[f] / count[f] for f in freqs]

def freq_to_chan(freq_hz):
    table = {
        2412000000.0: 1,
        2437000000.0: 6,
        2462000000.0: 11,
    }
    return table.get(freq_hz, "?")

labels = [f"ch {freq_to_chan(f)}\n{f/1e9:.3f} GHz" for f in freqs]

plt.figure(figsize=(8, 4))
plt.bar(range(len(freqs)), avg_power)
plt.xticks(range(len(freqs)), labels)
plt.ylabel("Potência média (|s|^2)")
plt.title("Ocupação dos canais Wi-Fi (2.4 GHz)")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
