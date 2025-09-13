import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import gmean, hmean

def calcular_tendencia_central(datos):
    media = round(np.mean(datos), 2)
    mediana = round(np.median(datos), 2)
    
    # Moda con soporte para múltiples modas
    moda_resultado = stats.mode(datos, keepdims=True)
    moda = [round(m, 2) for m in moda_resultado.mode.tolist()]
    
    media_geometrica = round(gmean(datos), 2)
    media_armonica = round(hmean(datos), 2)
    
    return {
        "Media aritmética": media,
        "Mediana": mediana,
        "Moda": moda,
        "Media Geométrica": media_geometrica,
        "Media Armónica": media_armonica
    }

def generar_dfs(datos):
    frecuencias = {}
    for valor in datos:
        frecuencias[valor] = frecuencias.get(valor, 0) + 1

    df = pd.DataFrame({
        "Valor": list(frecuencias.keys()),
        "Frecuencia": list(frecuencias.values())
    })
    df = df.sort_values(by="Valor", ascending=True).reset_index(drop=True)
    df["Frecuencia Acumulada"] = df["Frecuencia"].cumsum()
    df["Frecuencia Relativa"] = (df["Frecuencia"] / len(datos)).round(2)
    df["Frecuencia Relativa Acumulada"] = df["Frecuencia Relativa"].cumsum().round(2)
    return df

def generar_dfsvai(datos, bins=10):
    # Genera clases y produce un DataFrame con columna 'Intervalo' y 'Frecuencia'
    clases = pd.cut(datos, bins=bins)
    df = clases.value_counts().sort_index().reset_index()
    # Renombrar para que la columna de intervalos se llame 'Intervalo'
    df.columns = ["Intervalo", "Frecuencia"]
    # Marca de clase (punto medio)
    df["Marca de Clase"] = df["Intervalo"].apply(lambda x: round((x.left + x.right) / 2, 2))
    # Ordenar por marca de clase ascendente (útil para graficar de izquierda a derecha)
    df = df.sort_values(by="Marca de Clase", ascending=True).reset_index(drop=True)
    df["Frecuencia Acumulada"] = df["Frecuencia"].cumsum()
    df["Frecuencia Relativa"] = (df["Frecuencia"] / len(datos)).round(2)
    df["Frecuencia Relativa Acumulada"] = df["Frecuencia Relativa"].cumsum().round(2)
    return df
