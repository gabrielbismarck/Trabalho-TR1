import numpy as np
from CamadaFisica import CamadaFisica
from CamadaEnlace import CamadaEnlace

class Receptor:
    def __init__(self, amostras_por_bit=50):
        self.fisica = CamadaFisica(amostras_por_bit)
        self.enlace = CamadaEnlace()

    def bits_para_bytes(self, bits_array):
        """Converte array de bits (0 e 1) de volta para bytes"""
        bits_str = "".join(str(int(b)) for b in bits_array)
        
        # Padding se necessário
        resto = len(bits_str) % 8
        if resto != 0:
            bits_str += "0" * (8 - resto)
            
        bytes_lista = []
        for i in range(0, len(bits_str), 8):
            byte_str = bits_str[i:i+8]
            bytes_lista.append(int(byte_str, 2))
            
        return bytes(bytes_lista)

    def decodificar(self, sinal, mod_digital, tipo_enquadramento, tipo_erro="Bit de Paridade Par", mod_portadora="ASK"):
        """
        Fluxo: Sinal -> Demodulação -> Bits -> Bytes -> (Desenquadramento) -> (Verificação) -> Texto
        """
        try:

            bits_demodulados = self.fisica.demodular_analogico(sinal, tipo=mod_portadora)

            # 1. Camada Física: Decodifica o sinal digital -> Bits
            bits_recebidos = self.fisica.decodificar_digital(bits_demodulados, mod_digital)
            
            # 2. Interface Física-Enlace: Bits -> Bytes
            bytes_quadro = self.bits_para_bytes(bits_recebidos)

            # 3. Camada de Enlace: Desenquadramento
            try:
                dados_enquadrados = self.enlace.desenquadrar(bytes_quadro, tipo_enquadramento)
            except Exception as e:
                return f"[Erro de Enquadramento: {e}]", bits_recebidos

            # 4. Camada de Enlace: Verificação de Erros
            try:
                dados_limpos = self.enlace.verificar_deteccao_correcao(dados_enquadrados, tipo_erro)
            except ValueError as ve:
                return f"[Erro detectado ({tipo_erro}): {ve}]", bits_recebidos
            except Exception as e:
                return f"[Erro desconhecido na verificação: {e}]", bits_recebidos

            # 5. Aplicação: Bytes -> Texto
            try:
                texto_final = dados_limpos.decode('utf-8')
                return texto_final, bits_recebidos
            except UnicodeDecodeError:
                 return f"[Erro: Bytes inválidos para texto]", bits_recebidos

        except Exception as e:
            return f"{e}", []