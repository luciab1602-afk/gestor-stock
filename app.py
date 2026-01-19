import streamlit as st
import pandas as pd

from codigo1 import cargar_productos, productos_para_tabla, calcular_stock_total

# Configuración de la página
st.set_page_config(
    page_title="Gestor de Stock",
    layout="wide"
)

st.title("📦 Gestor de Stock")

# Cargar productos
productos = cargar_productos("alimentos.csv")

st.write(f"🧾 Productos cargados: **{len(productos)}**")

# Mostrar tabla
tabla = productos_para_tabla(productos)
df = pd.DataFrame(tabla)

st.subheader("📋 Detalle de productos")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Stock total
st.subheader("📊 Stock total")
total = calcular_stock_total(productos)
st.metric("Stock total disponible (kg)", f"{total:.2f}")

        