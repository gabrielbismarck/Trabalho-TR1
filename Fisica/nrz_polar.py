"""
@name: CamadaFisica
@file: CamadaFisica.py
@author: Gabriel Bismarck
@date: 2022-04-17
@version: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt

# Codificação banda base

def codificador_nrz_polar(bits, amostras_por_bit=50):
    bits = np.array(bits, dtype=int)
    niveis = np.where(bits == 1, 1.0, -1.0)
    sinal = np.repeat(niveis, amostras_por_bit)
    return sinal


def decodificador_nrz_polar(sinal, amostras_por_bit=50):
    sinal = np.array(sinal, dtype=float)
    n_bits = len(sinal) // amostras_por_bit

    blocos = sinal[:n_bits * amostras_por_bit].reshape(n_bits, amostras_por_bit)
    bits = (blocos.mean(axis=1) > 0).astype(int)

    return bits

# vizualização

def plotagem_nrz(bits, amostras_por_bit=50):
    sinal = codificador_nrz_polar(bits, amostras_por_bit)

    plt.figure(figsize=(10, 3))
    plt.plot(sinal)
    plt.title("NRZ-Polar")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()