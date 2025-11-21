import numpy as np
import matplotlib.pyplot as plt

def codificador_manchester(bits, amostras_por_bit=50):
    bits = np.array(bits, dtype=int)
    meio = amostras_por_bit // 2
    sinal = []

    for bit in bits:
        if bit == 1:
            sinal.extend([1.0] * meio )
            sinal.extend([-1.0] * meio )
        else:
            sinal.extend([ -1.0 ] * meio)
            sinal.extend([ 1.0 ] * meio)

    return np.array(sinal)

def decodificador_manchester(sinal, amostras_por_bit=50):
    sinal = np.array(sinal, dtype=float)
    meio = amostras_por_bit // 2
    n_bits = len(sinal) // amostras_por_bit

    bits = []

    for i in range(n_bits):
        bloco = sinal[i * amostras_por_bit:(i + 1) * amostras_por_bit]
        primeira_metade = bloco[:meio]
        bits.append(1 if primeira_metade.mean() > 0 else 0)

    return np.array(bits)

def plotagem_manchester(bits, amostras_por_bit=50):
    sinal = codificador_manchester(bits, amostras_por_bit)

    plt.figure(figsize=(10, 3))
    plt.plot(sinal)
    plt.title("Manchester")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()