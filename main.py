from CamadaFisica import codificador_nrz_polar, decodificador_nrz_polar,  plotagem_nrz
from CamadaFisica import codificador_manchester, decodificador_manchester, plotagem_manchester
from CamadaFisica import codificador_bipolar, decodificador_bipolar, plotagem_bipolar
from Enlace.enquadramentoDados import enquadrar_contagem_caracteres, desenquadrar_contagem_caracteres, enquadrar_flag_insercao_bit, desenquadrar_flag_insercao_bit, enquadrar_flag_insercao_byte, desenquadrar_flag_insercao_byte

def main():
    bits = [0, 1, 0, 1, 0, 0, 1, 1]
    byte = b"01111110"

    sinal = codificador_nrz_polar(bits, amostras_por_bit=50)
    bits_decod = decodificador_nrz_polar(sinal, amostras_por_bit=50)
    plotagem_nrz(bits, amostras_por_bit=50)

    print("Original:     ", bits)
    print("Enquadramento contagem de caractere:     ", enquadrar_contagem_caracteres(byte))
    print("Desenquadramento:     ", desenquadrar_contagem_caracteres(enquadrar_contagem_caracteres(byte)))
    print("Enquadramento inserção de bit:     ", enquadrar_flag_insercao_bit(byte))
    print("Desenquadramento:     ", desenquadrar_flag_insercao_bit(enquadrar_flag_insercao_bit(byte)))
    print("Enquadramento inserção de byte:     ", enquadrar_flag_insercao_byte(byte))
    print("Desenquadramento:     ", desenquadrar_flag_insercao_byte(enquadrar_flag_insercao_byte(byte)))
    print("Decodificado: ", bits_decod.tolist())


    plotagem_manchester(bits, amostras_por_bit=50)
    plotagem_bipolar(bits, amostras_por_bit=50)



if __name__ == "__main__":
    main()