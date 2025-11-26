def hamming(dado: bytes) -> bytes:
    """
    Codifica os dados usando o código de Hamming (suporta qualquer tamanho configurável).

    Parâmetros:
    • dado (bytes): Dados de entrada a serem codificados.

    Retorna:
    • bytes: Dados codificados com código Hamming.
    """

    def calcular_bits_paridade_necessarios(bd: int) -> int:
        bp = 0
        while (2 ** bp) < (bd + bp + 1):
            bp += 1
        return bp

    def calcular_bits_paridade(bits_completos: list, posicoes_paridade: list) -> list:
        paridades = []
        for pos_p in posicoes_paridade:
            xor = 0
            for i in range(len(bits_completos)):
                if (i + 1) & pos_p:  # inclui a própria posição de paridade no cálculo
                    xor ^= bits_completos[i]
            paridades.append(xor)
        return paridades

    # ==============================================================
    BITS_DADOS_POR_BLOCO = 4          # Alterar aqui para 4, 8, 11, 16, 26, etc.
    # ==============================================================

    bp = calcular_bits_paridade_necessarios(BITS_DADOS_POR_BLOCO)
    n = BITS_DADOS_POR_BLOCO + bp      # tamanho total do bloco codificado

    # Converte todos os dados para uma lista unica de bits
    todos_bits_dados = []
    for byte in dado:
        for j in range(7, -1, -1):               
            todos_bits_dados.append((byte >> j) & 1)

    # Calcula quantos bits validos temos
    total_bits_orig = len(todos_bits_dados)
    
    # Adiciona padding 0 apenas para completar o ultimo bloco de dados (não de codificação!)
    padding_necessario = (BITS_DADOS_POR_BLOCO - (total_bits_orig % BITS_DADOS_POR_BLOCO)) % BITS_DADOS_POR_BLOCO
    todos_bits_dados.extend([0] * padding_necessario)

    resultado_bits = []

    # posiçoes 1,2,4,8,...
    posicoes_paridade = [1 << i for i in range(bp)]  

    i = 0
    while i < len(todos_bits_dados):
        # Cria bloco vazio
        bloco = [0] * n

        # Insere bits de dados nas posições não-paridade
        pos_dado = 0
        for pos in range(1, n + 1):
            if pos not in posicoes_paridade:
                bloco[pos - 1] = todos_bits_dados[i + pos_dado]
                pos_dado += 1

        # Calcula e insere paridades
        paridades = calcular_bits_paridade(bloco, posicoes_paridade)
        for pos_p, valor in zip(posicoes_paridade, paridades):
            bloco[pos_p - 1] = valor

        resultado_bits.extend(bloco)
        i += BITS_DADOS_POR_BLOCO

    # Converte para bytes
    bytes_codificados = bytearray()
    for i in range(0, len(resultado_bits), 8):
        byte = 0
        for j in range(min(8, len(resultado_bits) - i)):
            byte |= resultado_bits[i + j] << (7 - j)
        bytes_codificados.append(byte)

    # Adiciona 2 bytes no final com o numero de bits validos originais
    # Isso permite ao decodificador saber exatamente onde parar
    bytes_codificados.append((total_bits_orig >> 8) & 0xFF)
    bytes_codificados.append(total_bits_orig & 0xFF)

    return bytes(bytes_codificados)


def verifica_hamming(quadro: bytes) -> bytes:
    """
    Verifica e corrige os dados codificados com o código de Hamming.
    Os últimos 2 bytes do quadro contêm o número total de bits originais.

    Parâmetros:
        quadro (bytes): Dados codificados com Hamming.

    Retorna:
        bytes: Dados corrigidos e decodificados (sem bits de paridade).
    """

    def calcular_bits_paridade_necessarios(bd: int) -> int:
        bp = 0
        while (2 ** bp) < (bd + bp + 1):
            bp += 1
        return bp

    # ==============================================================
    BITS_DADOS_POR_BLOCO = 4
    # ==============================================================

    bp = calcular_bits_paridade_necessarios(BITS_DADOS_POR_BLOCO)
    n = BITS_DADOS_POR_BLOCO + bp

    if len(quadro) < 2:
        return b''

    total_bits_orig = quadro[-2] | (quadro[-1] << 8)
    quadro_bits = quadro[:-2]  # remove os 2 bytes de metadado

    # Converte para lista de bits
    bits = []
    for byte in quadro_bits:
        for j in range(7, -1, -1):
            bits.append((byte >> j) & 1)

    posicoes_paridade = [1 << i for i in range(bp)]
    dados_extraidos = []

    for inicio in range(0, len(bits), n):
        bloco = bits[inicio:inicio + n]
        if len(bloco) < n:
            break

        # Calcula sindrome
        sindrome = 0
        for pos_p in posicoes_paridade:
            xor = 0
            for i in range(n):
                if (i + 1) & pos_p:
                    xor ^= bloco[i]
            if xor:
                sindrome |= pos_p

        # Corrige se necessario
        if 1 <= sindrome <= n:
            bloco[sindrome - 1] ^= 1

        # Extrai apenas bits de dados
        for i in range(n):
            if (i + 1) not in posicoes_paridade:
                dados_extraidos.append(bloco[i])

        if len(dados_extraidos) >= total_bits_orig:
            break

    # Remove padding que pode ter sido adicionado
    dados_extraidos = dados_extraidos[:total_bits_orig]

    # Converte de volta para bytes
    resultado = bytearray()
    for i in range(0, len(dados_extraidos), 8):
        byte = 0
        for j in range(min(8, len(dados_extraidos) - i)):
            byte |= dados_extraidos[i + j] << (7 - j)
        resultado.append(byte)

    return bytes(resultado)