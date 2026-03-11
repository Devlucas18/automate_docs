import tkinter as tk
from tkinter import filedialog

class interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Termos")
        self.root.geometry("500x750")
        self.root.configure(bg="#2d2d2d")

        # Main frame for the form, mimicking the image style
        form_wrapper = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        form_wrapper.pack(expand=True, fill="both", padx=20, pady=20)

        # --- Title ---
        title_label = tk.Label(form_wrapper, text="Termos", font=("Arial", 24, "bold"), bg="white", anchor="w")
        title_label.pack(fill="x", pady=(0, 20))

        # --- Scrollable Frame for Fields ---
        canvas = tk.Canvas(form_wrapper, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(form_wrapper, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Form Fields ---
        self.fields = {}

        # Helper to create a label and an entry widget
        def create_field(parent, label_text, row):
            label = tk.Label(parent, text=label_text, font=("Arial", 10), bg="white", anchor="w")
            label.grid(row=row, column=0, sticky="w", pady=(5, 2))
            
            entry = tk.Entry(parent, font=("Arial", 12), bg="#f0f0f0", relief="flat", highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor="#d9534f", bd=5)
            entry.grid(row=row + 1, column=0, sticky="ew", pady=(0, 10))
            
            self.fields[label_text.lower().replace(" ", "_").replace("ç", "c").replace("ã", "a")] = entry
            return entry

        # Row counter
        current_row = 0

        # Create all the fields
        create_field(scrollable_frame, "Nome", current_row); current_row += 2
        create_field(scrollable_frame, "CPF", current_row); current_row += 2
        create_field(scrollable_frame, "Cargo", current_row); current_row += 2
        
        # Observações (Text widget)
        obs_label = tk.Label(scrollable_frame, text="Observações", font=("Arial", 10), bg="white", anchor="w")
        obs_label.grid(row=current_row, column=0, sticky="w", pady=(5, 2)); current_row += 1
        self.obs_text = tk.Text(scrollable_frame, font=("Arial", 12), bg="#f0f0f0", relief="flat", height=4, highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor="#d9534f", bd=5)
        self.obs_text.grid(row=current_row, column=0, sticky="ew", pady=(0, 10)); current_row += 1
        self.fields["observacoes"] = self.obs_text

        # Checkbox for "com ou sem carregador"
        self.carregador_var = tk.BooleanVar()
        carregador_check = tk.Checkbutton(scrollable_frame, text="Com carregador", variable=self.carregador_var, font=("Arial", 10), bg="white", activebackground="white", anchor="w", relief="flat")
        carregador_check.grid(row=current_row, column=0, sticky="w", pady=(5, 10)); current_row += 1
        self.fields["com_ou_sem_carregador"] = self.carregador_var

        create_field(scrollable_frame, "Modelo", current_row); current_row += 2
        create_field(scrollable_frame, "IMEI", current_row); current_row += 2
        create_field(scrollable_frame, "Serial", current_row); current_row += 2
        create_field(scrollable_frame, "Etiqueta", current_row); current_row += 2
        create_field(scrollable_frame, "Linha", current_row); current_row += 2
        create_field(scrollable_frame, "ICCID", current_row); current_row += 2
        create_field(scrollable_frame, "Pacote de dados", current_row); current_row += 2

        # Date fields (dia, mes, ano)
        date_label = tk.Label(scrollable_frame, text="Data (DD/MM/AAAA)", font=("Arial", 10), bg="white", anchor="w")
        date_label.grid(row=current_row, column=0, sticky="w", pady=(5, 2)); current_row += 1
        
        date_frame = tk.Frame(scrollable_frame, bg="white")
        date_frame.grid(row=current_row, column=0, sticky="ew", pady=(0, 10)); current_row += 1
        
        self.dia_entry = tk.Entry(date_frame, font=("Arial", 12), bg="#f0f0f0", relief="flat", width=4, highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor="#d9534f", bd=5)
        self.dia_entry.pack(side="left", fill="x", expand=True)
        self.fields["dia"] = self.dia_entry
        
        tk.Label(date_frame, text="/", bg="white", font=("Arial", 12)).pack(side="left", padx=5)

        self.mes_entry = tk.Entry(date_frame, font=("Arial", 12), bg="#f0f0f0", relief="flat", width=4, highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor="#d9534f", bd=5)
        self.mes_entry.pack(side="left", fill="x", expand=True)
        self.fields["mes"] = self.mes_entry

        tk.Label(date_frame, text="/", bg="white", font=("Arial", 12)).pack(side="left", padx=5)

        self.ano_entry = tk.Entry(date_frame, font=("Arial", 12), bg="#f0f0f0", relief="flat", width=6, highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor="#d9534f", bd=5)
        self.ano_entry.pack(side="left", fill="x", expand=True)
        self.fields["ano"] = self.ano_entry

        # Image selection button
        img_label = tk.Label(scrollable_frame, text="Imagem do equipamento", font=("Arial", 10), bg="white", anchor="w")
        img_label.grid(row=current_row, column=0, sticky="w", pady=(10, 2)); current_row += 1
        
        self.img_path = tk.StringVar()
        self.img_path.set("Nenhuma imagem selecionada")
        
        img_button = tk.Button(scrollable_frame, text="Selecionar Imagem", command=self.select_image, relief="flat", bg="#e0e0e0", fg="black", font=("Arial", 10))
        img_button.grid(row=current_row, column=0, sticky="w", pady=(0, 5)); current_row += 1
        
        img_path_label = tk.Label(scrollable_frame, textvariable=self.img_path, font=("Arial", 8), bg="white", fg="gray", wraplength=350, justify="left")
        img_path_label.grid(row=current_row, column=0, sticky="w", pady=(0, 10)); current_row += 1
        self.fields["img"] = self.img_path

        scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Submit Button ---
        submit_button = tk.Button(form_wrapper, text="Submit", font=("Arial", 14, "bold"), bg="#d9534f", fg="white", relief="flat", padx=20, pady=10, activebackground="#c9302c", activeforeground="white")
        submit_button.pack(pady=(20, 0))

    def select_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
        )
        if path:
            self.img_path.set(path)








if __name__ == "__main__":
    root = tk.Tk()
    interface(root)
    root.mainloop()