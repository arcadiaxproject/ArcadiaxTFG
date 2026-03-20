import requests

def reset_arcade():
    """
    Realiza una solicitud PUT a 'http://localhost:8000/arcade/reset'
    para restablecer el estado de la arcade.

    Retorna:
    dict: Datos de la respuesta si la solicitud es exitosa.
    None: Si hay un error en la solicitud.
    """
    url = "http://localhost:8000/arcade/reset"

    try:
        # Realizar la solicitud PUT sin cuerpo
        respuesta = requests.put(url)

        # Verificar si la solicitud fue exitosa (código 200)
        if respuesta.status_code == 200:
            print("Solicitud PUT exitosa.")
            return respuesta.json()
        else:
            print(f"Error en la solicitud PUT: {respuesta.status_code}")
            print("Detalle:", respuesta.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

