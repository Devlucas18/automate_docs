import os
from docxtpl import DocxTemplate


class GeradorTermo:
    TEMPLATES = {
    "Notebook Recebimento": os.path.join("templates", "template_recebimento_notebook.docx"),
    "Notebook Devolução": os.path.join("templates", "template_devolucao_notebook.docx"),
    "Celular Recebimento": os.path.join("templates", "template_recebimento_celular.docx"),
    "Celular Devolução": os.path.join("templates", "template_devolucao_celular.docx"),
    "Celular + Chip Recebimento": os.path.join("templates", "template_recebimento_celular_chip.docx"),
    "Chip Recebimento": os.path.join("templates", "template_recebimento_chip.docx"),
    "Tablet Devolução": os.path.join("templates", "template_devolucao_tablet.docx"),
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
    doc.render(self.dados)

    nome = self.dados.get("nome", "SemNome").replace(" ", "_")
    doc.save(f"Termo_{self.tipo}_{nome}.docx")
