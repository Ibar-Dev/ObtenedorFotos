from obtenedor_fotos import ejecutar_con_procesos, ObtenedorFotos

if __name__ == "__main__":
    obtenedor = ObtenedorFotos()
    resultados, tiempo = ejecutar_con_procesos(obtenedor, 15)
    print(f"Tiempo con procesos: {tiempo:.2f}s")