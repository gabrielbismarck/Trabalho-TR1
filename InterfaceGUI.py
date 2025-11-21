import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from Utils import bits_list_formatter

from Transmissor import Transmissor
from Receptor import Receptor
from Meio import MeioDeComunicacao

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Camada Física e de Enlace - TR1")
        self.geometry("1400x950") # Aumentei um pouco a altura

        self.tx = Transmissor(amostras_por_bit=10)
        self.meio = MeioDeComunicacao()
        self.rx = Receptor(amostras_por_bit=10)

        # --- LAYOUT ---
        self.control_frame = ctk.CTkFrame(self, width=350) 
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.control_frame.pack_propagate(False)

        self.plot_container = ctk.CTkFrame(self) 
        self.plot_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # 1. Entrada
        self.entry_label = ctk.CTkLabel(self.control_frame, text="Texto a ser transmitido:", font=("Arial", 14, "bold"))
        self.entry_label.pack(pady=(10, 5), padx=10, anchor="w")
        self.text_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Digite sua mensagem...")
        self.text_entry.pack(pady=5, padx=10, fill="x")

        # 2. Modulação Digital
        self.mod_digital_frame = ctk.CTkFrame(self.control_frame)
        self.mod_digital_frame.pack(pady=10, padx=10, fill="x", anchor="w")
        self.mod_digital_label = ctk.CTkLabel(self.mod_digital_frame, text="Modulação Digital")
        self.mod_digital_label.pack(pady=5, padx=10, anchor="w")
        self.mod_digital_var = ctk.StringVar(value="NRZ")
        ctk.CTkRadioButton(self.mod_digital_frame, text="NRZ-Polar", variable=self.mod_digital_var, value="NRZ").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.mod_digital_frame, text="Manchester", variable=self.mod_digital_var, value="Manchester").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.mod_digital_frame, text="Bipolar", variable=self.mod_digital_var, value="Bipolar").pack(pady=5, padx=20, anchor="w")

        # 3. Portadora
        self.mod_portadora_frame = ctk.CTkFrame(self.control_frame)
        self.mod_portadora_frame.pack(pady=10, padx=10, fill="x", anchor="w")
        self.mod_portadora_label = ctk.CTkLabel(self.mod_portadora_frame, text="Modulação por Portadora")
        self.mod_portadora_label.pack(pady=5, padx=10, anchor="w")
        self.mod_portadora_var = ctk.StringVar(value="ASK")
        ctk.CTkRadioButton(self.mod_portadora_frame, text="ASK", variable=self.mod_portadora_var, value="ASK").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.mod_portadora_frame, text="FSK", variable=self.mod_portadora_var, value="FSK").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.mod_portadora_frame, text="PSK (QPSK)", variable=self.mod_portadora_var, value="PSK").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.mod_portadora_frame, text="16-QAM", variable=self.mod_portadora_var, value="16-QAM").pack(pady=5, padx=20, anchor="w")

        # 4. Enquadramento
        self.enquadramento_frame = ctk.CTkFrame(self.control_frame)
        self.enquadramento_frame.pack(pady=10, padx=10, fill="x", anchor="w")
        self.enquadramento_label = ctk.CTkLabel(self.enquadramento_frame, text="Enquadramento")
        self.enquadramento_label.pack(pady=5, padx=10, anchor="w")
        self.enquadramento_var = ctk.StringVar(value="Contagem de Caracteres")
        ctk.CTkRadioButton(self.enquadramento_frame, text="Contagem de Caracteres", variable=self.enquadramento_var, value="Contagem de Caracteres").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.enquadramento_frame, text="Inserção de Bytes", variable=self.enquadramento_var, value="Inserção de Bytes").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.enquadramento_frame, text="Inserção de Bits", variable=self.enquadramento_var, value="Inserção de Bits").pack(pady=5, padx=20, anchor="w")

        # 5. Erros
        self.erros_frame = ctk.CTkFrame(self.control_frame)
        self.erros_frame.pack(pady=10, padx=10, fill="x", anchor="w")
        self.erros_label = ctk.CTkLabel(self.erros_frame, text="Detecção/Correção de Erros")
        self.erros_label.pack(pady=5, padx=10, anchor="w")
        self.erros_var = ctk.StringVar(value="Bit de Paridade Par")
        ctk.CTkRadioButton(self.erros_frame, text="Bit de Paridade Par", variable=self.erros_var, value="Bit de Paridade Par").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.erros_frame, text="Checksum", variable=self.erros_var, value="Checksum").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.erros_frame, text="CRC-32", variable=self.erros_var, value="CRC-32").pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.erros_frame, text="Hamming", variable=self.erros_var, value="Hamming").pack(pady=5, padx=20, anchor="w")

        # 6. Ruído
        self.ruido_frame = ctk.CTkFrame(self.control_frame)
        self.ruido_frame.pack(pady=10, padx=10, fill="x", anchor="w")
        self.ruido_label = ctk.CTkLabel(self.ruido_frame, text="Controle de Ruído (Gaussiano)", font=("Arial", 12, "bold"))
        self.ruido_label.pack(pady=5, padx=10, anchor="w")
        self.sigma_label = ctk.CTkLabel(self.ruido_frame, text="Sigma (σ): 0.0")
        self.sigma_label.pack(pady=2, padx=10, anchor="w")
        self.slider_sigma = ctk.CTkSlider(self.ruido_frame, from_=0, to=2, number_of_steps=20, command=self.update_sigma_label)
        self.slider_sigma.set(0)
        self.slider_sigma.pack(pady=5, padx=10, fill="x")

        # Botão
        self.botao_transmitir = ctk.CTkButton(self.control_frame, text="TRANSMITIR", command=self.transmitir, font=("Arial", 14, "bold"), fg_color="green", hover_color="darkgreen")
        self.botao_transmitir.pack(pady=20, padx=10, side="bottom", fill="x")

        # --- ÁREA DIREITA ---
        self.plot_digital = ctk.CTkFrame(self.plot_container)
        self.plot_digital.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.plot_portadora = ctk.CTkFrame(self.plot_container)
        self.plot_portadora.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.frame_receptor = ctk.CTkFrame(self.plot_container)
        self.frame_receptor.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Status e Contador de Erros
        self.status_frame = ctk.CTkFrame(self.frame_receptor, fg_color="transparent")
        self.status_frame.pack(fill="x", pady=5, padx=10)
        
        self.status = ctk.CTkLabel(self.status_frame, text="Status: Aguardando...", font=("Arial", 12, "italic"))
        self.status.pack(side="left")
        
        self.label_ber = ctk.CTkLabel(self.status_frame, text="Erros de Bit: 0", font=("Arial", 12, "bold"), text_color="white")
        self.label_ber.pack(side="right")

        self.texto_recebido = ctk.CTkLabel(self.frame_receptor, text="Texto Recebido: -", font=("Arial", 14, "bold"))
        self.texto_recebido.pack(pady=5, padx=10, anchor="w")
        
        self.label_bits = ctk.CTkLabel(self.frame_receptor, text="Fluxo de Bits (TX vs RX):")
        self.label_bits.pack(pady=(5,0), padx=10, anchor="w")
        
        self.bits_recebidos_texto = ctk.CTkTextbox(self.frame_receptor, height=80)
        self.bits_recebidos_texto.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Configura Tag para texto vermelho (Erro) no widget subjacente do Tkinter
        self.bits_recebidos_texto._textbox.tag_config("erro", foreground="red", font=("Courier", 12, "bold"))
        self.bits_recebidos_texto._textbox.tag_config("normal", foreground="white", font=("Courier", 12))
        self.bits_recebidos_texto.configure(state="disabled")

        self.criar_grafico_inicial()

    def update_sigma_label(self, value):
        self.sigma_label.configure(text=f"Sigma (σ): {round(value, 2)}")

    def transmitir(self):
        texto_input = self.text_entry.get()
        mod_digital = self.mod_digital_var.get()
        mod_portadora = self.mod_portadora_var.get()
        enquadramento = self.enquadramento_var.get()
        tipo_erro = self.erros_var.get()
        sigma = self.slider_sigma.get()

        self.status.configure(text="Processando...", text_color="white")
        self.update_idletasks()

        try:
            #TX
            sinal_tx, bits_enviados = self.tx.processar(texto_input, mod_digital, enquadramento, tipo_erro)
            
            #Meio (Ruído)
            sinal_com_ruido = self.meio.transmitir(sinal_tx, sigma)
            
            #RX
            texto_recuperado, bits_rx_raw = self.rx.decodificar(sinal_com_ruido, mod_digital, enquadramento, tipo_erro)
            bits_recebidos = list(bits_rx_raw)

            # ATUALIZA GUI (GRÁFICOS E LABELS)
            self.atualizar_graficos(mod_digital, mod_portadora, sinal_com_ruido, bits_enviados)
            
            if "[Erro" in texto_recuperado:
                self.status.configure(text="ERRO DETECTADO PELA CAMADA DE ENLACE", text_color="red")
            else:
                self.status.configure(text="Recepção com Sucesso", text_color="#00FF00")

            self.texto_recebido.configure(text=f"Texto Recebido: {texto_recuperado}")

            #EXIBIÇÃO DOS BITS (SIMPLIFICADA)
            self.bits_recebidos_texto.configure(state="normal")
            self.bits_recebidos_texto.delete("1.0", "end")
            
            str_bits = "".join(map(str, bits_recebidos))
            str_bits = " ".join([str_bits[i:i+8] for i in range(0, len(str_bits), 8)])

            self.bits_recebidos_texto.insert("1.0", str_bits)
            self.bits_recebidos_texto.configure(state="disabled")

        except Exception as e:
            self.status.configure(text=f"Erro Crítico: {str(e)}", text_color="red")
            print(e)

    def criar_grafico_inicial(self):
        self.fig_digital = Figure(figsize=(5, 2.5), dpi=100)
        self.ax_digital = self.fig_digital.add_subplot(111)
        self.ax_digital.grid(True)
        self.ax_digital.set_title("Aguardando Sinal...")
        self.canvas_digital = FigureCanvasTkAgg(self.fig_digital, master=self.plot_digital)
        self.canvas_digital.draw()
        self.canvas_digital.get_tk_widget().pack(fill="both", expand=True)

        self.fig_portadora = Figure(figsize=(5, 2.5), dpi=100)
        self.ax_portadora = self.fig_portadora.add_subplot(111)
        self.ax_portadora.grid(True)
        self.ax_portadora.set_title("Aguardando Portadora...")
        self.canvas_portadora = FigureCanvasTkAgg(self.fig_portadora, master=self.plot_portadora)
        self.canvas_portadora.draw()
        self.canvas_portadora.get_tk_widget().pack(fill="both", expand=True)

    def atualizar_graficos(self, tipo_digital, tipo_portadora, sinal_y, bits_referencia):
        self.ax_digital.clear()
        self.ax_digital.plot(sinal_y, color="#00ffff", linewidth=1.2) 
        self.ax_digital.set_title(f"RX (Sinal Digital + Ruído): {tipo_digital}")
        self.ax_digital.grid(True, alpha=0.3)
        self.ax_digital.set_ylim(-3.0, 3.0) 
        self.canvas_digital.draw()
        
        # Placeholder Portadora
        self.ax_portadora.clear()
        x_port = np.linspace(0, len(sinal_y), len(sinal_y))
        y_port = np.sin(x_port * 0.1) * (1 if len(sinal_y) > 0 else 0)
        self.ax_portadora.plot(x_port, y_port, color="#ffaa00", linewidth=1) 
        self.ax_portadora.set_title(f"Portadora ({tipo_portadora}) - [Simulação]")
        self.ax_portadora.grid(True, alpha=0.3)
        self.canvas_portadora.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()