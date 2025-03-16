from obtenedor_fotos import ejecutar_con_hilos, ObtenedorFotos

if __name__ == "__main__":
    obtenedor = ObtenedorFotos()
    resultados, tiempo = ejecutar_con_hilos(obtenedor, 20)
    print(f"Tiempo con hilos: {tiempo:.2f}s")