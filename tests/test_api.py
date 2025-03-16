import pytest
import requests
from obtenedor_fotos import URL_FOTOS, URL_ALBUMES

def test_api_fotos_disponible():
    respuesta = requests.get(URL_FOTOS)
    assert respuesta.status_code == 200

def test_api_albumes_disponible():
    respuesta = requests.get(f"{URL_ALBUMES}/1")
    assert respuesta.status_code == 200