from typing import Any
import streamlit as st
from streamlit_cropper import st_cropper
from api.chatgpt.get_columns_names import GetColumnsNamesService
from api.chatgpt.get_itens_data import GetItensDataService

from core.handlers.pdf_file_handler import PdfFileHandler
from core.models.columns import Columns
from core.models.files import Files


class Main:

    def __init__(
            self,
            pdf_handler: PdfFileHandler,
            get_columns_service: GetColumnsNamesService,
            get_itens_service: GetItensDataService,
            base64_images: Files,
            columns: Columns) -> None:
        self.__pdf_handler: PdfFileHandler = pdf_handler
        self.__get_columns_service: GetColumnsNamesService = get_columns_service
        self.__get_itens_service: GetItensDataService = get_itens_service
        self.__base64_images: Files = base64_images
        self.__columns: Columns = columns
        self.__cropped_image_list: list = []

        if 'cropped_image_list' not in st.session_state:
            st.session_state.cropped_image_list = []

    def render(self) -> None:
        st.title('Processamento de pedidos')
        self.__render_file_upload()

        if not self.__columns.has_columns_names():
            if st.session_state.pdf_file_uploaded is not None:
                self.__convert_pdf()
            if self.__base64_images.get_image():
                self.__render_crop_image()
            if self.__base64_images.has_files():
                self.__extract_data()
                st.rerun()

        if self.__columns.has_columns_names():
            if not self.__columns.has_all_names():
                self.__render_columns_selection()
            else:
                self.__extract_itens_data()

    def __render_file_upload(self) -> None:
        st.file_uploader(
            label='Selecione o pdf a ser convertido',
            type='pdf', 
            key='pdf_file_uploaded',
            on_change=self.__on_file_upload_change,
            disabled=self.__columns.has_columns_names()
        )
    
    def __render_crop_image(self) -> None:
        if self.__base64_images.get_image() is not None:
            box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')

            aspect_choice: str | None = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
            aspect_dict = {
                "1:1": (1, 1),
                "16:9": (16, 9),
                "4:3": (4, 3),
                "2:3": (2, 3),
                "Free": None
            }
            aspect_ratio = (1, 1)
            if aspect_choice:
                aspect_ratio = aspect_dict.get(aspect_choice, None)
            
            col1, col2 = st.columns(spec=[0.7, 0.3])
            
            with col1:
                col_btn_cortar, col_btn_limpar, col_salvar = st.columns(3)
                with col_btn_cortar:
                    btn_cortar = st.button(label='Cortar', on_click=self.__save_cropped_image)
                with col_btn_limpar:
                    btn_limpar = st.button(label='Limpar Cortes', on_click=self.__clear_cropped_images)
                with col_salvar:
                    btn_salvar = st.button(label='Salvar Cortes', on_click=self.__merge_cropped_images)                 
                cropped_img = st_cropper(
                    img_file=self.__base64_images.get_image(), # type: ignore
                    realtime_update=True,
                    box_color=box_color,
                    aspect_ratio=aspect_ratio,
                    should_resize_image=True     
                )
                st.session_state.cropped_image = cropped_img                

            with col2:
                st.write('Preview')
                #_ = cropped_img.thumbnail((1920,1080)) # type: ignore
                #st.image(cropped_img) # type: ignore

                st.write('Images Cortadas')
                for image in st.session_state.cropped_image_list:
                    st.image(image=image)
    
    def __save_cropped_image(self):
        if st.session_state.cropped_image:
            st.session_state.cropped_image_list.append(
                st.session_state.cropped_image
            )
            #st.session_state.pop('cropped_image')
    
    def __clear_cropped_images(self):
        st.session_state.cropped_image_list.clear()
    
    def __merge_cropped_images(self):
        first_image = st.session_state.cropped_image_list[0]
        new_image =  first_image
        base64_image = self.__pdf_handler.convert_to_base64(first_image)
        self.__base64_images.add(base64_image)
        
        if len(st.session_state.cropped_image_list) > 1:
            for image in st.session_state.cropped_image_list[1:]:
                new_image = self.__pdf_handler.concat_images_vertical(
                    first_image=new_image,
                    second_image=image
                )
                base64_image = self.__pdf_handler.convert_to_base64(image)
                self.__base64_images.add(base64_image)
        
        if new_image:
            self.__base64_images.set_image(new_image)

    
    def __render_columns_selection(self) -> None:
        columns_names: list[str | None] = []
        columns_names.append('')
        columns_names.extend(self.__columns.get_pdf_columns_names())
        
        st.markdown('### Selecione on nomes referentes aos seguintes campos')
        
        with st.form('select_columns_form'):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                referencia: str | None = st.selectbox('Referencia', columns_names, key='referencia')
            with col2:
                descricao: str | None = st.selectbox('Descrição', columns_names, key='descricao')
            with col3:
                qtdade: str | None = st.selectbox('Qtdade', columns_names, key='qtdade')
            with col4:
                vlr_unitario: str | None = st.selectbox('Vlr.Unitário', columns_names, key='vlr_unitario')

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
                self.__columns.referencia = st.session_state.referencia
                self.__columns.descricao = st.session_state.descricao
                self.__columns.quantidade = st.session_state.qtdade
                self.__columns.vlr_unitario = st.session_state.vlr_unitario
                st.rerun()
        with col2:
            if st.button('Cancelar'):
                self.__columns.clear_names()
                st.rerun()
    
    def __convert_pdf(self) -> None:
        with st.spinner('Convertendo o pdf...'):
            pdf_file_uploaded = st.session_state.pdf_file_uploaded
            pdf_file_uploaded = pdf_file_uploaded.getvalue()            
            pdf_image = self.__pdf_handler.process_to_image(pdf_file=pdf_file_uploaded)

            if pdf_image is not None:
                self.__base64_images.set_image(image=pdf_image)       
            
            # base64_image: str | None = self.__pdf_handler.process_pdf_to_image(pdf_file=pdf_file_uploaded)
            # # if base64_image is not None:
            # #     self.__base64_images.add(base64_image)
    
    def __extract_data(self) -> None:
        with st.spinner('Enviando para a analise...'):
            base64_image = self.__base64_images.get_first()
            column_names = self.__get_columns_service.execute(base64_image)
            if column_names:
                self.__columns.add_pdf_columns_names(column_names)
    
    def __extract_itens_data(self):
        with st.spinner('Extraindo itens...'):
            columns: Columns = self.__columns
            base64_images: Files = self.__base64_images
            itens: dict[str, Any] | None = self.__get_itens_service.execute(columns, base64_images)
            if itens:
                st.write(itens)
    
    def __on_file_upload_change(self) -> None:
        if st.session_state.pdf_file_uploaded is None:
            self.__columns.clear_all()
            self.__base64_images.clear()