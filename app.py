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
    productos = cargar_productos("productos.csv")
except Exception as e:
    st.error("Error cargando productos.csv")
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
st.subheader("📊 Stock actual")
df = pd.DataFrame(productos_para_tabla(productos_filtrados))
st.dataframe(df, use_container_width=True)

# 🛠 Ajustes de stock
st.subheader("🛠 Ajustar stock")

for i, p in enumerate(productos_filtrados):
    with st.expander(p["prodnombre"]):
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("➕ Bolsa", key=f"mas_{i}"):
                p["bolsas_cerradas"] += 1

        with col2:
            if st.button("➖ Bolsa", key=f"menos_{i}"):
                if p["bolsas_cerradas"] > 0:
                    p["bolsas_cerradas"] -= 1

        with col3:
            cantidad_bolsas = st.number_input(
                "Cantidad de bolsas",
                min_value=0,
                step=1,
                key=f"bolsas_{i}"
            )

        with col4:
            if st.button("📦 Agregar bolsas cerradas", key=f"agregar_bolsas_{i}"):
                if cantidad_bolsas > 0:
                    p["bolsas_cerradas"] += cantidad_bolsas
                    st.success(f"✅ {cantidad_bolsas} bolsa(s) agregada(s)")

        with col5:
            kg_vendidos = st.number_input(
                "Kg vendidos",
                min_value=0.0,
                step=0.1,
                key=f"kg_{i}"
            )
            if st.button("💸 Registrar venta", key=f"venta_{i}"):
                if p["kg_abiertos"] >= kg_vendidos:
                    p["kg_abiertos"] -= kg_vendidos
                else:
                    st.warning("No hay suficientes kg abiertos")

# 💾 Guardar
if st.button("💾 Guardar cambios"):
    guardar_productos("productos.csv", productos)
    st.success("Cambios guardados correctamente ✅")