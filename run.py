import tabula
import streamlit as st
import pandas as pd

pdf_path: str = 'arquivos/pedido_iquine.pdf'
df: pd.DataFrame | None = None


dfs: list[pd.DataFrame] = tabula.read_pdf( # type: ignore
    input_path=pdf_path, 
    pages='1',
    area=[
        [30, 10, 95, 100]
    ],
    relative_area=True,
    multiple_tables=False,
    #relative_columns=True,
    #columns=[20, 48, 54, 58, 65, 75, 86, 95],
)

if dfs:
    df = dfs[0]

if len(dfs) > 1 and df is not None:
    for dff in dfs[1:]:
        df = pd.concat([df, dff])

if df is not None and not df.empty:
    st.set_page_config(
        page_title='PDF Extractor',
        layout='wide'
    )
    edited_df = st.data_editor(df, num_rows='dynamic')