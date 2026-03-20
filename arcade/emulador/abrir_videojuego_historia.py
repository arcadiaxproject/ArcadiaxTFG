import os
import subprocess

# Rutas dinámicas que puedes modificar fácilmente
ruta_emuladores = "./multimedia/consolas/acceso_directo"
ruta_videojuegos_base = "./multimedia/videojuegos"

def abrir_juego(nombre_videojuego: str, consola: str):
    """
    Función para abrir un videojuego con su emulador correspondiente.

    Parámetros:
    nombre_videojuego (str): Nombre del archivo del videojuego (ejemplo: 'pokemon.gba').
    consola (str): Nombre de la consola (ejemplo: 'gameboy', 'nds', 'psp').
    """

    # Nombre del emulador dinámico basado en el nombre de la consola
    nombre_emulador = f"{consola}.exe"
    ruta_emulador = f"{ruta_emuladores}/{nombre_emulador}"

    # Construimos la ruta completa del videojuego utilizando mezcla de separadores
    ruta_juego = f"{ruta_videojuegos_base}/{consola}/{nombre_videojuego}"
    
    # Verificamos si el emulador existe
    if not os.path.exists(ruta_emulador):
        print(f"El emulador '{nombre_emulador}' para la consola '{consola}' no se encuentra.")
        return

    # Verificamos si el archivo del videojuego existe
    if not os.path.exists(ruta_juego):
        print(f"El videojuego '{nombre_videojuego}' no se encuentra en la carpeta '{consola}'.")
        return

    # Ejecutamos el emulador con el videojuego
    try:
        subprocess.run([ruta_emulador, ruta_juego], check=True)
        print(f"Abriendo '{nombre_videojuego}' en la consola '{consola}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar abrir el videojuego: {e}")

# Ejemplo de uso
