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


def crc(quadro: bytes, tamanho_do_edc: int = 8, polinomio: int = 0x07) -> bytes:
    """
    Aplica CRC genérico (CRC-8, CRC-16, CRC-32).

    Parâmetros:
        quadro (bytes): Quadro original sem CRC.
        tamanho_do_edc (int): Tamanho do CRC (8, 16, 32 bits).
        polinomio (int): Polinômio gerador.

    Retorna:
        bytes: Quadro + CRC (em bytes).
    """
    crc = 0

    for byte in quadro:
        crc ^= byte
        for _ in range(8):
            if crc & (1 << (tamanho_do_edc - 1)):
                crc = (crc << 1) ^ polinomio
            else:
                crc <<= 1

            crc &= (1 << tamanho_do_edc) - 1  # Mantém tamanho correto

    # Quantidade de bytes necessária para armazenar o CRC
    num_bytes_crc = (tamanho_do_edc + 7) // 8

    crc_bytes = crc.to_bytes(num_bytes_crc, byteorder='big')

    return quadro + crc_bytes


def verifica_crc(quadro: bytes, tamanho_do_edc: int = 8, polinomio: int = 0x07) -> bytes:
    """
    Verifica CRC de tamanho variável (8, 16, 32 bits).

    Parâmetros:
        quadro (bytes): Quadro contendo os dados + CRC no final.
        tamanho_do_edc (int): Número de bits do CRC.
        polinomio (int): Polinômio gerador.

    Retorna:
        bytes: Quadro sem o CRC, se válido.

    Exceção:
        ValueError: Se o CRC for inválido.
    """
    num_bytes_crc = (tamanho_do_edc + 7) // 8
    crc = 0

    # Recalcula o CRC processando todo o quadro (dados + CRC)
    for byte in quadro:
        crc ^= byte
        for _ in range(8):
            if crc & (1 << (tamanho_do_edc - 1)):
                crc = (crc << 1) ^ polinomio
            else:
                crc <<= 1

            crc &= (1 << tamanho_do_edc) - 1

    # CRC válido ⇒ resultado deve ser 0
    if crc != 0:
        raise ValueError("Erro de CRC detectado!")

    # Retorna apenas o quadro original, sem os bytes do CRC
    return quadro[:-num_bytes_crc]
