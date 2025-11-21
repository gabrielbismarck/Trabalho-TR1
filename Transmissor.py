import numpy as np
from CamadaFisica import CamadaFisica
from CamadaEnlace import CamadaEnlace

class Transmissor:
    def __init__(self, amostras_por_bit=50):
        self.fisica = CamadaFisica(amostras_por_bit)
        self.enlace = CamadaEnlace()

    def bytes_para_bits(self, dados_bytes):
        """Converte bytes para array de bits (0 e 1) para a camada física"""
        bits = []
        for byte in dados_bytes:
            bin_str = f'{byte:08b}'
            bits.extend([int(b) for b in bin_str])
        return np.array(bits)

    def processar(self, texto, mod_digital, tipo_enquadramento, tipo_erro="Bit de Paridade Par"):
        """
        Fluxo: Texto -> Bytes -> (Erro) -> (Enquadramento) -> Bits -> Modulação
        """
        #Aplicação: Texto -> Bytes
        # Se o texto for vazio, usa um espaço para não quebrar
        if not texto: texto = " "
        dados_originais = texto.encode('utf-8') 
        
        # Aplica CRC, Hamming ou Paridade NO DADO BRUTO
        dados_com_erro = self.enlace.aplicar_deteccao_correcao(dados_originais, tipo_erro)

        # Enquadra o dado já protegido
        quadro_bytes = self.enlace.enquadrar(dados_com_erro, tipo_enquadramento)
        
        quadro_bits = self.bytes_para_bits(quadro_bytes)

        # Gera o sinal elétrico (amostras)
        sinal_digital = self.fisica.codificar_digital(quadro_bits, mod_digital)
        
        # Retorna o sinal para o meio e os bits para plotagem
        return sinal_digital, quadro_bits