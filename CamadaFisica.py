import numpy as np
import matplotlib.pyplot as plt

# =========================== NRZ POLAR ===========================
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

def plotagem_nrz(bits, amostras_por_bit=50):
    sinal = codificador_nrz_polar(bits, amostras_por_bit)
    plt.plot(sinal)
    plt.show()

# =========================== MANCHESTER ===========================
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
    plt.plot(sinal)
    plt.show()

# ============================ BIPOLAR =============================
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

def decodificador_bipolar(sinal, amostras_por_bit=50):
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

def plotagem_bipolar(bits, amostras_por_bit=50):
    sinal = codificador_bipolar(bits, amostras_por_bit)
    plt.plot(sinal)
    plt.show()

# ==================================================================
#                           ANALÓGICOS
#       NOTA: Alterei as frequências (fc) para valores baixos 
#       (1, 2, 4) para caberem dentro de 50 amostras sem Aliasing.
# ==================================================================

# ================== AMPLITUDE SHIFT KEYING (ASK) ==================
def modulador_ask(bits, fc=1, A_1 = 1.0, A_0 = 0.0, amostras_por_bit=50):
    # fc=1 significa 1 ciclo completo por bit (onda perfeita para visualização)
    bits = np.array(bits, dtype=int)
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    sinal = []
    for bit in bits:
        A = A_1 if bit == 1 else A_0
        portadora = A * np.sin(2 * np.pi * fc * t)
        sinal.extend(portadora)
    return np.array(sinal)

def demodulador_ask(sinal, fc=1, amostras_por_bit=50):
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    portadora = np.sin(2 * np.pi * fc * t)
    n_bits = len(sinal) // amostras_por_bit
    bits = []
    for i in range(n_bits):
        bloco = sinal[i * amostras_por_bit:(i + 1) * amostras_por_bit]
        correlacao = np.sum(bloco * portadora)
        bits.append(1 if correlacao > 0 else 0)
    return np.array(bits)

# ================== FREQUENCY SHIFT KEYING (FSK) ==================
def modulador_fsk(bits, f_1=2, f_0=1, amostras_por_bit=50):
    # f_0 = 1 ciclo por bit, f_1 = 2 ciclos por bit
    bits = np.array(bits, dtype=int)
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    sinal = []
    for bit in bits:
        f = f_1 if bit == 1 else f_0
        portadora = np.sin(2 * np.pi * f * t)
        sinal.extend(portadora)
    return np.array(sinal)

def demodulador_fsk(sinal, f_1=2, f_0=1, amostras_por_bit=50):
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    portadora_0 = np.sin(2 * np.pi * f_0 * t)
    portadora_1 = np.sin(2 * np.pi * f_1 * t)
    
    n_bits = len(sinal) // amostras_por_bit
    bits = []
    for i in range(n_bits):
        bloco = sinal[i * amostras_por_bit:(i + 1) * amostras_por_bit]
        correlacao_0 = np.sum(bloco * portadora_0)
        correlacao_1 = np.sum(bloco * portadora_1)
        # Quem tiver maior correlação "ganha"
        bits.append(0 if correlacao_0 > correlacao_1 else 1)
    return np.array(bits)

# ================== QUADRATURE PHASE SHIFT KEYING (QPSK) ==========
mapa_fase_qpsk = {
    (0, 0): np.pi / 4,   # 45°
    (0, 1): 3*np.pi / 4, # 135°
    (1, 1): 5*np.pi / 4, # 225°
    (1, 0): 7*np.pi / 4  # 315°
}

def modulador_qpsk(bits, fc=1, amostras_por_bit=50):
    bits = np.array(bits, dtype=int)
    if len(bits) % 2 != 0:
        bits = np.append(bits, [0])
    
    t = np.linspace(0, 1, amostras_por_bit, endpoint=False)
    sinal = []
    
    # Processa 2 bits por vez (1 símbolo)
    for i in range(0, len(bits), 2):
        par = (bits[i], bits[i + 1])
        fase = mapa_fase_qpsk[par]
        portadora = np.sin(2 * np.pi * fc * t + fase)
        sinal.extend(portadora)
    return np.array(sinal)

def demodulador_qpsk(sinal, fc=1, amostras_por_simbolo=50):
    t = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
    n_simbolos = len(sinal) // amostras_por_simbolo
    bits = []

    # Cria as 4 ondas de referência possíveis
    ref = {
        (0, 0): np.sin(2*np.pi*fc*t + np.pi/4),
        (0, 1): np.sin(2*np.pi*fc*t + 3*np.pi/4),
        (1, 1): np.sin(2*np.pi*fc*t + 5*np.pi/4),
        (1, 0): np.sin(2*np.pi*fc*t + 7*np.pi/4)
    }
    
    for i in range(n_simbolos):
        bloco = sinal[i * amostras_por_simbolo:(i + 1) * amostras_por_simbolo]
        melhor_correlacao = -float('inf')
        melhor_bits = None

        # Compara o bloco recebido com as 4 referências
        for bits_ref, onda_ref in ref.items():
            correlacao = np.sum(bloco * onda_ref)
            if correlacao > melhor_correlacao:
                melhor_correlacao = correlacao
                melhor_bits = bits_ref
        
        bits.extend(melhor_bits)
    return np.array(bits)

# ================== QUADRATURE AMPLITUDE MODULATION (16-QAM) ======
mapa_16qam = {
    (0,0,0,0): (-3,  3), (0,0,0,1): (-1,  3), (0,0,1,1): ( 1,  3), (0,0,1,0): ( 3,  3),
    (0,1,0,0): (-3,  1), (0,1,0,1): (-1,  1), (0,1,1,1): ( 1,  1), (0,1,1,0): ( 3,  1),
    (1,1,0,0): (-3, -1), (1,1,0,1): (-1, -1), (1,1,1,1): ( 1, -1), (1,1,1,0): ( 3, -1),
    (1,0,0,0): (-3, -3), (1,0,0,1): (-1, -3), (1,0,1,1): ( 1, -3), (1,0,1,0): ( 3, -3),
}

def modulador_16qam(bits, fc=1, amostras_por_simbolo=50):
    bits = np.array(bits, dtype=int)
    t = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
    sinal = []

    while len(bits) % 4 != 0:
        bits = np.append(bits, 0)
    
    for i in range(0, len(bits), 4):
        bloco = tuple(bits[i:i + 4])
        I, Q = mapa_16qam[bloco]
        
        # Modulação em Quadratura
        portadora_I = I * np.cos(2 * np.pi * fc * t)
        portadora_Q = Q * np.sin(2 * np.pi * fc * t)
        sinal.extend(portadora_I - portadora_Q) # Sinal final
        
    return np.array(sinal)

def demodulador_16qam(sinal, fc=1, amostras_por_simbolo=50):
    t = np.linspace(0, 1, amostras_por_simbolo, endpoint=False)
    n_simbolos = len(sinal) // amostras_por_simbolo
    bits = []

    # Ondas base de referência (Cosseno e Seno)
    cos_ref = np.cos(2 * np.pi * fc * t)
    sin_ref = np.sin(2 * np.pi * fc * t) # Note o sinal negativo na geração acima, ou ajuste aqui

    # Fator de normalização: A soma de (cos^2) ao longo de um período é N/2.
    # Precisamos dividir por N/2 para recuperar a amplitude original (1 ou 3).
    fator_norm = 2 / amostras_por_simbolo 

    for i in range(n_simbolos):
        bloco = sinal[i * amostras_por_simbolo:(i + 1) * amostras_por_simbolo]

        # Correlação para extrair I e Q aproximados
        # Se modulamos como (I*cos - Q*sin), demodulamos projetando:
        I_estimado = np.sum(bloco * cos_ref) * fator_norm
        Q_estimado = np.sum(bloco * sin_ref) * fator_norm * (-1) # Ajuste de sinal se necessário
        
        # Como o modulador fez (portadora_I - portadora_Q), sendo Q*sin...
        # Vamos simplificar: I*cos - Q*sin.
        # <Sinal, cos> = I * <cos, cos> = I * (N/2) -> I = Corr * 2/N
        # <Sinal, sin> = -Q * <sin, sin> = -Q * (N/2) -> Q = -Corr * 2/N
        
        Q_estimado = np.sum(bloco * np.sin(2 * np.pi * fc * t)) * fator_norm * (-1)

        melhor_dist = float('inf')
        melhor_bits = None

        # Distância Euclidiana para achar o ponto mais próximo na constelação
        for bits_ref, (I_ref, Q_ref) in mapa_16qam.items():
            dist = (I_estimado - I_ref)**2 + (Q_estimado - Q_ref)**2
            if dist < melhor_dist:
                melhor_dist = dist
                melhor_bits = bits_ref

        bits.extend(melhor_bits)
                
    return np.array(bits)


class CamadaFisica:
    def __init__(self, amostras_por_bit=50):
        self.amostras_por_bit = amostras_por_bit

    def codificar_digital(self, bits, tipo):
        if tipo == "NRZ":
            return codificador_nrz_polar(bits, self.amostras_por_bit)
        elif tipo == "Manchester":
            return codificador_manchester(bits, self.amostras_por_bit)
        elif tipo == "Bipolar":
            return codificador_bipolar(bits, self.amostras_por_bit)
        else:
            raise ValueError(f"Modulação digital desconhecida: {tipo}")

    def decodificar_digital(self, sinal, tipo):
        if tipo == "NRZ":
            return decodificador_nrz_polar(sinal, self.amostras_por_bit)
        elif tipo == "Manchester":
            return decodificador_manchester(sinal, self.amostras_por_bit)
        elif tipo == "Bipolar":
            return decodificador_bipolar(sinal, self.amostras_por_bit)
        else:
            raise ValueError(f"Modulação digital desconhecida: {tipo}")
    
    def modular_analogico(self, bits=None, sinal_digital=None, tipo="ASK"):
        # Repassa o self.amostras_por_bit para as funções
        # E usa fc=1 ou 2 para garantir visualização limpa
        if tipo == "ASK":
            return modulador_ask(bits, fc=1, amostras_por_bit=self.amostras_por_bit)
        elif tipo == "FSK":
            return modulador_fsk(bits, f_0=1, f_1=2, amostras_por_bit=self.amostras_por_bit)
        elif tipo == "PSK (QPSK)" or tipo == "QPSK": 
            return modulador_qpsk(bits, fc=1, amostras_por_bit=self.amostras_por_bit)
        elif tipo == "16-QAM" or tipo == "16QAM":
            return modulador_16qam(bits, fc=1, amostras_por_simbolo=self.amostras_por_bit)
        else:
            raise ValueError(f"Modulação analogica desconhecida: {tipo}")

    def demodular_analogico(self, sinal_analogico, tipo):
        if tipo == "ASK":
            return demodulador_ask(sinal_analogico, fc=1, amostras_por_bit=self.amostras_por_bit)
        elif tipo == "FSK":
            return demodulador_fsk(sinal_analogico, f_0=1, f_1=2, amostras_por_bit=self.amostras_por_bit)
        elif tipo == "PSK (QPSK)" or tipo == "QPSK":
            return demodulador_qpsk(sinal_analogico, fc=1, amostras_por_simbolo=self.amostras_por_bit)
        elif tipo == "16-QAM" or tipo == "16QAM":
            return demodulador_16qam(sinal_analogico, fc=1, amostras_por_simbolo=self.amostras_por_bit)
        else:
            raise ValueError(f"Modulação analogica desconhecida: {tipo}")