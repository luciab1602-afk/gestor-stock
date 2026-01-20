import streamlit as st
import pandas as pd
import csv
import re

# =====================
# FUNCIONES
# =====================

def a_int(valor):
    if not valor:
        return 0
    match = re.search(r"\d+", str(valor))
    return int(match.group()) if match else 0


def a_float(valor):
    if not valor:
        return 0.0
    valor = str(valor).replace(",", ".")
    match = re.search(r"\d+(\.\d+)?", valor)
    return float(match.group()) if match else 0.0


def cargar_productos(nombre_archivo):
    productos = []
    with open(nombre_archivo, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            productos.append({
                "prodnombre": fila["prodnombre"],
                "kg_por_bolsa": a_float(fila["kg_por_bolsa"]),
                "bolsas_cerradas": a_int(fila["bolsas_cerradas"]),
                "kg_abiertos": a_float(fila["kg_abiertos"]),
            })
    return productos


def guardar_productos(nombre_archivo, df):
    df.to_csv(nombre_archivo, index=False)


# =====================
# STREAMLIT
# =====================

st.set_page_config(page_title="Gestor de Stock", layout="wide")
st.title("📦 Gestor de Stock – Curioso")

# Inicializar estado
if "df" not in st.session_state:
    productos = cargar_productos("alimentos.csv")
    st.session_state.df = pd.DataFrame(productos)

# Buscador
busqueda = st.text_input("🔍 Buscar producto")

df = st.session_state.df

if busqueda:
    df = df[df["prodnombre"].str.lower().str.contains(busqueda.lower())]

# Editor
df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "prodnombre": st.column_config.TextColumn("Producto"),
        "kg_por_bolsa": st.column_config.NumberColumn("Kg por bolsa", min_value=0.1),
        "bolsas_cerradas": st.column_config.NumberColumn("Bolsas cerradas", min_value=0, step=1),
        "kg_abiertos": st.column_config.NumberColumn("Kg abiertos", min_value=0.0, step=0.1),
    }
)

# Guardar cambios
if st.button("💾 Guardar cambios"):
    st.session_state.df.update(df_editado)
    guardar_productos("alimentos.csv", st.session_state.df)
    st.success("Stock actualizado correctamente")

# Stock total
df["stock_total"] = (
    df["kg_por_bolsa"] * df["bolsas_cerradas"] + df["kg_abiertos"]
)

st.metric("📊 Stock total (kg)", f"{df['stock_total'].sum():.2f}")

# Agregar producto
st.subheader("➕ Agregar nuevo producto")
with st.form("agregar"):
    nombre = st.text_input("Nombre")
    kg_bolsa = st.text_input("Kg por bolsa")
    bolsas = st.text_input("Bolsas cerradas")
    abiertos = st.text_input("Kg abiertos")
    enviar = st.form_submit_button("Agregar")

    if enviar:
        nuevo = {
            "prodnombre": nombre,
            "kg_por_bolsa": a_float(kg_bolsa),
            "bolsas_cerradas": a_int(bolsas),
            "kg_abiertos": a_float(abiertos),
        }
        st.session_state.df = pd.concat(
            [st.session_state.df, pd.DataFrame([nuevo])],
            ignore_index=True
        )
        guardar_productos("alimentos.csv", st.session_state.df)
        st.success("Producto agregado")
