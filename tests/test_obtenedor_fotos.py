import pytest
from obtenedor_fotos import ObtenedorFotos

def test_obtener_foto_existente():
    obtenedor = ObtenedorFotos()
    resultado = obtenedor.obtener_datos_foto(1)
    assert resultado['id'] == 1
    assert 'error' not in resultado

def test_obtener_foto_inexistente():
    obtenedor = ObtenedorFotos()
    resultado = obtenedor.obtener_datos_foto(99999)
    assert 'error' in resultado