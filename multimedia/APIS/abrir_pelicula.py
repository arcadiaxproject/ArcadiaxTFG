import requests

def actualizar_pelicula_abierto(nombre: str):

    url = f"http://localhost:8000/multimedia/pelicula/abrir/{nombre}"
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

