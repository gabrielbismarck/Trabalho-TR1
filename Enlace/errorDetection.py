import Utils

def bit_de_paridade_par(quadro: bytes) -> bytes:
    """
    Força o quadro a ter número par de bits '1' usando paridade PAR.
    Adiciona 1 byte ao final contendo 0x00 ou 0x01.

    Funcionamento:
        • Saída = quadro + b"\x01" → se número de 1s for ímpar.
        • Saída = quadro + b"\x00" → se número de 1s for par.

    Parâmetro:
        quadro (bytes): Quadro sem o bit de paridade.

    Retorna:
        bytes: Quadro com o bit de paridade par.
    """
    # Converte para bits e remove espaços
    bits = Utils.byte_formarter(quadro).replace(" ", "")

    # Se número de '1' for ímpar → adiciona bit 1
    if bits.count("1") % 2 != 0:
        return quadro + b"\x01"
    else:
        return quadro + b"\x00"


def verifica_bit_de_paridade_par(quadro: bytes) -> bytes:
    """
    Verifica o bit de paridade par e remove o byte de paridade.

    Parâmetro:
        quadro (bytes): Quadro contendo o byte de paridade no final.

    Retorna:
        bytes: Quadro sem o byte de paridade.

    Exceção:
        ValueError: Se o número de bits '1' for ímpar (erro detectado).
    """
    # Converte para bits
    bits = Utils.byte_formarter(quadro).replace(" ", "")

    # Número de '1' deve ser PAR
    if bits.count("1") % 2 != 0:
        raise ValueError("Erro de paridade! Número ímpar de bits 1.")

    # Remove último byte (bit de paridade)
    return quadro[:-1]

def checksum(quadro: bytes) -> bytes:
    """
    Calcula o Checksum

    Parâmetro:
        quadro (bytes): Quadro contendo o byte

    Retorna:
        bytes: Quadro original + 1 byte checksum
    """
    soma = 0
    
    for byte in quadro:
        soma += byte
        
        # Se a soma passar de 8 bits, o bit de "carry" deve ser somado de volta no bit menos significativo.
        while soma > 0xFF:
            soma = (soma & 0xFF) + (soma >> 8)

    # Calcula o complemento (inverte os bits) e garante a máscara 0xFF
    checksum_val = ~soma & 0xFF

    return quadro + checksum_val.to_bytes(1, byteorder='big')

def verifica_checksum(quadro: bytes) -> bytes:
    """
    Verifica o Checksum.

    - Soma (Dados + Checksum recebido).
    - Faz o complemento do resultado.
    - Se o resultado final for 0, aceita.


    Parâmetro:
        quadro (bytes): Quadro contendo o quadro original + 1 byte checksum

    Retorna:
        bytes: Quadro contendo o byte
    """
    soma = 0
    
    for byte in quadro:
        soma += byte
        while soma > 0xFF:
            soma = (soma & 0xFF) + (soma >> 8)
            
    # Complemento do resultado final
    resultado = ~soma & 0xFF

    if resultado != 0:
        raise ValueError("Erro de Checksum detectado!")
        
    # Retorna os dados removendo o byte de checksum do final
    return quadro[:-1]

def crc(quadro: bytes, tamanho_do_edc: int = 32, polinomio: int = 0x04C11DB7) -> bytes:
    """
    Calcula o código CRC-32 (IEEE 802.3) ao quadro de dados.

    Parâmetros:
        quadro (bytes): Dados originais da camada de enlace.
        tamanho_do_edc (int): Tamanho do código de verificação em bits (Padrão: 32).
        polinomio (int): Polinômio gerador do CRC (Padrão: 0x04C11DB7 - IEEE 802.3).

    Retorna:
        bytes: O quadro original concatenado com os bytes do CRC calculado.
    """
    crc = 0
    mask = (1 << tamanho_do_edc) - 1 # Máscara para manter 32 bits (0xFFFFFFFF)

    for byte in quadro:
        crc ^= (byte << (tamanho_do_edc - 8)) # Alinha o byte ao MSB
        for _ in range(8):
            if crc & (1 << (tamanho_do_edc - 1)): # Verifica bit mais significativo
                crc = (crc << 1) ^ polinomio
            else:
                crc <<= 1
            crc &= mask # Garante que não exceda 32 bits

    num_bytes_crc = (tamanho_do_edc + 7) // 8
    crc_bytes = crc.to_bytes(num_bytes_crc, byteorder='big')

    return quadro + crc_bytes


def verifica_crc(quadro: bytes, tamanho_do_edc: int = 32, polinomio: int = 0x04C11DB7) -> bytes:
    """
    Verifica a integridade do quadro recalculando o CRC dos dados e comparando com o CRC recebido.

    Parâmetros:
        quadro (bytes): Quadro recebido contendo os dados seguidos pelo CRC.
        tamanho_do_edc (int): Tamanho do código de verificação em bits (Padrão: 32).
        polinomio (int): Polinômio gerador utilizado para validação.

    Retorna:
        bytes: O quadro de dados original (sem os bytes de CRC).

    Exceção:
        ValueError: Se o CRC calculado não coincidir com o CRC recebido (erro detectado).
    """
    # 1. Descobre quantos bytes são do CRC
    num_bytes_crc = (tamanho_do_edc + 7) // 8

    # 2. Separa o Dado Original do CRC que veio junto
    dados_apenas = quadro[:-num_bytes_crc]
    crc_recebido = quadro[-num_bytes_crc:]

    #Recalcula o CRC usando APENAS os dados
    quadro_esperado = crc(dados_apenas, tamanho_do_edc, polinomio)
    
    crc_calculado = quadro_esperado[-num_bytes_crc:]

    if crc_recebido != crc_calculado:
        raise ValueError("Erro de CRC detectado!")

    return dados_apenas
