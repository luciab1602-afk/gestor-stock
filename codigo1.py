import csv
import re


def a_int(valor):
    if valor is None:
        return 0

    valor = valor.strip()
    if valor == "":
        return 0

    match = re.search(r"\d+", valor)
    if match:
        return int(match.group())

    return 0


def a_float(valor):
    if valor is None:
        return 0.0

    valor = valor.strip()
    if valor == "":
        return 0.0

    # Cambia coma decimal por punto
    valor = valor.replace(",", ".")

    # Busca número entero o decimal dentro del texto
    match = re.search(r"\d+(\.\d+)?", valor)
    if match:
        return float(match.group())

    return 0.0


def cargar_productos(nombre_archivo):
    productos = []

    with open(nombre_archivo, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            producto = {
                "prodnombre": fila.get("prodnombre", "").strip(),
                "kg_por_bolsa": a_float(fila.get("kg_por_bolsa")),
                "bolsas_cerradas": a_int(fila.get("bolsas_cerradas")),
                "kg_abiertos": a_float(fila.get("kg_abiertos")),
            }

            productos.append(producto)

    return productos


def mostrar_productos(productos, limite=10):
    print("\n--- LISTA DE PRODUCTOS ---")

    for i, p in enumerate(productos[:limite], start=1):
        stock_total = (
            p["kg_por_bolsa"] * p["bolsas_cerradas"] + p["kg_abiertos"]
        )

        print(
            f"{i}. {p['prodnombre']} | "
            f"Bolsa: {p['kg_por_bolsa']} kg | "
            f"Bolsas cerradas: {p['bolsas_cerradas']} | "
            f"Kg abiertos: {p['kg_abiertos']} | "
            f"Stock total: {stock_total:.2f} kg"
        )

    if len(productos) > limite:
        print(f"... mostrando {limite} de {len(productos)} productos")


def calcular_stock_total(productos):
    total = 0.0

    for p in productos:
        total += p["kg_por_bolsa"] * p["bolsas_cerradas"]
        total += p["kg_abiertos"]

    return total
    
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
