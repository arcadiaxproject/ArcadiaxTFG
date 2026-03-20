import asyncio
from API.hay_juego_reproduciendo import obtener_estado_juego
from API.datos_juego_ejecucion import obtener_juego_en_reproduccion
from API.abrir_videojuego import actualizar_juego_abierto
from emulador.abrir_videojuego import abrir_juego
from programa_ejecucion.programa_ejecucion import programa_en_ejecucion
from API.finalizar_juego import reset_arcade
from trailer.abrirTrailer import reproducir_trailer

async def main():
    while True:
        # Verificar si hay un juego reproduciéndose
        estado = obtener_estado_juego()

        if estado:
            # Obtener datos del juego en reproducción
            juego = obtener_juego_en_reproduccion()

            # Verificar si el juego no está marcado como abierto
            if not juego["abierto"]:
                # Actualizar estado del juego a 'abierto'
                juego_abierto = actualizar_juego_abierto(juego["nombre"], juego["consola"])
                abrir_juego(juego_abierto["ubicacion"], juego_abierto["consola"])

            # Verificar si el programa del juego no está en ejecución
            ejecutando = programa_en_ejecucion(juego["consola"] + ".exe")
            if not ejecutando:
                print("El videojuego no se está ejecutando, restableciendo arcade.")
                reset_arcade()

        else:
            # Verificar si VLC no está en ejecución y reproducir tráiler si no lo está
            reproductor = programa_en_ejecucion("vlc.exe")
            if not reproductor:
                print("No hay juego en reproducción, iniciando tráiler.")
                await reproducir_trailer()

        # Esperar 1 segundo antes de la siguiente iteración
        await asyncio.sleep(1)

# Ejecutar la función main
if __name__ == "__main__":
    asyncio.run(main())