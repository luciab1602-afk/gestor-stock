import streamlit as st
import pandas as pd

from codigo1 import cargar_productos, productos_para_tabla

st.set_page_config(page_title="Gestor de Stock", layout="wide")

st.title("📦 Gestor de Stock")

productos = cargar_productos("alimentos.csv")

st.write(f"🧾 Productos cargados: **{len(productos)}**")

tabla = productos_para_tabla(productos)
df = pd.DataFrame(tabla)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
