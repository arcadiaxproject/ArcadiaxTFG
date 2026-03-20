import os
import asyncio
import subprocess
from API.ObnerTrailer import obtener_trailer

# Ruta del ejecutable del reproductor multimedia (por ejemplo, VLC)
ruta_reproductor = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
ruta_trailer = "./multimedia/trailer/"

# Función para reproducir el tráiler
async def reproducir_trailer():
    trailer = await obtener_trailer()
    
    if trailer:
        # Eliminar comillas del nombre del archivo
        trailer = trailer.strip('"')
        
        # Obtener la ruta absoluta del archivo de tráiler
        ruta_video = os.path.abspath(os.path.join(ruta_trailer, trailer))
        
        # Verificar si el archivo existe
        if not os.path.isfile(ruta_video):
            print(f"Archivo no encontrado: {ruta_video}")
            return

        # Comando para abrir el reproductor con el tráiler y cerrar al finalizar
        comando = [ruta_reproductor, ruta_video, "--play-and-exit"]
        print(f"Reproduciendo tráiler: {ruta_video}")
        
        # Ejecutar el reproductor y esperar a que termine
        proceso = subprocess.Popen(comando)
        proceso.wait()  # Espera a que el reproductor termine
        
        print("Tráiler finalizado y VLC cerrado.")
    else:
        print("No se pudo obtener el tráiler.")

