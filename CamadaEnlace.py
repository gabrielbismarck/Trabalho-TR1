# Arquivo: CamadaEnlace.py
import Enlace.enquadramentoDados as enquadramentoDados
import Enlace.errorDetection as errorDetection
import Enlace.errorCorrection as errorCorrection

class CamadaEnlace:
    def __init__(self):
        pass

    def aplicar_deteccao_correcao(self, dados: bytes, tipo: str) -> bytes:
        """
        Aplica o algoritmo de erro escolhido.
        """
        if tipo == "Bit de Paridade Par":
            return errorDetection.bit_de_paridade_par(dados)
        elif tipo == "CRC-32":
            # Polinômio padrão IEEE 802.3 para CRC-32: 0x04C11DB7
            return errorDetection.crc(dados)
        elif tipo == "Hamming":
            return errorCorrection.hamming(dados)
        elif tipo == "Checksum":
            return errorDetection.checksum(dados) 
        else:
            return dados # Nenhum tratamento

    def verificar_deteccao_correcao(self, dados: bytes, tipo: str) -> bytes:
        """
        Verifica/Corrige o erro e remove os bits de controle.
        """
        if tipo == "Bit de Paridade Par":
            return errorDetection.verifica_bit_de_paridade_par(dados)
        elif tipo == "CRC-32":
            return errorDetection.verifica_crc(dados)
        elif tipo == "Hamming":
            return errorCorrection.verifica_hamming(dados)
        elif tipo == "Checksum":
            return errorDetection.verifica_checksum(dados)
        else:
            return dados

    def enquadrar(self, dados: bytes, tipo: str) -> bytes:
        """
        Aplica o enquadramento desejado.
        """
        if tipo == "Contagem de Caracteres":
            return enquadramentoDados.enquadrar_contagem_caracteres(dados)
        elif tipo == "Inserção de Bytes":
            return enquadramentoDados.enquadrar_flag_insercao_byte(dados)
        elif tipo == "Inserção de Bits":
            return enquadramentoDados.enquadrar_flag_insercao_bit(dados)
        else:
            return dados

    def desenquadrar(self, dados: bytes, tipo: str) -> bytes:
        """
        Desenquadra a mensagem transmitida
        """
        if tipo == "Contagem de Caracteres":
            return enquadramentoDados.desenquadrar_contagem_caracteres(dados)
        elif tipo == "Inserção de Bytes":
            return enquadramentoDados.desenquadrar_flag_insercao_byte(dados)
        elif tipo == "Inserção de Bits":
            return enquadramentoDados.desenquadrar_flag_insercao_bit(dados)
        else:
            return dados