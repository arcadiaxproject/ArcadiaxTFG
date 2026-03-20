import requests

def obtener_juego_en_reproduccion():
    """
    Realiza una solicitud GET a 'http://localhost:8000/arcade/juego/en-reproduccion'
    y retorna el objeto JSON obtenido de la respuesta.

    Retorna:
    dict: Datos del juego en reproducción si la solicitud es exitosa.
    None: Si hay un error en la solicitud.
    """
    url = "http://localhost:8000/arcade/juego/en-reproduccion"

    try:
        # Hacer la solicitud GET
        respuesta = requests.get(url)

        # Verificar si la solicitud fue exitosa (código 200)
        if respuesta.status_code == 200:
            # Retornar el contenido de la respuesta como un diccionario (JSON)
            return respuesta.json()
        else:
            print(f"Error en la solicitud: {respuesta.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

