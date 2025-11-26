import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np 

def bytes_para_bits(self, dados_em_bytes: bytes) -> list[int]:
        bits = []
        for byte in dados_em_bytes:
            binario = format(byte, '08b')
            bits.extend([int(b) for b in binario])
        return bits

    
def findall(substring, string):
    """
    Encontra todas as ocorrencias de uma substring na string original
     
    Args:
        substring: substring que deseja ser encotnrada
        string: String original
    
    Returns:
        Lista de com todos os indexs do inicio da substring

    """
    l = []
    i = -1
    while True:
        i = string.find(substring, i+1)
        if i == -1:
            return l
        l.append(string.find(substring, i))

def find_xor(a:str, b:str) -> str:
    """
    Realiza o Xor bit a bit da palavra
     
    Args:
        a: string que será relizada o xor
        b: string que será relizada o xor
    
    Returns:
        String com do resultado do xor bit a bit de a e b 

    """
    n = len(b)
    result = ""
    for i in range(1, n):  # Skip first bit (CRC standard)
        result += '0' if a[i] == b[i] else '1'
    return result


def bits_list_formatter(bits_data: list) -> str:
    """
    Recebe uma lista de bits (0 e 1) e retorna uma string formatada.
    Ex: [0, 1, 1, 0] -> "0110"
    """
    try:
        # Garante que é uma lista plana e converte cada item para string
        return "".join(str(int(bit)) for bit in bits_data)
    except Exception:
        return str(bits_data)

def byte_formarter(data: bytes) -> str:
    """
    Formata bytes para visualização binária.
    """
    return ' '.join(f'{b:08b}' for b in data)