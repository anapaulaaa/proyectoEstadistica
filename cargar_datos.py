import pandas as pd

def importar_csv(ruta):
    try:
        datos = pd.read_csv(ruta)
        return datos
    except Exception as e:
        print(f"Error al importar: {e}")
        return None
