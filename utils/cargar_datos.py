from pathlib import Path

import pandas as pd

def importar_csv(ruta):
    try:
        ruta = str(Path(ruta))
        intentos = [
            {"encoding": "utf-8-sig", "sep": None, "engine": "python"},
            {"encoding": "utf-8", "sep": None, "engine": "python"},
            {"encoding": "latin-1", "sep": None, "engine": "python"},
            {"encoding": "utf-8-sig"},
            {"encoding": "latin-1"},
        ]

        ultimo_error = None
        for kwargs in intentos:
            try:
                return pd.read_csv(ruta, **kwargs)
            except Exception as error:
                ultimo_error = error

        raise ultimo_error
    except Exception as e:
        print(f"Error al importar: {e}")
        return None
