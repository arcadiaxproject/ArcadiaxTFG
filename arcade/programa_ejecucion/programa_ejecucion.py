import subprocess
import os

def programa_en_ejecucion(nombre_programa: str) -> bool:
    """
    Verifica si un programa está en ejecución usando tasklist.exe (con ruta completa).
    """
    ruta_tasklist = r"C:\Windows\System32\tasklist.exe"

    if not os.path.exists(ruta_tasklist):
        print("No se encontró tasklist.exe en C:\\Windows\\System32.")
        return False

    try:
        resultado = subprocess.run(
            [ruta_tasklist],
            capture_output=True,
            text=True,
            shell=False
        )
        return nombre_programa.lower() in resultado.stdout.lower()
    except subprocess.SubprocessError as e:
        print(f"Error al ejecutar tasklist: {e}")
        return False
