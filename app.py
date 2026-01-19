import streamlit as st
import pandas as pd
from codigo1 import cargar_productos

st.set_page_config(page_title="Gestor de Stock", layout="wide")

st.title("📦 Gestor de Stock")

# Cargar productos desde el CSV
productos = cargar_productos("alimentos.csv")

st.write(f"🧾 Productos cargados: **{len(productos)}**")

# Convertir a DataFrame
df = pd.DataFrame(productos)

# Calcular stock total por producto
df["stock_total_kg"] = (
    df["kg_por_bolsa"] * df["bolsas_cerradas"] + df["kg_abiertos"]
)

# Mostrar tabla
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


        