import pandas as pd

def exportar_resultados(tendencia, dfs, dfsvai):
    # Exportar medidas
    pd.DataFrame([tendencia]).to_csv("datos/resultados_tendencia.csv", index=False)

    # Exportar cuadros
    dfs.to_csv("datos/cuadro_frecuencia_simple.csv", index=False)
    dfsvai.to_csv("datos/cuadro_frecuencia_agrupada.csv", index=False)
