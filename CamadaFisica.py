import numpy as np
import matplotlib.pyplot as plt

# =========================== NRZ POLAR ===========================
def codificador_nrz_polar(bits, amostras_por_bit=10):
    bits = np.array(bits, dtype=int)
    niveis = np.where(bits == 1, 1.0, -1.0)
    sinal = np.repeat(niveis, amostras_por_bit)
    return sinal


def decodificador_nrz_polar(sinal, amostras_por_bit=10):
    sinal = np.array(sinal, dtype=float)
    n_bits = len(sinal) // amostras_por_bit

    blocos = sinal[:n_bits * amostras_por_bit].reshape(n_bits, amostras_por_bit)
    bits = (blocos.mean(axis=1) > 0).astype(int)

    return bits

# vizualização

def plotagem_nrz(bits, amostras_por_bit=10):
    sinal = codificador_nrz_polar(bits, amostras_por_bit)

    plt.figure(figsize=(10, 3))
    plt.plot(sinal)
    plt.title("NRZ-Polar")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# =========================== MANCHESTER ===========================
def codificador_manchester(bits, amostras_por_bit=10):
    bits = np.array(bits, dtype=int)
    meio = amostras_por_bit // 2
    sinal = []

    for bit in bits:
        # Se o bit for 1, o sinal vai ser 1.0, 1.0, -1.0, -1.0
        if bit == 1:
            sinal.extend([1.0] * meio )
            sinal.extend([-1.0] * meio )
        # Se o bit for 0, o sinal vai ser -1.0, -1.0, 1.0, 1.0
        else:
            sinal.extend([ -1.0 ] * meio)
            sinal.extend([ 1.0 ] * meio)

    return np.array(sinal)

def decodificador_manchester(sinal, amostras_por_bit=10):
    sinal = np.array(sinal, dtype=float)
    meio = amostras_por_bit // 2
    n_bits = len(sinal) // amostras_por_bit

    bits = []

    for i in range(n_bits):
        bloco = sinal[i * amostras_por_bit:(i + 1) * amostras_por_bit]
        primeira_metade = bloco[:meio]
        bits.append(1 if primeira_metade.mean() > 0 else 0)

    return np.array(bits)

def plotagem_manchester(bits, amostras_por_bit=10):
    sinal = codificador_manchester(bits, amostras_por_bit)

    plt.figure(figsize=(10, 3))
    plt.plot(sinal)
    plt.title("Manchester")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ============================ BIPOLAR =============================
def codificador_bipolar(bits, amostras_por_bit=10):
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

def decodificador_bipolar(sinal, amostras_por_bit=10):

    sinal = np.array(sinal, dtype=float)
    n_bits = len(sinal) // amostras_por_bit

    bits = []

    for i in range(n_bits):
        bloco = sinal[i * amostras_por_bit:(i + 1) * amostras_por_bit]
        
        media = bloco.mean()

        if abs(media) < 0.1:
            bits.append(0)
        else:
            bits.append(1)

    return np.array(bits)

def plotagem_bipolar(bits, amostras_por_bit=10):
    sinal = codificador_bipolar(bits, amostras_por_bit)

    plt.figure(figsize=(10, 3))
    plt.plot(sinal)
    plt.title("Bipolar")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ==================================================================
#                           ANALÓGICOS
# ==================================================================

# ================== AMPLITUDE SHIFT KEYING (ASK) ==================
def modulador_ask(bits, fc=2000, A_1 = 1.0, A_0 = 0.0, amostras_por_bit=10):
    bits = np.array(bits, dtype=int)
    
    # cria um array t de números começanmdo em 0 e indo ate 1 (0 <= x < 1)com 50 = [amostras_por_bit] amostras
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    sinal = []

    for bit in bits:
        if bit == 1:
            A = A_1  
        else:
            A = A_0

        # gera a portadora no trecho de tempo com a amplitude A
        portadora = A * np.sin(2 * np.pi *fc * t)
        sinal.extend(portadora)

    return np.array(sinal)

def demodulador_ask(sinal, fc=2000, amostras_por_bit=10):
    # cria um array t de números começanmdo em 0 e indo ate 1 (0 <= x < 1)com 50 = [amostras_por_bit] amostras
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    
    # formula da onda portadora de referência
    portadora = np.sin(2 * np.pi *fc * t)

    # Calcula quantos bits tem no sinal modulado
    n_bits = len(sinal) // amostras_por_bit
    
    bits = []

    for i in range(n_bits):
        # pega cada bloco ou trecho do sinal e calcula a correlação. sinal[inicio:fim]
        bloco = sinal[i * amostras_por_bit:(i + 1) * amostras_por_bit]
        correlacao = np.sum(bloco * portadora)

        # Se a correlação for maior que zero, o bit é 1, isto significa que os sinais estão em fase
        # caso contrário, o bit é 0, isto significa que os sinais estao fora de fase
        if correlacao > 0:
            bits.append(1)
        else:
            bits.append(0)

    return np.array(bits)

# ================== FREQUENCY SHIFT KEYING (FSK) ==================
def modulador_fsk(bits, f_1 = 1000, f_0 = 2000, amostras_por_bit=10):
    bits = np.array(bits, dtype=int)
    
    # cria um array t de números commencendo em 0 e indo ate 1 (0 <= x < 1)com 50 = [amostras_por_bit] amostras
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    sinal = []

    for bit in bits:
        if bit == 1:
            f = f_1
        else:
            f = f_0

        portadora = np.sin(2 * np.pi * f * t)
        sinal.extend(portadora)

    return np.array(sinal)

def demodulador_fsk (sinal, f_1 = 1000, f_0 = 2000, amostras_por_bit=10):
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    portadora_0 = np.sin(2 * np.pi * f_0 * t)
    portadora_1 = np.sin(2 * np.pi * f_1 * t)

    n_bits = len(sinal) // amostras_por_bit

    bits = []

    for i in range(n_bits):
        bloco = sinal[i * amostras_por_bit:(i + 1) * amostras_por_bit]
        correlacao_0 = np.sum(bloco * portadora_0)
        correlacao_1 = np.sum(bloco * portadora_1)

        if correlacao_0 > correlacao_1:
            bits.append(0)
        else:
            bits.append(1)

    return np.array(bits)

# ================== QUADRATURE PHASE SHIFT KEYING (QPSK) ==========
mapa_fase_qpsk = {
    (0, 0): np.pi / 4,   # 45°
    (0, 1): 3*np.pi / 4, # 135°
    (1, 1): 5*np.pi / 4, # 225°
    (1, 0): 7*np.pi / 4  # 315°
}

def  modulador_qpsk(bits, fc=2000, amostras_por_bit=10):
    bits = np.array(bits, dtype=int)

    # Garante que o número de bits seja multiplo de 2
    if len(bits) % 2 != 0:
        bits = np.append(bits, [0])
    
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    sinal = []

    for i in range(0, len(bits), 2):
        par = (bits[i], bits[i + 1])
        fase = mapa_fase_qpsk[par]
        portadora = np.sin(2 * np.pi * fc * t + fase)
        sinal.extend(portadora)

    return np.array(sinal)

def demodulador_qpsk(sinal, fc=2000, amostras_por_simbolo=50):
    # Preciso implemenar corretamente
    # Gera vetor de tempo
    t = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
    
    # Verifica quantos símbolos existem no sinal
    n_simbolos = len(sinal) // amostras_por_simbolo
    bits = []

    ref = {
        (0, 0): np.sin(2*np.pi*fc*t + np.pi/4),      # 45°
        (0, 1): np.sin(2*np.pi*fc*t + 3*np.pi/4),    # 135°
        (1, 1): np.sin(2*np.pi*fc*t + 5*np.pi/4),    # 225°
        (1, 0): np.sin(2*np.pi*fc*t + 7*np.pi/4)     # 315°
    }
    
    for i in range(n_simbolos):
        bloco = sinal[i * amostras_por_simbolo:(i + 1) * amostras_por_simbolo]

        melhor_correlacao = None
        melhor_bits = None

        for bits_ref, onda_ref in ref.items():
            # semelhança sinal recebido e sinal de referência
            correlacao = np.sum(bloco * onda_ref)

            if melhor_correlacao is None or correlacao > melhor_correlacao:
                melhor_correlacao = correlacao
                melhor_bits = bits_ref

        bits.extend(melhor_bits)

    return np.array(bits)

# ================== QUADRATURE AMPLITUDE MODULATION (16-QAM) ======
mapa_16qam = {
    (0,0,0,0): (-3,  3),
    (0,0,0,1): (-1,  3),
    (0,0,1,1): ( 1,  3),
    (0,0,1,0): ( 3,  3),

    (0,1,0,0): (-3,  1),
    (0,1,0,1): (-1,  1),
    (0,1,1,1): ( 1,  1),
    (0,1,1,0): ( 3,  1),

    (1,1,0,0): (-3, -1),
    (1,1,0,1): (-1, -1),
    (1,1,1,1): ( 1, -1),
    (1,1,1,0): ( 3, -1),

    (1,0,0,0): (-3, -3),
    (1,0,0,1): (-1, -3),
    (1,0,1,1): ( 1, -3),
    (1,0,1,0): ( 3, -3),
}

def modulador_16qam(bits, fc=2000, amostras_por_simbolo=50):
    bits = np.array(bits, dtype=int)

    t = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
    sinal = []

    # Garante que o número de bits seja multiplo de 4, caso na seja, adiciona um 0 até ser
    while len(bits) % 4 != 0:
        bits = np.append(bits, 0)
    
    # Percorre o vetor de bits de 4 em 4. Cada bloco é um símbolo 16-QAM
    for i in range(0, len(bits), 4):
        # Tranforma o bloco em tupla para usar como chave no mapa
        bloco = tuple(bits[i:i + 4])
        # Obtem o par I, Q com as chaves obtidas no mapa
        I, Q = mapa_16qam[bloco]

        # Gera as portadoras
        portadora_I = I * np.cos(2 * np.pi * fc * t)
        portadora_Q = Q * np.sin(2 * np.pi * fc * t)

        # Gera o sinal como soma das portadoras IQ
        s = portadora_I + portadora_Q

        sinal.extend(s)

    return np.array(sinal)

def demodulador_16qam(sinal, fc=2000, amostras_por_simbolo=50):
    # Preciso implementar corretamente
    t = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
    n_simbolos = len(sinal) // amostras_por_simbolo
    bits = []

    # Portadoras de referencia

    cos_ref = np.cos(2 * np.pi * fc * t)
    sen_ref = np.sin(2 * np.pi * fc * t)

    for i in range(n_simbolos):
        # extrai o bloco do sinal
        bloco = sinal[i * amostras_por_simbolo:(i + 1) * amostras_por_simbolo]

        # Correlação
        I_correlacao_cos = np.sum(bloco * cos_ref)
        Q_correlacao_sen = np.sum(bloco * sen_ref)

        melhor_dist = None
        melhor_bits = None

        # Percorrer os símbolos no mapa
        for bits_ref, (I_ref, Q_ref) in mapa_16qam.items():

            # Calcula a distância euclidiana entre (I_rx, Q_rx) e (I, Q) de referência
            dist = (I_correlacao_cos - I_ref)**2 + (Q_correlacao_sen - Q_ref)**2

            if melhor_dist is None or dist < melhor_dist:
                melhor_dist = dist
                melhor_bits = bits_ref

        bits.extend(melhor_bits)
                
    return np.array(bits)


class CamadaFisica:
    def __init__(self, amostras_por_bit=10):
        self.amostras_por_bit = amostras_por_bit

    def codificar_digital(self, bits, tipo):
        """
        Seleciona o codificador digital baseado na string 'tipo' vinda da GUI.
        """
        if tipo == "NRZ":
            return codificador_nrz_polar(bits, self.amostras_por_bit)
        elif tipo == "Manchester":
            return codificador_manchester(bits, self.amostras_por_bit)
        elif tipo == "Bipolar":
            return codificador_bipolar(bits, self.amostras_por_bit)
        else:
            raise ValueError(f"Modulação digital desconhecida: {tipo}")

    def decodificar_digital(self, sinal, tipo):
        """
        Seleciona o decodificador digital baseado na string 'tipo'.
        """
        if tipo == "NRZ":
            return decodificador_nrz_polar(sinal, self.amostras_por_bit)
        elif tipo == "Manchester":
            return decodificador_manchester(sinal, self.amostras_por_bit)
        elif tipo == "Bipolar":
            return decodificador_bipolar(sinal, self.amostras_por_bit)
        else:
            raise ValueError(f"Modulação digital desconhecida: {tipo}")
    
    def modular_analogico(self, bits=None, sinal_digital=None, tipo="ASK"):
        # TODO: Implementar ASK, FSK, PSK, QAM
        # Por enquanto retorna o próprio sinal digital para teste
        if tipo == "ASK":
            return modulador_ask(bits)
        elif tipo == "FSK":
            return modulador_fsk(bits)
        elif tipo == "QPSK":
            return modulador_qpsk(bits)
        elif tipo == "16QAM":
            return modulador_16qam(bits)
        
        else:
            ValueError(f"Modulação analogica desconhecida: {tipo}")

    def demodular_analogico(self, sinal_analogico, tipo):
        # TODO: Implementar ASK, FSK, PSK, QAM
        if tipo == "ASK":
            return demodulador_ask(sinal_analogico)
        elif tipo == "FSK":
            return demodulador_fsk(sinal_analogico)
        elif tipo == "QPSK":
            return demodulador_qpsk(sinal_analogico)
        elif tipo == "16QAM":
            return demodulador_16qam(sinal_analogico)
        
        else:
            ValueError(f"Modulação analogica desconhecida: {tipo}")