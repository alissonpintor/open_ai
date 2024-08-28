import streamlit as st
from core.handlers.pdf_file_handler import PdfFileHandler
from api.chatgpt.get_columns_names import GetColumnsNamesService
from core.models.files import Files
from core.models.columns import Columns


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

    def render(self):
        st.title('Processamento de pedidos')
        self.__render_file_upload()

        if not self.__columns.has_columns_names():
            if st.session_state.pdf_file_uploaded is not None:
                self.__convert_pdf()
            if self.__base64_images.has_files():
                self.__extract_data()

    def __render_file_upload(self) -> None:
        st.file_uploader(
            'Selecione o pdf a ser convertido',
            'pdf', 
            key='pdf_file_uploaded',
            on_change=self.__on_file_upload_change,
            disabled=self.__columns.has_columns_names()
        )
    
    def __convert_pdf(self):
        with st.spinner('Convertendo o pdf...'):
            pdf_file_uploaded = st.session_state.pdf_file_uploaded
            pdf_file_uploaded = pdf_file_uploaded.getvalue()            
            images: list[bytes] = self.__pdf_handler.process_pdf_to_image(pdf_file_uploaded)            
            self.__base64_images.add(images)
    
    def __extract_data(self):
        with st.spinner('Enviando para a analise...'):
            base64_image = self.__base64_images.get_first()
            column_names = self.__get_columns_service.execute(base64_image)
            if column_names:
                self.__columns.add_pdf_columns_names(column_names)
    
    def __on_file_upload_change(self):
        if st.session_state.pdf_file_uploaded is None:
            self.__columns.clear_all()
            self.__base64_images.clear()