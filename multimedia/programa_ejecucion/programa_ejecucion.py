import subprocess

def programa_en_ejecucion(nombre_programa: str) -> bool:
    """
    Verifica si un programa está en ejecución en Windows.
    """
    try:
        resultado = subprocess.run(
            [r"C:\Windows\System32\tasklist.exe"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return nombre_programa.lower() in resultado.stdout.lower()
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar 'tasklist': {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False