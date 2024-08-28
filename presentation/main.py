import streamlit as st
from api.chatgpt.get_columns_names import GetColumnsNamesService

from core.handlers.pdf_file_handler import PdfFileHandler
from core.models.columns import Columns
from core.models.files import Files


class Main:
    __pdf_handler: PdfFileHandler
    __get_columns_service: GetColumnsNamesService
    __base64_images: Files
    __columns: Columns

    def __init__(
            self,
            pdf_handler: PdfFileHandler,
            get_columns_service: GetColumnsNamesService,
            base64_images: Files,
            columns: Columns) -> None:
        self.__pdf_handler = pdf_handler
        self.__get_columns_service = get_columns_service
        self.__base64_images = base64_images
        self.__columns = columns

    def render(self) -> None:
        st.title('Processamento de pedidos')
        self.__render_file_upload()

        if not self.__columns.has_columns_names():
            if st.session_state.pdf_file_uploaded is not None:
                self.__convert_pdf()
            if self.__base64_images.has_files():
                self.__extract_data()
        
        if self.__columns.has_columns_names():
            self.__render_columns_selection()

    def __render_file_upload(self) -> None:
        print(self.__columns.has_columns_names())
        st.file_uploader(
            'Selecione o pdf a ser convertido',
            'pdf', 
            key='pdf_file_uploaded',
            on_change=self.__on_file_upload_change,
            disabled=self.__columns.has_columns_names()
        )
    
    def __render_columns_selection(self) -> None:
        columns_names: list[str | None] = []
        columns_names.append('')
        columns_names.extend(self.__columns.get_pdf_columns_names())
        
        st.markdown('### Selecione on nomes referentes aos seguintes campos')
        
        with st.form('select_columns_form'):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                referencia: str | None = st.selectbox('Referencia', columns_names)
            with col2:
                descricao: str | None = st.selectbox('Descrição', columns_names)
            with col3:
                qtdade: str | None = st.selectbox('Qtdade', columns_names)
            with col4:
                vlr_unitario: str | None = st.selectbox('Vlr.Unitário', columns_names)

            submited = st.form_submit_button('Confirmar')
            if submited:
                submited = False
                if not all([referencia, descricao, qtdade, vlr_unitario]):
                    st.warning('Selecione todos os campos')
                    return
                
                self.__render_diaog()
    
    @st.dialog('Confirme as colunas selecionadas')
    def __render_diaog(self):
        st.write('Tenha certeza de que as colunas estão corretas, pois ao confirmar \
                  sera realizado a extração dos dados usando essas informações.')
        
        col1, col2, _ = st.columns([0.25, 0.25, 0.5])
        with col1:
            if st.button('Confirmar'):
                pass
        with col2:
            if st.button('Cancelar'):
                self.__columns.clear_all()
    
    def __convert_pdf(self) -> None:
        with st.spinner('Convertendo o pdf...'):
            pdf_file_uploaded = st.session_state.pdf_file_uploaded
            pdf_file_uploaded = pdf_file_uploaded.getvalue()            
            images: list[bytes] = self.__pdf_handler.process_pdf_to_image(pdf_file_uploaded)            
            self.__base64_images.add(images)
    
    def __extract_data(self) -> None:
        with st.spinner('Enviando para a analise...'):
            base64_image = self.__base64_images.get_first()
            column_names = self.__get_columns_service.execute(base64_image)
            if column_names:
                self.__columns.add_pdf_columns_names(column_names)
    
    def __on_file_upload_change(self) -> None:
        if st.session_state.pdf_file_uploaded is None:
            self.__columns.clear_all()
            self.__base64_images.clear()