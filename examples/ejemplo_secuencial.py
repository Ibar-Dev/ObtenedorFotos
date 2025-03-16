from obtenedor_fotos import ejecutar_secuencial, ObtenedorFotos

if __name__ == "__main__":
    obtenedor = ObtenedorFotos()
    resultados, tiempo = ejecutar_secuencial(obtenedor, 10)
    print(f"Tiempo secuencial: {tiempo:.2f}s")