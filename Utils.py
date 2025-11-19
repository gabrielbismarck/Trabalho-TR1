import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np 

def byte_formarter(bytes_data):
    """
    Transforma bytes em string dos bits correspondentes.

    Parâmetros:
    • bytes_data (bytes): Dados em bytes.

    Retorna:
    • str: String dos bits formatada, com espaço entre os bytes.

    Exemplo:
        Entrada → b'teste'
        Saída  → "01110100 01100101 01110011 01110100 01100101"
    """
    return ' '.join(f"{byte:08b}" for byte in bytes_data)

    
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
