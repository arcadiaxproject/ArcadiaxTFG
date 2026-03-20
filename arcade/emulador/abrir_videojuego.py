import os
import subprocess
import time
import pygetwindow as gw

# Rutas dinámicas que puedes modificar fácilmente
ruta_emuladores = "./multimedia/consolas/acceso_directo"
ruta_videojuegos_base = "./multimedia/videojuegos"

def enfocar_ventana(nombre_parcial):
    """
    Activa la primera ventana visible que contenga 'nombre_parcial' en el título.
    """
    ventanas = gw.getWindowsWithTitle(nombre_parcial)
    if ventanas:
        for ventana in ventanas:
            if ventana.isVisible and not ventana.isMinimized:
                ventana.activate()
                time.sleep(1)
                return True
        # Si todas están minimizadas, restaurar y activar la primera
        ventana = ventanas[0]
        ventana.restore()
        ventana.activate()
        time.sleep(1)
        return True
    return False

def abrir_juego(nombre_videojuego: str, consola: str):
    """
    Abre un videojuego con su emulador correspondiente y enfoca la ventana.
    """
    nombre_emulador = f"{consola}.exe"
    ruta_emulador = f"{ruta_emuladores}/{nombre_emulador}"
    ruta_juego = f"{ruta_videojuegos_base}/{consola}/{nombre_videojuego}"

    if not os.path.exists(ruta_emulador):
        print(f"El emulador '{nombre_emulador}' para la consola '{consola}' no se encuentra.")
        return

    if not os.path.exists(ruta_juego):
        print(f"El videojuego '{nombre_videojuego}' no se encuentra en la carpeta '{consola}'.")
        return

    try:
        subprocess.Popen([ruta_emulador, ruta_juego])  # Usamos Popen en vez de run para no bloquear
        print(f"Abriendo '{nombre_videojuego}' en la consola '{consola}'...")

        # Esperar unos segundos para que la ventana se abra
        time.sleep(2)

        # Intentar enfocar la ventana del emulador
        if not enfocar_ventana(consola.upper()):
            print("⚠️ No se pudo encontrar o enfocar la ventana del emulador.")
    except Exception as e:
        print(f"Error al intentar abrir el videojuego: {e}")
