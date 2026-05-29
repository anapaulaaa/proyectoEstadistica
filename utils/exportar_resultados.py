import pandas as pd

from utils.app_paths import writable_data_dir

def exportar_resultados(tendencia, dfs, dfsvai):
    destino = writable_data_dir()

    # Exportar medidas
    pd.DataFrame([tendencia]).to_csv(destino / "resultados_tendencia.csv", index=False)

    # Exportar cuadros
    dfs.to_csv(destino / "cuadro_frecuencia_simple.csv", index=False)
    dfsvai.to_csv(destino / "cuadro_frecuencia_agrupada.csv", index=False)
