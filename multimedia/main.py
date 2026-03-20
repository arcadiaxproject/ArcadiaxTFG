import asyncio
import psutil
from APIS.hay_pelicula_reproduciendose import obtener_estado_pelicula
from APIS.datos_pelicula_ejecucion import obtener_pelicula_en_reproduccion
from APIS.resetear_pelicula import reset_pelicula
from programa_ejecucion.programa_ejecucion import programa_en_ejecucion
from APIS.abrir_pelicula import actualizar_pelicula_abierto
from reproductor.abrir_pelicula import abrir_pelicula_vlc

# Función para cerrar VLC
def cerrar_vlc():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == "vlc.exe":
            try:
                proc.kill()
                print("VLC cerrado automáticamente.")
            except Exception as e:
                print(f"Error al cerrar VLC: {e}")

async def main():
    while True:
        # Verificar si hay una película reproduciéndose
        estado = obtener_estado_pelicula()
        vlc_activo = programa_en_ejecucion("vlc.exe")
        
        if estado:
            # Hay película en reproducción
            pelicula = obtener_pelicula_en_reproduccion()
            if pelicula:
                if not pelicula["abierto"]:
                    if not vlc_activo:
                        print(f"Abriendo película: {pelicula['nombre']}")
                        actualizar_pelicula_abierto(pelicula["nombre"])
                        abrir_pelicula_vlc(pelicula["ubicacion"])
                    else:
                        print("VLC ya está activo, pero la película no estaba marcada como abierta.")
                else:
                    if not vlc_activo:
                        print("El reproductor VLC se cerró. Reseteando la película...")
                        reset_pelicula()
            else:
                print("No se encontró ninguna película en reproducción.")
        else:
            # No hay película marcada para reproducción
            if vlc_activo:
                print("No hay película activa pero VLC está abierto. Cerrando VLC...")
                cerrar_vlc()
        
        await asyncio.sleep(1)

# Ejecutar la función main
if __name__ == "__main__":
    asyncio.run(main())
