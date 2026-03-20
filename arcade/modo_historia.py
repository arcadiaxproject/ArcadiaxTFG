import time
import pyautogui
import psutil
import pygetwindow as gw  # Para manejar ventanas

def programa_ejecucion(nombre_programa):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == nombre_programa.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def enfocar_ventana(nombre_parcial):
    """
    Trae al frente la ventana que contiene 'nombre_parcial' en su título.
    """
    ventanas = gw.getWindowsWithTitle(nombre_parcial)
    if ventanas:
        ventana = ventanas[0]
        if not ventana.isMinimized:
            ventana.activate()
        else:
            ventana.restore()
            ventana.activate()
        time.sleep(1)  # Esperar un segundo para que la ventana esté activa
        return True
    return False

def gestionar_psp_emulador(nombre_programa, titulo_ventana):
    primera_vez = True

    while True:
        if programa_ejecucion(nombre_programa):
            print(f"{nombre_programa} detectado en ejecución.")

            # Asegurarse de que la ventana está en primer plano
            enfocar_ventana(titulo_ventana)

            if primera_vez:
                print("Esperando 5 segundos antes de cargar la última partida (F4)...")
                time.sleep(5)
                print("Cargando la última partida (F4)...")
                pyautogui.press('f4')
                primera_vez = False

            print("Guardando la partida (F2)...")
            pyautogui.press('f2')
            time.sleep(30)
        else:
            print(f"{nombre_programa} no detectado. Esperando...")
            primera_vez = True
            time.sleep(5)

if __name__ == "__main__":
    # Cambia esto por el nombre real del proceso y parte del título de la ventana
    gestionar_psp_emulador("psp.exe", "PPSSPP")
