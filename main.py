#RECEBIMENTO DE DADOS E CHAMAR FUNÇÃO GERAR_DOC
#TRATAMENTO DE DADOS
import os
from service.gerador import GeradorTermo

DADOS = {
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "modelo": "Modelo A",
    "serial": "SN123456789",
    "dia": "01",
    "mes": "Janeiro",
    "ano": "2024",
    "recebido_por": "Maria Oliveira",
    "observações": "Nenhuma",
    "tipo_de_termo": "Celular Devolução"
}
gerador = GeradorTermo(DADOS)
gerador.gerar_doc()