def hamming(dado: bytes) -> bytes:
    """
    Codifica os dados usando o código de Hamming.

    Parâmetros:
    • dado (bytes): Dados de entrada a serem codificados.

    Retorna:
    • bytes: Dados codificados com código Hamming.
    """

    def calcular_bits_paridade(bits_dados: list) -> tuple:
        p1 = bits_dados[0] ^ bits_dados[1] ^ bits_dados[3]  # p1 = d1 ⊕ d2 ⊕ d4
        p2 = bits_dados[0] ^ bits_dados[2] ^ bits_dados[3]  # p2 = d1 ⊕ d3 ⊕ d4
        p3 = bits_dados[1] ^ bits_dados[2] ^ bits_dados[3]  # p3 = d2 ⊕ d3 ⊕ d4
        return p1, p2, p3

    codificacao_bytes = []  # Lista que vai armazenar os bytes codificados

    for byte in dado:
        # Divide o byte em dois nibbles
        nibbles = [(byte >> 4) & 0b1111, byte & 0b1111]

        for nibble in nibbles:
            # Converte o nibble em lista de bits [d1, d2, d3, d4]
            bits_dados = [(nibble >> j) & 1 for j in range(3, -1, -1)]

            # Calcula p1, p2, p3
            p1, p2, p3 = calcular_bits_paridade(bits_dados)

            # Formato [p1, p2, d1, p3, d2, d3, d4]
            bloco_hamming = [
                p1,
                p2,
                bits_dados[0],
                p3,
                bits_dados[1],
                bits_dados[2],
                bits_dados[3]
            ]

            # Converte 7 bits para 1 byte (msb não usado)
            byte_codificado = 0
            for i, bit in enumerate(bloco_hamming):
                byte_codificado |= bit << (6 - i)

            codificacao_bytes.append(byte_codificado)

    return bytes(codificacao_bytes)


def verifica_hamming(quadro: bytes) -> bytes:
    """
    Verifica e corrige os dados codificados com o código de Hamming (7,4).

    Parâmetros:
        quadro (bytes): Dados codificados com Hamming (7,4).

    Retorna:
        bytes: Dados corrigidos e decodificados (sem bits de paridade).
    """

    dados_decodificados = []

    for byte in quadro:
        # Obtém os 7 bits úteis
        bits = [(byte >> (6 - i)) & 1 for i in range(7)]

        # Mapeamento: p1, p2, d1, p3, d2, d3, d4
        p1, p2, d1, p3, d2, d3, d4 = bits

        # Síndromes (paridades esperadas)
        s1 = p1 ^ d1 ^ d2 ^ d4
        s2 = p2 ^ d1 ^ d3 ^ d4
        s3 = p3 ^ d2 ^ d3 ^ d4

        # Posição do erro (0 = sem erro)
        erro_pos = (s3 << 2) | (s2 << 1) | s1

        # Corrige erro (somente se atingir bit de dado)
        if erro_pos in {3, 5, 6, 7}:
            bits[erro_pos - 1] ^= 1
            p1, p2, d1, p3, d2, d3, d4 = bits

        # Reconstrói o nibble original
        nibble = (d1 << 3) | (d2 << 2) | (d3 << 1) | d4
        dados_decodificados.append(nibble)

    # Reagrupa nibbles em bytes
    bytes_decodificados = bytearray()
    for i in range(0, len(dados_decodificados), 2):
        if i + 1 < len(dados_decodificados):
            byte = (dados_decodificados[i] << 4) | dados_decodificados[i + 1]
        else:
            byte = dados_decodificados[i] << 4
        bytes_decodificados.append(byte)

    return bytes(bytes_decodificados)
