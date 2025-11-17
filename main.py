from CamadaFisica.nrz_polar import codificador_nrz_polar, decodificador_nrz_polar,  plotagem_nrz
from CamadaFisica.manchester import codificador_manchester, decodificador_manchester, plotagem_manchester
from CamadaFisica.bipolar import codificador_bipolar, decodificador_bipolar, plotagem_bipolar

def main():
    bits = [1, 0, 1, 1, 0, 0, 1]

    sinal = codificador_nrz_polar(bits, amostras_por_bit=50)
    bits_decod = decodificador_nrz_polar(sinal, amostras_por_bit=50)
    plotagem_nrz(bits, amostras_por_bit=50)

    print("Original:     ", bits)
    print("Decodificado: ", bits_decod.tolist())


    plotagem_manchester(bits, amostras_por_bit=50)
    plotagem_bipolar(bits, amostras_por_bit=50)



if __name__ == "__main__":
    main()