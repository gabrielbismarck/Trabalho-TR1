# Arquivo: CamadaFisica.py
import numpy as np
from Fisica.nrz_polar import codificador_nrz_polar, decodificador_nrz_polar
from Fisica.manchester import codificador_manchester, decodificador_manchester
from Fisica.bipolar import codificador_bipolar, decodificador_bipolar

class CamadaFisica:
    def __init__(self, amostras_por_bit=50):
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
    
    def modular_analogico(self, sinal_digital, tipo):
        # TODO: Implementar ASK, FSK, PSK, QAM
        # Por enquanto retorna o próprio sinal digital para teste
        return sinal_digital 

    def demodular_analogico(self, sinal_analogico, tipo):
        # TODO: Implementar ASK, FSK, PSK, QAM
        return sinal_analogico