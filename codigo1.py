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


# ---------------- PROGRAMA PRINCIPAL ----------------

productos = cargar_productos("alimentos.csv")

while True:
    print("\n===== GESTOR DE STOCK =====")
    print("1 - Mostrar productos")
    print("2 - Ver stock total (kg)")
    print("3 - Descontar stock")
    print("4 - Salir")
    opcion = input("Elegí una opción: ")

    if opcion == "1":
        mostrar_productos(productos)

    elif opcion == "2":
        total = calcular_stock_total(productos)
        print(f"\nStock total disponible: {total:.2f} kg")

    elif opcion == "3":
        nombre_buscar = input("Ingresá el nombre del producto a descontar: ").strip().lower()
        encontrado = False

        for p in productos:
            if nombre_buscar in p["prodnombre"].lower():
                encontrado = True
                print(f"Producto encontrado: {p['prodnombre']}")
                print(f"Stock actual: {p['kg_por_bolsa'] * p['bolsas_cerradas'] + p['kg_abiertos']:.2f} kg")

                kg_a_descontar = a_float(input("Ingresá la cantidad de kg a descontar: "))
                stock_actual = p["kg_por_bolsa"] * p["bolsas_cerradas"] + p["kg_abiertos"]

                if kg_a_descontar > stock_actual:
                    print("No hay suficiente stock para descontar esa cantidad.")
                else:
                    # Descontar de kg abiertos primero
                    if kg_a_descontar <= p["kg_abiertos"]:
                        p["kg_abiertos"] -= kg_a_descontar
                    else:
                        kg_a_descontar -= p["kg_abiertos"]
                        p["kg_abiertos"] = 0.0

                        # Descontar de bolsas cerradas
                        bolsas_a_descontar = int(kg_a_descontar // p["kg_por_bolsa"])
                        kg_restante = kg_a_descontar % p["kg_por_bolsa"]

                        if bolsas_a_descontar > p["bolsas_cerradas"]:
                            bolsas_a_descontar = p["bolsas_cerradas"]
                            kg_restante = 0.0

                        p["bolsas_cerradas"] -= bolsas_a_descontar
                        p["kg_abiertos"] -= kg_restante

                    print("Descuento realizado con éxito.")
                break

        if not encontrado:
            print("Producto no encontrado.")
    elif opcion == "4":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida. Intentá de nuevo.")

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
