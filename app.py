import streamlit as st
import dotenv

from core.handlers.pdf_file_handler import PdfFileHandler
from core.models.files import Files
from core.models.columns import Columns
from api.chatgpt.get_columns_names import GetColumnsNamesService
from api.chatgpt.get_itens_data import GetItensDataService
from view.main import Main


dotenv.load_dotenv()

'''
Processador de pedidos de compras

1) recebe um pdf do usuario
2) processa o pdf e converte as paginas em bytes de jpeg
3) processas as imagens jpeg em base64
4) solicita a IA para extrair os nomes das colunas
5) retorna as colunas para o usuario
6) usuario seleciona as colunas de acordo com o padrão informado
7) solicita a IA para extrair os itens das imagens a partir das colunas selecionadas
8) converte o json retornado pela IA em um objeto
'''


def initialize():
    if 'base64_images' not in st.session_state:
        st.session_state.base64_images = Files()
    if 'colunas_selecionadas' not in st.session_state:
        st.session_state.colunas_selecionadas = Columns()

def has_pdf_uploaded():
    if st.session_state.pdf_file_uploaded is None:
        st.session_state.colunas_selecionadas.clear_all()
        st.session_state.base64_images.clear()

if __name__ == '__main__':
    initialize()
    
    pdf_handler: PdfFileHandler = PdfFileHandler()
    get_columns_service: GetColumnsNamesService = GetColumnsNamesService()
    get_itens_service: GetItensDataService = GetItensDataService()
    base64_images: Files = st.session_state.base64_images
    columns: Columns = st.session_state.colunas_selecionadas

    main = Main(
        pdf_handler,
        get_columns_service,
        get_itens_service,
        base64_images,
        columns
    )
    main.render()