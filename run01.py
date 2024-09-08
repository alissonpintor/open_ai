import streamlit as st
import tabula
from mitosheet.streamlit.v1 import spreadsheet


df = tabula.read_pdf('arquivos/pedido_iquine.pdf', pages='all')

if __name__ == '__main__':
    st.set_page_config(layout='wide')
    new_df, code = spreadsheet(*df, df_names=[f'df{n}' for n in range(0, len(df))])
    st.code(code)