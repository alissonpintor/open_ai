import streamlit as st
import dotenv

from core.handlers.pdf_file_handler import PdfFileHandler
from core.models.files import Files
from core.models.columns import Columns
from api.chatgpt.get_columns_names import GetColumnsNamesService
from presentation.main import Main


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
        if 'colunas' in st.session_state:
            del st.session_state['colunas']
        st.session_state.base64_images.clear()

if __name__ == '__main__':
    image_handler: PdfFileHandler = PdfFileHandler()
    get_columns_service: GetColumnsNamesService = GetColumnsNamesService()

    initialize()
    base64_images: Files = st.session_state.base64_images
    columns: Columns = st.session_state.colunas_selecionadas

    is_columns_generated: bool = 'colunas' in st.session_state
    
    st.file_uploader('Selecione o pdf a ser convertido', 'pdf', disabled=is_columns_generated, key='pdf_file_uploaded', on_change=has_pdf_uploaded)
    
    if not is_columns_generated and st.session_state.pdf_file_uploaded is not None:
        with st.spinner('Convertendo o pdf...'):
            print('Convertendo imagens...')
            pdf_file_uploaded = st.session_state.pdf_file_uploaded
            pdf_file_uploaded = pdf_file_uploaded.getvalue()
            base64_images.add(image_handler.process_pdf_to_image(pdf_file_uploaded))
        
    if not is_columns_generated and base64_images.has_files():
        with st.spinner('Enviando para a AI...'):
            print('Enviando para o ChatGPT...')

            base64_image = base64_images.get_first()
            column_names = get_columns_service.execute(base64_image)

            if column_names:
                st.session_state['colunas'] = column_names['colunas']
    
    if 'colunas' in st.session_state:
        st.write('Selecione a colunas correspondentes aos campos a seguir:')
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            referencia = st.selectbox('Referencia', st.session_state['colunas'])
        
        with col2:
            descricao = st.selectbox('Descricão', st.session_state['colunas'])
        
        with col3:
            quantidade = st.selectbox('Qtdade', st.session_state['colunas'])
        
        with col4:
            vlr_unitario = st.selectbox('Vlr.Unitário', st.session_state['colunas'])
    
    if 1==2:
        system_message = {
            'role': 'assistant',
            'content': '''
                Você recebe uma imagem que possui textos com uma tabela de itens e deve retornar o um json contendo 
                os itens dessa tabela seguindo o exemplo entre ####:

                ####
                {
                    "itens": [
                        {
                            "Referencia": "50300201",
                            "Descrição": "DIATEX PINTA MAIS BRANCO NEVE 3,6L",
                            "Qtde": "48",
                            "Preço Líq": "24,59"                        },
                        {
                            "Referencia": "11100104",
                            "Descrição": "SELADORA CONCENTRADAINCOLOR 900 ML",
                            "Qtde": "60",
                            "Preço Líq": "16,51"
                        }
                    ]
                }
                ####

                Na imagem Referencia se chama ###, Descrição se chama ###, Qtde se chama ###,
                Preço Líq se chama #### . retorne o json desses dados.
            '''
        }