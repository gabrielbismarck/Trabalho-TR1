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
        
        # Padding se necessário (garante multiplo de 8)
        resto = len(bits_str) % 8
        if resto != 0:
            bits_str += "0" * (8 - resto)
            
        bytes_lista = []
        for i in range(0, len(bits_str), 8):
            byte_str = bits_str[i:i+8]
            # Proteção contra bytes vazios
            if byte_str:
                bytes_lista.append(int(byte_str, 2))
            
        return bytes(bytes_lista)

    def decodificar(self, sinal, mod_digital, tipo_enquadramento, tipo_erro="Bit de Paridade Par", mod_portadora="ASK"):
        """
        Fluxo: Sinal Modulado -> Demodulação -> Bits -> Bytes -> (Desenquadramento) -> (Verificação) -> Texto
        """
        try:
            # 1. Camada Física: Demodula a Portadora
            # Isso JÁ RETORNA OS BITS (ex: [0, 1, 0, 1...])
            bits_recebidos = self.fisica.demodular_analogico(sinal, tipo=mod_portadora)
            
            # --- CORREÇÃO AQUI ---
            # Removemos a chamada 'self.fisica.decodificar_digital'.
            # Motivo: O demodulador analógico já entregou os bits. 
            # Tentar decodificar digitalmente aqui trataria os bits como amostras de sinal, destruindo o dado.
            
            # Garante que é uma lista de inteiros
            bits_recebidos = [int(b) for b in bits_recebidos]

            # 2. Interface Física-Enlace: Bits -> Bytes
            bytes_quadro = self.bits_para_bytes(bits_recebidos)

            # 3. Camada de Enlace: Desenquadramento
            try:
                dados_enquadrados = self.enlace.desenquadrar(bytes_quadro, tipo_enquadramento)
            except Exception as e:
                # Retorna erro mas mantem os bits para visualização no debug
                return f"[Erro de Enquadramento: {e}]", bits_recebidos

            # 4. Camada de Enlace: Verificação de Erros
            try:
                dados_limpos = self.enlace.verificar_deteccao_correcao(dados_enquadrados, tipo_erro)
            except ValueError as ve:
                return f"[Erro detectado ({tipo_erro})]", bits_recebidos
            except Exception as e:
                return f"[Erro desconhecido na verificação: {e}]", bits_recebidos

            # 5. Aplicação: Bytes -> Texto
            try:
                texto_final = dados_limpos.decode('utf-8')
                return texto_final, bits_recebidos
            except UnicodeDecodeError:
                 # Tenta decodificar ignorando erros para mostrar algo
                 texto_final = dados_limpos.decode('utf-8', errors='replace')
                 return f"[Erro UTF-8] {texto_final}", bits_recebidos

        except Exception as e:
            # Em caso de erro crítico, retorna o erro e uma lista vazia
            print(f"Erro no Receptor: {e}")
            return f"[Erro Crítico RX: {e}]", []