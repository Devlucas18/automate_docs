import customtkinter as ctk
from PIL import Image, ImageGrab
from service.imagem import imagem  # sua classe
import io

class ImagePasteField(ctk.CTkFrame):
    """Widget reutilizável para colar imagens."""

    def __init__(self, master, on_image_ready=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_image_ready = on_image_ready  # callback: recebe bytes processados
        self._ctk_img = None

        self.configure(width=400, height=280, corner_radius=12)
        self.pack_propagate(False)

        # Borda tracejada visual (CTkCanvas)
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bg="transparent")
        self.canvas.place(relwidth=1, relheight=1)

        # Hint central
        self.hint = ctk.CTkLabel(
            self,
            text="📋  Ctrl+V para colar imagem",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.hint.place(relx=0.5, rely=0.5, anchor="center")

        # Label para exibir a imagem colada
        self.img_label = ctk.CTkLabel(self, text="")
        self.img_label.place(relx=0.5, rely=0.5, anchor="center")

        # Binds
        self.bind("<Button-1>", lambda e: self.focus_set())
        self.bind("<Control-v>", self._on_paste)
        self.hint.bind("<Button-1>", lambda e: self.focus_set())

    def _on_paste(self, event=None):
        img = ImageGrab.grabclipboard()

        if not isinstance(img, Image.Image):
            self._show_error("Nenhuma imagem no clipboard.")
            return

        # Processa com sua classe
        processado: bytes = imagem(img).process()

        # Reconstrói PIL para exibição no CTkLabel
        img_display = Image.open(io.BytesIO(processado))
        self._exibir(img_display)

        # Dispara callback com os bytes prontos
        if self.on_image_ready:
            self.on_image_ready(processado)

    def _exibir(self, img: Image.Image):
        self.hint.place_forget()

        # Ajusta ao tamanho do frame sem ultrapassar
        frame_w = self.winfo_width() or 400
        frame_h = self.winfo_height() or 280
        img.thumbnail((frame_w - 16, frame_h - 16))

        self._ctk_img = ctk.CTkImage(light_image=img, size=img.size)
        self.img_label.configure(image=self._ctk_img, text="")

    def _show_error(self, msg: str):
        self.hint.configure(text=f"⚠️  {msg}", text_color="red")
        self.hint.place(relx=0.5, rely=0.5, anchor="center")

    def limpar(self):
        """Reseta o campo."""
        self._ctk_img = None
        self.img_label.configure(image=None, text="")
        self.hint.configure(text="📋  Ctrl+V para colar imagem", text_color="gray")
        self.hint.place(relx=0.5, rely=0.5, anchor="center")