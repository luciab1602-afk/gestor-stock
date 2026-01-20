import streamlit as st
import pandas as pd
import csv
import re

# =====================
# FUNCIONES AUXILIARES
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


def guardar_productos(nombre_archivo, productos):
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        campos = ["prodnombre", "kg_por_bolsa", "bolsas_cerradas", "kg_abiertos"]
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        for p in productos:
            writer.writerow(p)


def productos_para_tabla(productos):
    filas = []
    for p in productos:
        stock_total = p["kg_por_bolsa"] * p["bolsas_cerradas"] + p["kg_abiertos"]
        filas.append({
            "Producto": p["prodnombre"],
            "Kg por bolsa": p["kg_por_bolsa"],
            "Bolsas cerradas": p["bolsas_cerradas"],
            "Kg abiertos": round(p["kg_abiertos"], 2),
            "Stock total (kg)": round(stock_total, 2)
        })
    return filas


# =====================
# APP STREAMLIT
# =====================

st.set_page_config(page_title="Gestor de Stock", layout="wide")
st.title("📦 Gestor de Stock – Curioso")

try:
    productos = cargar_productos("alimentos.csv")
except Exception as e:
    st.error("Error cargando alimentos.csv")
    st.stop()

# 🔍 Buscador
busqueda = st.text_input("🔍 Buscar producto")

if busqueda:
    productos_filtrados = [
        p for p in productos
        if busqueda.lower() in p["prodnombre"].lower()
    ]
else:
    productos_filtrados = productos

# 📊 Tabla
st.title("📦 Gestor de Stock")

df_editado = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "prodnombre": st.column_config.TextColumn("Producto"),
        "kg_por_bolsa": st.column_config.NumberColumn("Kg por bolsa", min_value=0.1),
        "bolsas_cerradas": st.column_config.NumberColumn("Bolsas cerradas", min_value=0, step=1),
        "kg_abiertos": st.column_config.NumberColumn("Kg abiertos", min_value=0.0, step=0.1),
    }
)
if st.button("💾 Guardar cambios"):
    df_editado.to_csv("alimentos.csv", index=False)
    st.session_state.df = df_editado
    st.success("Stock actualizado correctamente")
df_editado["stock_total"] = (
    df_editado["kg_por_bolsa"] * df_editado["bolsas_cerradas"]
    + df_editado["kg_abiertos"]
)

st.metric(
    "📊 Stock total (kg)",
    f"{df_editado['stock_total'].sum():.2f}"
)


# ➕ Formulario para agregar productos
st.subheader("➕ Agregar nuevo producto")
with st.form("form_agregar_producto"):
    nombre = st.text_input("Nombre del producto")
    kg_por_bolsa = st.text_input("Kg por bolsa")
    bolsas_cerradas = st.text_input("Cantidad de bolsas cerradas")
    kg_abiertos = st.text_input("Kg abiertos")
    enviar = st.form_submit_button("Agregar producto")

    if enviar:
        nuevo_producto = {
            "prodnombre": nombre,
            "kg_por_bolsa": a_float(kg_por_bolsa),
            "bolsas_cerradas": a_int(bolsas_cerradas),
            "kg_abiertos": a_float(kg_abiertos),
        }
        productos.append(nuevo_producto)
        try:
            guardar_productos("alimentos.csv", productos)
            st.success(f"Producto '{nombre}' agregado correctamente.")
        except Exception as e:
            st.error("Error guardando el producto en alimentos.csv")
    st.title("📦 Gestor de Stock")

df_editado = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "prodnombre": st.column_config.TextColumn("Producto"),
        "kg_por_bolsa": st.column_config.NumberColumn("Kg por bolsa", min_value=0.1),
        "bolsas_cerradas": st.column_config.NumberColumn("Bolsas cerradas", min_value=0, step=1),
        "kg_abiertos": st.column_config.NumberColumn("Kg abiertos", min_value=0.0, step=0.1),
    })
