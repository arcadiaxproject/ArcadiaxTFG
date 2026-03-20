import subprocess
import keyboard
import time
import os
import psutil

# Variables globales para procesos
proceso_main = None
proceso_historia = None

# Función para lanzar los scripts
def iniciar_scripts():
    global proceso_main, proceso_historia
    proceso_main = subprocess.Popen(["python", "main.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    proceso_historia = subprocess.Popen(["python", "modo_historia.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("✅ Scripts lanzados: main.py y modo_historia.py")

# Función para cerrar los scripts
def cerrar_scripts():
    global proceso_main, proceso_historia
    if proceso_main and proceso_main.poll() is None:
        proceso_main.terminate()
        proceso_main.wait(timeout=5)
    if proceso_historia and proceso_historia.poll() is None:
        proceso_historia.terminate()
        proceso_historia.wait(timeout=5)
    print("🛑 Scripts cerrados.")

# Función para cerrar RetroBat
def cerrar_retrobat():
    for proc in psutil.process_iter(['pid', 'name']):
        if "emulationstation.exe" in proc.info['name'].lower():
            try:
                proc.kill()
                print("🛑 RetroBat cerrado.")
            except Exception as e:
                print(f"⚠️ Error cerrando RetroBat: {e}")

# Función para cerrar emuladores
def cerrar_emuladores():
    emuladores = [
        "pcsx2.exe", "snes9x.exe", "project64.exe", "dolphin.exe",
        "mame.exe", "retroarch.exe", "psp.exe", "citra.exe"
    ]
    for proc in psutil.process_iter(['pid', 'name']):
        nombre_proc = proc.info['name'].lower()
        for emulador in emuladores:
            if emulador in nombre_proc:
                try:
                    proc.kill()
                    print(f"🛑 Emulador cerrado: {nombre_proc}")
                except Exception as e:
                    print(f"⚠️ Error cerrando {nombre_proc}: {e}")

# Función para cerrar VLC
def cerrar_vlc_si_abierto():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and "vlc.exe" in proc.info['name'].lower():
            try:
                proc.kill()
                print("🎵 VLC cerrado automáticamente.")
            except Exception as e:
                print(f"⚠️ No se pudo cerrar VLC: {e}")

# Lanzar scripts al inicio
iniciar_scripts()

print("🎮 Sistema iniciado. Mantén pulsado '2' durante 10 segundos para cambiar a RetroBat...")

tiempo_inicio = None
duracion_activacion = 10  # segundos
tiempo_sin_tecla = None
retrobat_lanzado = False

try:
    while True:
        if not retrobat_lanzado:
            # Si se mantiene pulsado el 2 durante 10s
            if keyboard.is_pressed("2"):
                if tiempo_inicio is None:
                    tiempo_inicio = time.time()
                elif time.time() - tiempo_inicio >= duracion_activacion:
                    print("🟢 Botón '2' mantenido más de 10s. Cerrando scripts y emuladores...")

                    cerrar_scripts()
                    cerrar_emuladores()
                    cerrar_vlc_si_abierto()

                    print("🚀 Lanzando RetroBat...")
                    subprocess.Popen(r"C:\RetroBat\retrobat.exe", shell=True)
                    retrobat_lanzado = True
                    tiempo_sin_tecla = time.time()
            else:
                tiempo_inicio = None
        else:
            # Vigilamos si RetroBat está abierto y cerramos VLC si aparece
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and "emulationstation.exe" in proc.info['name'].lower():
                    cerrar_vlc_si_abierto()
                    break

            # Vigilamos inactividad de teclado
            teclas_monitor = [
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                "u", "v", "w", "x", "y", "z",
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "space", "enter", "esc", "up", "down", "left", "right",
                "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"
            ]

            if any(keyboard.is_pressed(k) for k in teclas_monitor):
                tiempo_sin_tecla = time.time()

            if time.time() - tiempo_sin_tecla >= 60:
                print("⏳ Inactividad detectada. Cerrando RetroBat y relanzando scripts...")

                cerrar_retrobat()
                cerrar_emuladores()
                time.sleep(2)
                iniciar_scripts()
                retrobat_lanzado = False
                tiempo_inicio = None

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Sistema detenido manualmente.")
    cerrar_scripts()
    cerrar_emuladores()
    cerrar_retrobat()
