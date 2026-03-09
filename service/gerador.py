import os
from docxtpl import DocxTemplate

# Sobe um nível (de /service/ para a raiz do projeto)
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
        print(f"Procurando template em: {arquivo_template}")
        print(f"Arquivo existe? {os.path.exists(arquivo_template)}")

        if not os.path.exists(arquivo_template):
            raise FileNotFoundError(f"Template não encontrado: {arquivo_template}")

        doc = DocxTemplate(arquivo_template)

        img_path = self.dados.get("img")


        if img_path and os.path.exists(img_path):
            doc.replace_pic("image1.png", img_path)

        doc.render(self.dados)

        nome = self.dados.get("nome", "SemNome").replace(" ", "_")
        doc.save(f"Termo_{self.tipo}_{nome}.docx")
