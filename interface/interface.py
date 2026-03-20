import customtkinter as ctk
from service.gerador import GeradorTermo
from service.imagepastefield import ImagePasteField

CAMPOS_POR_TIPO = {
    "Notebook Recebimento":       ["Cargo", "Observação", "Marca", "Modelo", "Configuração", "Etiqueta", "Patrimônio", "Serial Number", "imagem"],
    "Notebook Devolução":         ["Modelo", "Configuração", "Etiqueta", "Serial", "Observação", "Recebido Por"],
    "Celular Recebimento":        ["Cargo", "Observação", "Modelo Celular", "Serial", "IMEI", "Etiqueta", "imagem"],
    "Celular Devolução":          ["Modelo", "Serial", "Recebido Por"],
    "Celular + Chip Recebimento": ["Cargo", "Observação", "Modelo", "IMEI", "Serial", "Etiqueta", "Linha", "ICCID", "Pacote de Dados", "imagem"],
    "Chip Recebimento":           ["Serial Chip", "Linha", "Pacote de Dados"],
    "Tablet Devolução":           ["Modelo", "Etiqueta", "Serial", "Recebido Por"],
}


class Interface:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("500x500")
        ctk.set_appearance_mode("dark")

        self.entries = {} 

        ctk.CTkLabel(self.root, text="Gerador de Termos", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
        ctk.CTk
    
        self.imagem_bytes: bytes | None = None

        # FRAME_NOME
        frame_nome = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_nome.pack(pady=(0, 10))
        ctk.CTkLabel(frame_nome, text="Nome:  ").pack(side="left")
        self.nome = ctk.CTkEntry(frame_nome, placeholder_text="Digite o nome do funcionário")
        self.nome.pack(side="left")

        # FRAME_CPF
        frame_cpf = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_cpf.pack(pady=(0, 10))
        ctk.CTkLabel(frame_cpf, text="CPF:  ").pack(side="left")
        self.cpf = ctk.CTkEntry(frame_cpf, placeholder_text="Digite o CPF do funcionário")
        self.cpf.pack(side="left")

        # FRAME_DATA
        frame_data = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_data.pack(pady=(0, 10))
        ctk.CTkLabel(frame_data, text="DIA / MÊS / ANO:  ").pack(side="left")
        self.dia = ctk.CTkEntry(frame_data, placeholder_text="Dia", width=60)
        self.dia.pack(side="left", padx=(0, 4))
        self.mes = ctk.CTkEntry(frame_data, placeholder_text="Mês", width=60)
        self.mes.pack(side="left", padx=(0, 4))
        self.ano = ctk.CTkEntry(frame_data, placeholder_text="Ano", width=80)
        self.ano.pack(side="left")

        # COMBOBOX
        self.combobox_tipo = ctk.CTkComboBox(
            self.root,
            values=list(CAMPOS_POR_TIPO.keys()),
            command=self.atualizar_frames   
        )
        self.combobox_tipo.pack(pady=(0, 10))

        self.frame_dinamico = ctk.CTkScrollableFrame(self.root, fg_color="transparent", height=200)
        self.frame_dinamico.pack(pady=(0, 10), fill="x", padx=20)

        # BOTÃO
        botao_gerar = ctk.CTkButton(self.root, text="Gerar Termo", corner_radius=10, command=self.gerar)
        botao_gerar.pack(pady=(0, 10))
        
        self.atualizar_frames(self.combobox_tipo.get())

        self.root.mainloop()
    def receber_imagem(self, dados: bytes):
        self.imagem_bytes = dados

    def atualizar_frames(self, tipo):

        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()

        self.entries = {}  

        campos = CAMPOS_POR_TIPO.get(tipo, [])

        for campo in campos:
            if campo.lower() == "imagem":  # ← cobre "imagem", "Imagem", "imgem" não
                image_field = ImagePasteField(self.frame_dinamico, on_image_ready=self.receber_imagem)
                image_field.pack(padx=40, pady=10)
                ctk.CTkButton(self.frame_dinamico, text="Limpar Imagem", command=image_field.limpar).pack()
                continue

            frame = ctk.CTkFrame(self.frame_dinamico, fg_color="transparent")
            frame.pack(pady=(0, 8))

            ctk.CTkLabel(frame, text=f"{campo}:  ", width=140, anchor="e").pack(side="left")
            entry = ctk.CTkEntry(frame, placeholder_text=f"Digite {campo.lower()}")
            entry.pack(side="left")

            self.entries[campo] = entry  

    def gerar(self):
        dados = {
            "nome": self.nome.get(),
            "cpf": self.cpf.get(),
            "dia": self.dia.get(),
            "mês": self.mes.get(),
            "ano": self.ano.get(),
            "tipo_de_termo": self.combobox_tipo.get(),
            "imagem": self.imagem_bytes
        }
        for campo, entry in self.entries.items():
            dados[campo] = entry.get()  

        print(dados)
        gerador = GeradorTermo(dados)
        gerador.gerar_doc() 


if __name__ == "__main__":
    Interface()