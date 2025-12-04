import threading
import time
import math

# apanhar o objeto do flowgraph (top block) passado a este snippet
_locals = locals()
tb = list(_locals.values())[0] if _locals else None


# THREAD 1: Sweep de Frequências


def wifi_sweep_thread():
    """
    Varrimento automático da lista freq_list.
    Atualiza current_freq (LO do Pluto) e imprime a potência média.
    """

    while True:
        try:
            freq_list = tb.freq_list
            idx = int(tb.freq_index)
        except Exception as e:
            print("Erro a ler variáveis de frequência:", e)
            time.sleep(0.5)
            continue

        if not freq_list:
            time.sleep(0.5)
            continue

        # frequência atual
        freq = freq_list[idx]

        # atualizar variável usada no Pluto LO
        try:
            tb.set_current_freq(freq)
        except Exception as e:
            print("Erro em set_current_freq:", e)

        # medir potência global (Probe ligado ao Complex to Mag^2)
        try:
            power = tb.blocks_probe_signal_x_1.level()
        except Exception as e:
            print("Erro a ler probe de potência:", e)
            power = 0.0

        print(f"[SWEEP] freq={freq/1e9:.3f} GHz  power={power:.4f}")

        # próximo canal
        idx = (idx + 1) % len(freq_list)
        try:
            tb.set_freq_index(idx)
        except Exception as e:
            print("Erro em set_freq_index:", e)

        time.sleep(0.3)



# THREAD 2: Threshold Automático do Sync Short


def auto_threshold_thread():
    """
    Calcula limiar 'thr' adaptativo para o WiFi Sync Short,
    usando a saída do Divide (probe blocks_probe_signal_x_1_0).
    thr = média + k * desvio_padrão (estimados exponencialmente).
    """

    alpha = 0.02   # rapidez de adaptação
    k = 3.0        # quantos desvios acima da média

    mean = 0.0
    var = 0.0

    while True:
        try:
            x = tb.blocks_probe_signal_x_1_0.level()
        except Exception as e:
            print("Erro a ler probe_corr:", e)
            x = 0.0

        # média e variância exponencial
        mean = (1.0 - alpha) * mean + alpha * x
        diff = x - mean
        var = (1.0 - alpha) * var + alpha * (diff * diff)
        std = math.sqrt(max(var, 1e-12))

        new_thr = mean + k * std

        try:
            tb.set_thr(new_thr)
        except Exception as e:
            print("Erro em set_thr:", e)

        # debug opcional:
        # print(f"[THR] mean={mean:.4f} std={std:.4f} thr={new_thr:.4f}")

        time.sleep(0.02)


# Arrancar as duas threads


t1 = threading.Thread(target=wifi_sweep_thread)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=auto_threshold_thread)
t2.daemon = True
t2.start()
def wifi_sweep_thread():
    """
    Varrimento automático da lista freq_list.
    Fica mais tempo parado na frequência quando deteta Wi-Fi,
    para permitir apanhar mais frames / bits.
    """

    # tempos de espera (em segundos)
    hold_no_wifi = 0.3   # quando não há Wi-Fi
    hold_wifi    = 2.0   # quando há Wi-Fi (fica parado aqui)

    # limiar de potência para dizer "há Wi-Fi"
    wifi_power_thr = 0.0005   # podes afinar mais tarde

    while True:
        try:
            freq_list = tb.freq_list
            idx = int(tb.freq_index)
        except Exception as e:
            print("Erro a ler variáveis de frequência:", e)
            time.sleep(0.5)
            continue

        if not freq_list:
            time.sleep(0.5)
            continue

        # frequência atual
        freq = freq_list[idx]

        # atualizar variável usada no Pluto LO
        try:
            tb.set_current_freq(freq)
        except Exception as e:
            print("Erro em set_current_freq:", e)

        # medir potência global (Probe ligado ao Complex to Mag^2)
        try:
            power = tb.blocks_probe_signal_x_1.level()
        except Exception as e:
            print("Erro a ler probe de potência:", e)
            power = 0.0

        print(f"[SWEEP] freq={freq/1e9:.3f} GHz  power={power:.4f}")

        # decidir quanto tempo ficar aqui e se mudamos de canal
        if power > wifi_power_thr:
            # Há Wi-Fi → NÃO muda de canal, só espera mais tempo
            time.sleep(hold_wifi)
        else:
            # Não há Wi-Fi → passa já ao próximo canal
            idx = (idx + 1) % len(freq_list)
            try:
                tb.set_freq_index(idx)
            except Exception as e:
                print("Erro em set_freq_index:", e)

            time.sleep(hold_no_wifi)