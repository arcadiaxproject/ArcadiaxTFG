#eventos que se disparan cuando el usuario interactua
class Events:
    #Cuando alguien pulsa un boton en la mmaquina arcade
    ARCADE_BUTTON_SELECT="input.arcade.select"
    #cuando volvemos atras en el arcade:
        #si estas en seleccion y vuelves a IDLE
        #Si estas jugando cierra el emulador
    ARCADE_BUTTON_BACK="input.arcade.back"
    #Para confirma juego elegido
    ARCADE_BUTTON_CONFIRM="input.arcade.confirm"
    #Arcade buton selec pero para la web. Esto permite reutilizar el flujo de trabajo
    WEB_SELECT_REQUEST="input.web.select"

    #Cambiar de estado, por ejemplo servira al front para actualizar el estado en tiempo real. 
    #Payload:{"state:"idle|trailer|selecting|loading|playing etc}
    STATE_CHANGED="state.changed"

    #Cuando un usuario elige un juego desde la web o desde la arcade
    #Playload{nombre:Crash, consola:ps1, ubicacion:d/roms/crash.bin}
    #El arcade lo recibe y busca el drive correcto para lanzar el emulador
    GAME_PLAY="playback.game.play"
    #Cuando el emulador arranca correctamente
    GAME_OPENED="playback.game.opened"
    #Cuando cerramos un juego
    GAME_CLOSED="playback.game.closed"

    #Cuando un usuario elige una pelicula
    #Payload{nombre:Inception, ubicacion:/peliculas/inception.mkv}
    FILM_PLAY="playback.film.play"

    #Para toda la reproduccion (juegos y peliculas) y resetea el estado en la BBDD
    PLAYBACK_STOP="playback.stop"

    #Cuando estamos x segundo/ min sin actividad en el sistema
    IDLE_DETECTED="system.idle"

    #Cuando se va a apagar el sistema
    SYSTEM_SHUTDOWN="system.shutdown"
