import requests

# Función para obtener el tráiler desde la API
async def obtener_trailer():
    url = "http://localhost:8000/arcade/juego/trailer"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la respuesta es exitosa (status 200)
        return response.text  # Devuelve la URL del tráiler como string
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el tráiler: {e}")
        return None
