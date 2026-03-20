import requests

def obtener_estado_juego():
 
    url = "http://localhost:8000/arcade/juego/ejecutando"

    try:
        # Hacer la solicitud GET
        respuesta = requests.get(url)

        # Verificar si la solicitud fue exitosa (código 200)
        if respuesta.status_code == 200:
            # Retornar el valor booleano obtenido de la respuesta
            return respuesta.json()  # Se espera que la respuesta sea un booleano (True o False)
        else:
            print(f"Error en la solicitud: {respuesta.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return False
