import requests

def actualizar_juego_abierto(nombre: str, consola: str):
    """
    Realiza una solicitud PUT a 'http://localhost:8000/arcade/juego/abrir/{nombre}/{consola}'
    para actualizar el campo 'abierto' a True.

    Parámetros:
    nombre (str): Nombre del juego.
    consola (str): Nombre de la consola.

    Retorna:
    dict: Datos de la respuesta si la solicitud es exitosa.
    None: Si hay un error en la solicitud.
    """
    url = f"http://localhost:8000/arcade/juego/abrir/{nombre}/{consola}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "abierto": True
    }

    try:
        # Hacer la solicitud PUT
        respuesta = requests.put(url, json=payload, headers=headers)

        # Verificar si la solicitud fue exitosa (código 200)
        if respuesta.status_code == 200:
            print("Solicitud PUT exitosa.")
            return respuesta.json()
        else:
            print(f"Error en la solicitud PUT: {respuesta.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

