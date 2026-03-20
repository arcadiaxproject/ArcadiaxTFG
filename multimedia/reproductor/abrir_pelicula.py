import subprocess
import os

# Define la ruta directamente a la carpeta de archivos/peliculas dentro del proyecto
PELICULAS_DIR = os.path.join(os.getcwd(), "archivos", "peliculas")  # Ruta dinámica relativa al proyecto
VLC_PATH = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"  # Ruta al ejecutable de VLC

def abrir_pelicula_vlc(nombre_pelicula):
    """
    Abre una película en el reproductor VLC.

    :param nombre_pelicula: Nombre del archivo de la película (incluyendo extensión).
    """
    # Construir la ruta completa del archivo de la película dentro de archivos/peliculas
    pelicula_path = os.path.join(PELICULAS_DIR, nombre_pelicula)

    # Verificar si el archivo existe
    if not os.path.exists(pelicula_path):
        print(f"Error: La película '{nombre_pelicula}' no se encuentra en {PELICULAS_DIR}.")
        return

    # Ejecutar VLC con la película
    try:
        subprocess.Popen([VLC_PATH, pelicula_path], shell=True)
        print(f"Reproduciendo '{nombre_pelicula}' en VLC.")
    except Exception as e:
        print(f"Error al intentar abrir VLC: {e}")
