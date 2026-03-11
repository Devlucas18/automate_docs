import customtkinter as ctk

class Interface:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("500x400")

        combobox_tipo = ctk.CTkComboBox(self.root, values=["Notebook Recebimento",
     "Notebook Devolução", "Celular Recebimento", "Celular Devolução", 
     "Celular + Chip Recebimento", "Chip Recebimento", "Tablet Devolução"])
        combobox_tipo.pack(pady=20)

        entry = ctk.CTkEntry(self.root, placeholder_text="Digite o nome do arquivo de imagem")
        entry.pack(pady=10)

        botao_gerar = ctk.CTkButton(self.root, text="Gerar Termo", corner_radius=10)
        botao_gerar.place(relx=0.5, rely=0.5, anchor="center")

        

        self.root.mainloop()

        

if __name__ == "__main__":
    Interface()