import Utils


def enquadrar_contagem_caracteres(dado: bytes) -> bytes:
    tamanho = len(dado) + 1
    tamanho_byte = tamanho.to_bytes(1, byteorder='big')
    quadro = tamanho_byte + dado
    return quadro


def desenquadrar_contagem_caracteres(quadro: bytes) -> bytes:
    """
    Desfaz o enquadramento por contagem de caracteres.

    Dinâmica:
        Remove o primeiro byte (que indica o tamanho do quadro) e retorna o restante.

    Parâmetros:
    • quadro (bytes): Quadro com o byte de tamanho seguido do payload.

    Retorna:
    • bytes: Apenas o payload (dados da camada de aplicação).
    """
    return quadro[1:]  # Remove primeiro byte



def enquadrar_flag_insercao_byte(dado: bytes, flag=b'\x7E', esc=b'\x7D') -> bytes:
    """
    Enquadramento por inserção de bytes.

    Dinâmica:
        - Adiciona uma flag no início e no final da mensagem.
        - Se a flag aparece na mensagem, insere caractere de escape antes.
        - Se o escape aparece na mensagem, duplica o escape.

    Retorna:
    • bytes: Quadro enquadrado.
    """
    if flag in dado:
        esc_pos = Utils.findall(esc, dado)
        for pos in range(len(esc_pos)):
            offset = len(esc) * pos
            dado = dado[:(esc_pos[pos] + offset)] + esc + dado[(esc_pos[pos] + offset):]

        flag_pos = Utils.findall(flag, dado)
        for pos in range(len(flag_pos)):
            offset = len(esc) * pos
            dado = dado[:(flag_pos[pos] + offset)] + esc + dado[(flag_pos[pos] + offset):]

    return flag + dado + flag


def desenquadrar_flag_insercao_byte(quadro: bytes, flag=b'\x7E', esc=b'\x7D') -> bytes:
    """
    Desenquadramento por inserção de bytes.

    Remove flags e processa os caracteres de escape restaurando o conteúdo original.
    """
    if not (quadro.startswith(flag) and quadro.endswith(flag)):
        raise ValueError("Flags de início/fim ausentes")

    quadro = quadro[len(flag):-len(flag)]

    resultado = bytearray()
    i = 0
    n = len(quadro)

    while i < n:
        if quadro[i:i+1] == esc:
            if i + 1 >= n:
                raise ValueError("Escape incompleto no fim do quadro")
            resultado.append(quadro[i+1])
            i += 2
        else:
            resultado.append(quadro[i])
            i += 1

    return bytes(resultado)


def enquadrar_flag_insercao_bit(dado: bytes) -> bytes:
    """
    Enquadra usando bit stuffing com FLAG 0x7E (01111110).
    Atenção: O último byte do quadro pode ficar incompleto.
    """
    FLAG = b'\x7E'

    # Converte o objeto bytes em uma única string de bits
    bit_str = ''.join(f'{byte:08b}' for byte in dado)

    bits_preenchidos = []
    cont_1bit = 0

    for bit in bit_str:
        bits_preenchidos.append(bit)
        
        if bit == '1':
            cont_1bit += 1
        else:
            cont_1bit = 0

        # Regra de Stuffing: Insere '0' após o quinto '1' consecutivo
        if cont_1bit == 5:
            bits_preenchidos.append('0')
            cont_1bit = 0
            
    bit_string_final = ''.join(bits_preenchidos)
    
    bytes_preenchidos = bytes(
        int(bit_string_final[i:i+8], 2)
        for i in range(0, len(bit_string_final), 8)
    )

    return FLAG + bytes_preenchidos + FLAG


def desenquadrar_flag_insercao_bit(quadro: bytes) -> bytes:
    """
    Desfaz o bit stuffing removendo a FLAG 0x7E e removendo os bits inseridos.
    """
    FLAG = b'\x7E'

    if quadro[:1] != FLAG or quadro[-1:] != FLAG:
        raise ValueError("FLAG de delimitação ausente")

    quadro = quadro[1:-1]

    bit_str = ''.join(f'{byte:08b}' for byte in quadro)

    bits_desenquadrados = []
    cont_1bit = 0
    i = 0

    while i < len(bit_str):
        bit = bit_str[i]
        bits_desenquadrados.append(bit)

        if bit == '1':
            cont_1bit += 1
            if cont_1bit == 5:
                i += 1
                cont_1bit = 0
        else:
            cont_1bit = 0

        i += 1

    while len(bits_desenquadrados) % 8 != 0:
        bits_desenquadrados.pop()

    dados = bytes(
        int(''.join(bits_desenquadrados[i:i+8]), 2)
        for i in range(0, len(bits_desenquadrados), 8)
    )

    return dados
