import os
import io
from pydoc import doc
from PIL import Image
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from service.imagem import imagem


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GeradorTermo:
    TEMPLATES = {
        "Notebook Recebimento": os.path.join(BASE_DIR, "template", "template_recebimento_notebook.docx"),
        "Notebook Devolução": os.path.join(BASE_DIR, "template", "template_devolucao_notebook.docx"),
        "Celular Recebimento": os.path.join(BASE_DIR, "template", "template_recebimento_celular.docx"),
        "Celular Devolução": os.path.join(BASE_DIR, "template", "template_devolucao_celular.docx"),
        "Celular + Chip Recebimento": os.path.join(BASE_DIR, "template", "template_recebimento_celular_chip.docx"),
        "Chip Recebimento": os.path.join(BASE_DIR, "template", "template_recebimento_chip.docx"),
        "Tablet Devolução": os.path.join(BASE_DIR, "template", "template_devolucao_tablet.docx"),
    }

    def __init__(self, dados: dict):
        tipo = dados.get("tipo_de_termo")

        if tipo not in self.TEMPLATES:
            raise ValueError(f"Tipo inválido: {tipo}")

        self.dados = dados
        self.tipo = tipo

    def gerar_doc(self):
        arquivo_template = self.TEMPLATES[self.tipo]

        if not os.path.exists(arquivo_template):
            raise FileNotFoundError(f"Template não encontrado: {arquivo_template}")

        doc = DocxTemplate(arquivo_template)

        dados_render = self.dados.copy()

        # Processar a imagem
        image_bytes = dados_render.get("img")
        if image_bytes:
            image_stream = io.BytesIO(image_bytes)
            dados_render["img"] = InlineImage(doc, image_stream, width=Mm(80))
        else:
            dados_render["img"] = ""




        doc.render(dados_render)

        nome = self.dados.get("nome", "SemNome").replace(" ", "_")
        doc.save(f"gerados\\Termo_{self.tipo}_{nome}.docx")