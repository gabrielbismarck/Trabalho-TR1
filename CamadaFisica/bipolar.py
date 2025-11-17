import numpy as np
import matplotlib.pyplot as plt

def codificador_bipolar(bits, amostras_por_bit=50):
    bits = np.array(bits, dtype=int)
    sinal = []

    ultimo_pulso = -1

    for bit in bits:
        if bit == 1:
            ultimo_pulso = -ultimo_pulso
            sinal.extend([ultimo_pulso] * amostras_por_bit)
        else:
            sinal.extend([0.0] * amostras_por_bit)

    return np.array(sinal)

def decodificador_bipolar(sinal, amostras_por_bits=50):

    sinal = np.array(sinal, dtype=float)
    n_bits = len(sinal) // amostras_por_bits

    bits = []

    for i in range(n_bits):
        bloco = sinal[i * amostras_por_bits:(i + 1) * amostras_por_bits]
        
        media = bloco.mean()

        if abs(media) < 0.1:
            bits.append(0)
        else:
            bits.append(1)

    return np.array(bits)

def plotagem_bipolar(bits, amostras_por_bit=50):
    sinal = codificador_bipolar(bits, amostras_por_bit)

    plt.figure(figsize=(10, 3))
    plt.plot(sinal)
    plt.title("Bipolar")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()