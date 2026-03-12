import customtkinter as ctk

class Interface:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("500x400")

        ctk.set_appearance_mode("dark")


        ctk.CTkLabel(self.root, text="Gerador de Termos", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        #FRAME_NOME
        frame_nome = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_nome.pack(pady=(0, 10))
        ctk.CTkLabel(frame_nome, text="Nome:  ").pack(side="left", pady=(0, 8))
        nome = ctk.CTkEntry(frame_nome, placeholder_text="Digite o nome do funcionário")
        nome.pack(side="left", pady=(0, 8))

        #FRAME_CPF
        frame_cpf = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_cpf.pack(pady=(0, 10))
        ctk.CTkLabel(frame_cpf, text="CPF:  ").pack(side="left", pady=(0, 8))
        cpf = ctk.CTkEntry(frame_cpf, placeholder_text="Digite o CPF do funcionário")
        cpf.pack(side="left", pady=(0, 8))

        #FRAME_DATA
        frame_data = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_data.pack(pady=(0, 10))
        ctk.CTkLabel(frame_data, text="  DIA/ MÊS/ ANO:  ").pack(side="left", pady=(0, 8))
        dia = ctk.CTkEntry(frame_data, placeholder_text="Digite o dia")
        dia.pack(side="left", pady=(0, 8))
        mes = ctk.CTkEntry(frame_data, placeholder_text="Digite o mês")
        mes.pack(side="left", pady=(0, 8))
        ano = ctk.CTkEntry(frame_data, placeholder_text="Digite o ano")
        ano.pack(side="left", pady=(0, 8))

        combobox_tipo = ctk.CTkComboBox(self.root, values=["Notebook Recebimento",
        "Notebook Devolução", "Celular Recebimento", "Celular Devolução", 
        "Celular + Chip Recebimento", "Chip Recebimento", "Tablet Devolução"])
        combobox_tipo.pack(pady=(0, 10))

        botao_gerar = ctk.CTkButton(self.root, text="Gerar Termo", corner_radius=10)
        botao_gerar.pack(pady=(0, 10))
        tipo = combobox_tipo.get()        

        self.root.mainloop()

if __name__ == "__main__":
    Interface()