import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Imports
from CamadaFisica.nrz_polar import codificador_nrz_polar
from CamadaFisica.manchester import codificador_manchester
from CamadaFisica.bipolar import codificador_bipolar

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de Camada Física e de Enlace")
        self.geometry("1400x900")

        # Bloco dos botões
        self.control_frame = ctk.CTkFrame(self, width=350) 
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.control_frame.pack_propagate(False)

        # Bloco dos gráficos
        self.plot_container = ctk.CTkFrame(self) 
        self.plot_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ==Widgets do bloco de botões==
        # Entrada de texto
        self.entry_label = ctk.CTkLabel(self.control_frame, text="Texto a ser transmitido:", font=("Arial", 14, "bold"))
        self.entry_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        self.text_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Digite seu texto aqui")
        self.text_entry.pack(pady=5, padx=10, fill="x")

        # Bloco de modulação digital
        self.mod_digital_frame = ctk.CTkFrame(self.control_frame)
        self.mod_digital_frame.pack(pady=10, padx=10, fill="x", anchor="w")

        self.mod_digital_label = ctk.CTkLabel(self.mod_digital_frame, text="Modulação Digital")
        self.mod_digital_label.pack(pady=5, padx=10, anchor="w")

        # Set botões mod digital
        self.mod_digital_var = ctk.StringVar(value="NRZ")

        self.radio_nrz = ctk.CTkRadioButton(self.mod_digital_frame, text="NRZ", variable=self.mod_digital_var, value="NRZ")
        self.radio_nrz.pack(pady=5, padx=20, anchor="w")
        
        self.radio_manchester = ctk.CTkRadioButton(self.mod_digital_frame, text="Manchester", variable=self.mod_digital_var, value="Manchester")
        self.radio_manchester.pack(pady=5, padx=20, anchor="w")
        
        self.radio_bipolar = ctk.CTkRadioButton(self.mod_digital_frame, text="Bipolar", variable=self.mod_digital_var, value="Bipolar")
        self.radio_bipolar.pack(pady=5, padx=20, anchor="w")

        # Bloco de modulação por portadora
        self.mod_portadora_frame = ctk.CTkFrame(self.control_frame)
        self.mod_portadora_frame.pack(pady=10, padx=10, fill="x", anchor="w")

        self.mod_portadora_label = ctk.CTkLabel(self.mod_portadora_frame, text="Modulação por Portadora")
        self.mod_portadora_label.pack(pady=5, padx=10, anchor="w")

        # Set botões mod portadora
        self.mod_portadora_var = ctk.StringVar(value="ASK")

        self.radio_ask = ctk.CTkRadioButton(self.mod_portadora_frame, text="ASK", variable=self.mod_portadora_var, value="ASK")
        self.radio_ask.pack(pady=5, padx=20, anchor="w")
        
        self.radio_fsk = ctk.CTkRadioButton(self.mod_portadora_frame, text="FSK", variable=self.mod_portadora_var, value="FSK")
        self.radio_fsk.pack(pady=5, padx=20, anchor="w")
        
        self.radio_psk = ctk.CTkRadioButton(self.mod_portadora_frame, text="PSK", variable=self.mod_portadora_var, value="PSK")
        self.radio_psk.pack(pady=5, padx=20, anchor="w")

        self.radio_16qam = ctk.CTkRadioButton(self.mod_portadora_frame, text="16-QAM", variable=self.mod_portadora_var, value="16-QAM")
        self.radio_16qam.pack(pady=5, padx=20, anchor="w")

        # Bloco de enquadramento
        self.enquadramento_frame = ctk.CTkFrame(self.control_frame)
        self.enquadramento_frame.pack(pady=10, padx=10, fill="x", anchor="w")

        self.enquadramento_label = ctk.CTkLabel(self.enquadramento_frame, text="Enquadramento")
        self.enquadramento_label.pack(pady=5, padx=10, anchor="w")

        # Set botões enquadramento
        self.enquadramento_var = ctk.StringVar(value="Contagem de Caracteres")

        self.radio_cc = ctk.CTkRadioButton(self.enquadramento_frame, text="Contagem de Caracteres", variable=self.enquadramento_var, value="Contagem de Caracteres")
        self.radio_cc.pack(pady=5, padx=20, anchor="w")
        
        self.radio_bytes = ctk.CTkRadioButton(self.enquadramento_frame, text="Inserção de Bytes", variable=self.enquadramento_var, value="Inserção de Bytes")
        self.radio_bytes.pack(pady=5, padx=20, anchor="w")
        
        self.radio_bits = ctk.CTkRadioButton(self.enquadramento_frame, text="Inserção de Bits", variable=self.enquadramento_var, value="Inserção de Bits")
        self.radio_bits.pack(pady=5, padx=20, anchor="w")

        # Bloco de detecçao de erros
        self.erros_frame = ctk.CTkFrame(self.control_frame)
        self.erros_frame.pack(pady=10, padx=10, fill="x", anchor="w")

        self.erros_label = ctk.CTkLabel(self.erros_frame, text="Detecção de Erros")
        self.erros_label.pack(pady=5, padx=10, anchor="w")

        # Set botões erros
        self.erros_var = ctk.StringVar(value="Bit de Paridade Par")

        self.radio_bpp = ctk.CTkRadioButton(self.erros_frame, text="Bit de Paridade Par", variable=self.erros_var, value="Bit de Paridade Par")
        self.radio_bpp.pack(pady=5, padx=20, anchor="w")
        
        self.radio_cs = ctk.CTkRadioButton(self.erros_frame, text="Checksum", variable=self.erros_var, value="Checksum")
        self.radio_cs.pack(pady=5, padx=20, anchor="w")
        
        self.radio_crc = ctk.CTkRadioButton(self.erros_frame, text="CRC-32", variable=self.erros_var, value="CRC-32")
        self.radio_crc.pack(pady=5, padx=20, anchor="w")

        self.radio_ham = ctk.CTkRadioButton(self.erros_frame, text="Hamming", variable=self.erros_var, value="Hamming")
        self.radio_ham.pack(pady=5, padx=20, anchor="w")

        # Botão transmitir
        self.botao_transmitir = ctk.CTkButton(self.control_frame, text="Transmitir", command=self.transmitir, font=("Arial", 14, "bold"))
        self.botao_transmitir.pack(pady=20, padx=10, side="bottom", fill="x")

        # ==Widgets do bloco de grafico==
        # Bloco mod. digital
        self.plot_digital = ctk.CTkFrame(self.plot_container)
        self.plot_digital.pack(fill="both", expand=True, padx=5, pady=5)

        # Bloco mod. portadora
        self.plot_portadora = ctk.CTkFrame(self.plot_container)
        self.plot_portadora.pack(fill="both", expand=True, padx=5, pady=5)

        # Bloco receptor
        self.frame_receptor = ctk.CTkFrame(self.plot_container)
        self.frame_receptor.pack(fill="both", expand=True, padx=5, pady=5)

        self.status = ctk.CTkLabel(self.frame_receptor, text="Status: Aguardando Transmissão...", font=("Arial", 12, "italic"))
        self.status.pack(pady=5, padx=10, anchor="w")

        self.texto_recebido = ctk.CTkLabel(self.frame_receptor, text="Texto Recebido: -", font=("Arial", 14))
        self.texto_recebido.pack(pady=5, padx=10, anchor="w")

        self.bits_recebidos_label = ctk.CTkLabel(self.frame_receptor, text="Bits/Quadros Recebidos:", font=("Arial", 12))
        self.bits_recebidos_label.pack(pady=(5, 0), padx=10, anchor="w")
        
        self.bits_recebidos_texto = ctk.CTkTextbox(self.frame_receptor, height=100)
        self.bits_recebidos_texto.pack(pady=5, padx=10, fill="both", expand=True)
        self.bits_recebidos_texto.insert("1.0", "...")
        self.bits_recebidos_texto.configure(state="disabled")

        self.criar_grafico_inicial()

    def texto_para_bits(self, texto):
        bits = []
        for char in texto:
            binario = format(ord(char), '08b')
            bits.extend([int(b) for b in binario])
        return bits

    def transmitir(self):
        texto = self.text_entry.get()
        mod_digital = self.mod_digital_var.get()
        mod_portadora = self.mod_portadora_var.get()
        
        if not texto:
            texto = "A" # Valor padrao pra teste
        
        bits_para_transmitir = self.texto_para_bits(texto)

        amostras = 50
        sinal_digital = []

        # Seleção
        if mod_digital == "NRZ":
            sinal_digital = codificador_nrz_polar(bits_para_transmitir, amostras_por_bit=amostras)
        elif mod_digital == "Manchester":
            sinal_digital = codificador_manchester(bits_para_transmitir, amostras_por_bit=amostras)
        elif mod_digital == "Bipolar":
            sinal_digital = codificador_bipolar(bits_para_transmitir, amostras_por_bit=amostras)
        
        # Atualiza interface
        self.atualizar_graficos(mod_digital, mod_portadora, sinal_digital, bits_para_transmitir)
        
        # Receptor provisorio
        self.atualizar_("Mensagem Enviada com Sucesso", texto, str(bits_para_transmitir))

    def criar_grafico_inicial(self):
        # ==Cria os gráficos matplotlib==
        # Grafico mod. digital
        self.fig_digital = Figure(figsize=(5, 3), dpi=100)
        self.ax_digital = self.fig_digital.add_subplot(111)
        self.ax_digital.set_title("Modulação Digital")
        self.ax_digital.grid(True)
        
        self.canvas_digital = FigureCanvasTkAgg(self.fig_digital, master=self.plot_digital)
        self.canvas_digital.draw()
        self.canvas_digital.get_tk_widget().pack(fill="both", expand=True)

        # Grafico mod. portadora
        self.fig_portadora = Figure(figsize=(5, 3), dpi=100)
        self.ax_portadora = self.fig_portadora.add_subplot(111)
        self.ax_portadora.set_title("Modulação por Portadora")
        self.ax_portadora.grid(True)
        
        self.canvas_portadora = FigureCanvasTkAgg(self.fig_portadora, master=self.plot_portadora)
        self.canvas_portadora.draw()
        self.canvas_portadora.get_tk_widget().pack(fill="both", expand=True)

    def atualizar_graficos(self, tipo_digital, tipo_portadora, sinal_digital_y, bits_originais):
        # Atualiza Digital
        self.ax_digital.clear()
        self.ax_digital.plot(sinal_digital_y, color="cyan", linewidth=1.5)
        self.ax_digital.set_title(f"Modulação Digital: {tipo_digital}")
        self.ax_digital.grid(True, alpha=0.3)
        self.ax_digital.set_ylim(-1.5, 1.5) 
        self.canvas_digital.draw()

        # Atualiza Portadora (Simulado por enquanto)
        self.ax_portadora.clear()
        x_port = np.linspace(0, len(bits_originais), len(sinal_digital_y))
        y_port = np.sin(x_port * 20) 
        self.ax_portadora.plot(x_port, y_port, color="orange")
        self.ax_portadora.set_title(f"Modulação por Portadora: {tipo_portadora} (Exemplo)")
        self.ax_portadora.grid(True)
        self.canvas_portadora.draw()

    def atualizar_(self, status, text, bits):
        # ==Atualiza os widgets do frame 'Receptor' com os novos dados==
        # Atualiza o Status
        self.status.configure(text=status)
        
        # Atualiza o texto recebido
        self.texto_recebido.configure(text=f"Texto Recebido: {text}")
        
        # Atualiza a caixa de bits
        self.bits_recebidos_texto.configure(state="normal")
        self.bits_recebidos_texto.delete("1.0", "end") # Limpa o conteudo antigo
        self.bits_recebidos_texto.insert("1.0", bits)  # Insere o novo conteudo
        self.bits_recebidos_texto.configure(state="disabled") # Bloqueia novamente

if __name__ == "__main__":
    app = App()
    app.mainloop()