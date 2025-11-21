import numpy as np

class MeioDeComunicacao:
    def transmitir(self, sinal, sigma):
        """
        Aplica ruído gaussiano ao sinal.
        Sigma (σ) é o desvio padrão do ruído.
        """
        if sigma > 0:
            ruido = np.random.normal(0, sigma, len(sinal))
            return sinal + ruido
        return sinal