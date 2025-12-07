import socket
import struct
import time
import os

# Caminho do FIFO (pipe)
FIFO_PATH = os.path.expanduser('~/pcap_live/wifi_pipe.pcap')

UDP_IP  = '127.0.0.1'
UDP_PORT = 5555

# Cabeçalho global PCAP - LINKTYPE_IEEE802_11 = 105
PCAP_GLOBAL_HDR = struct.pack(
    '<IHHIIII',
    0xa1b2c3d4,  # magic number
    2,           # major version
    4,           # minor version
    0,           # thiszone
    0,           # sigfigs
    65535,       # snaplen
    105          # linktype 105 = IEEE 802.11
)

def main():
    # Garante que o FIFO existe
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)

    print(f'[LOGGER] Abrir FIFO para escrita: {FIFO_PATH}')
    f = open(FIFO_PATH, 'wb', buffering=0)

    # Escrever cabeçalho global PCAP
    f.write(PCAP_GLOBAL_HDR)
    f.flush()

    # Socket UDP para receber PDUs do GNU Radio
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f'[LOGGER] À escuta em UDP {UDP_IP}:{UDP_PORT}')

    while True:
        data, _ = sock.recvfrom(65535)
        if not data:
            continue

        # DEBUG opcional
        print('[LOGGER] LEN:', len(data))

        t = time.time()
        ts_sec = int(t)
        ts_usec = int((t - ts_sec) * 1e6)
        incl_len = orig_len = len(data)

        pkt_hdr = struct.pack('<IIII', ts_sec, ts_usec, incl_len, orig_len)
        f.write(pkt_hdr + data)

if __name__ == '__main__':
    main()

