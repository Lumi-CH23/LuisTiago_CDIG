import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """
    AGC adaptativo simples:
    - Mantém a média da magnitude perto de 'target'
    - Ajusta 'gain' lentamente para evitar saturação/oscilações
    """

    def __init__(self, target=0.7, alpha=0.001, beta=0.01):
        gr.sync_block.__init__(
            self,
            name='agc_adapt',
            in_sig=[np.complex64],
            out_sig=[np.complex64],
        )
        # Parâmetros
        self.target = float(target)  # amplitude alvo (~0.7)
        self.alpha = float(alpha)    # velocidade de ajustamento do ganho
        self.beta = float(beta)      # velocidade de média da magnitude

        # Estado interno
        self.avg_mag = 0.0
        self.gain = 1.0

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        for i, s in enumerate(x):
            mag = abs(s)

            # média exponencial da magnitude |x|
            self.avg_mag = (1.0 - self.beta) * self.avg_mag + self.beta * mag

            if self.avg_mag > 1e-6:
                # erro entre o alvo e a média atual
                err = self.target / self.avg_mag
                # atualiza ganho de forma suave
                self.gain = (1.0 - self.alpha) * self.gain + self.alpha * err

            # limitar o ganho para não explodir
            self.gain = max(0.01, min(self.gain, 100.0))

            # aplica o ganho
            y[i] = s * self.gain

        return len(y)
