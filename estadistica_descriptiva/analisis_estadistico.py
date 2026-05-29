import math
from statistics import multimode

import pandas as pd
import numpy as np


def _media_geometrica(datos):
    valores = np.asarray(list(datos), dtype=float)
    if valores.size == 0:
        raise ValueError("Se requieren datos para calcular la media geométrica.")
    if np.any(valores <= 0):
        raise ValueError("La media geométrica solo se puede calcular con valores positivos.")
    return float(math.exp(np.mean(np.log(valores))))


def _media_armonica(datos):
    valores = np.asarray(list(datos), dtype=float)
    if valores.size == 0:
        raise ValueError("Se requieren datos para calcular la media armónica.")
    if np.any(valores == 0):
        raise ValueError("La media armónica no se puede calcular con valores iguales a 0.")
    return float(len(valores) / np.sum(1 / valores))

def calcular_tendencia_central(datos):
    media = round(np.mean(datos), 2)
    mediana = round(np.median(datos), 2)
    
    # Moda con soporte para múltiples modas
    moda = [round(m, 2) for m in multimode(list(datos))]
    
    media_geometrica = round(_media_geometrica(datos), 2)
    media_armonica = round(_media_armonica(datos), 2)
    
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
