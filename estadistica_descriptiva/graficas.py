from math import sqrt, pi, exp
from statistics import multimode

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def graficar_tendencia(columna, bins=10):
    """
    Genera una visualización moderna de la distribución con media, mediana y moda
    Retorna la figura en lugar de mostrarla
    """
    datos = pd.Series(columna).dropna().astype(float).to_numpy()
    if datos.size == 0:
        raise ValueError('No hay datos para graficar.')

    media = float(np.mean(datos))
    mediana = float(np.median(datos))
    modas = multimode(datos.tolist())
    desviacion = float(np.std(datos, ddof=1)) if datos.size > 1 else 0.0

    fig, ax = plt.subplots(figsize=(12, 6), dpi=110)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    counts, edges, patches = ax.hist(
        datos,
        bins=bins,
        edgecolor='#1F2937',
        color='#60A5FA',
        alpha=0.82,
    )

    if desviacion > 0:
        x_vals = np.linspace(datos.min(), datos.max(), 400)
        y_vals = (1 / (desviacion * sqrt(2 * pi))) * np.exp(-0.5 * ((x_vals - media) / desviacion) ** 2)
        y_vals *= len(datos) * (edges[1] - edges[0])
        ax.plot(x_vals, y_vals, color='#0F766E', linewidth=2.5, label='Curva suavizada')

    ax.axvline(media, color='#DC2626', linestyle='--', linewidth=2.2, label=f'Media = {media:.2f}')
    ax.axvline(mediana, color='#16A34A', linestyle='--', linewidth=2.2, label=f'Mediana = {mediana:.2f}')

    if modas:
        for indice, moda in enumerate(modas):
            ax.axvline(moda, color='#F59E0B', linestyle=':', linewidth=2.2, alpha=0.9, label='Moda' if indice == 0 else None)

    ax.set_title('Distribución de Edad con Medidas Centrales', fontsize=15, fontweight='bold', pad=14)
    ax.set_xlabel('Edad', fontsize=12)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.grid(True, alpha=0.25, linestyle='--')
    ax.legend(frameon=False, fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig


def graficar_frecuencia(df, tipo='simple', titulo_simple='Frecuencia Simple', titulo_agrupada='Frecuencia con Intervalos'):
    """
    Genera gráfica de barras para frecuencias
    Retorna la figura en lugar de mostrarla
    """
    if df is None or len(df) == 0:
        raise ValueError('No hay datos para graficar frecuencias.')

    fig, ax = plt.subplots(figsize=(12, 6), dpi=110)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    # Diagnóstico rápido (descomentar si necesitas debug)
    # print("DEBUG columnas:", df.columns.tolist())
    # print(df.head())

    if tipo == 'simple':
        # Asegurarnos de que existan las columnas esperadas
        if 'Valor' not in df.columns or 'Frecuencia' not in df.columns:
            # intentar detectar columnas similares
            cols_lower = {c.lower(): c for c in df.columns}
            if 'valor' in cols_lower and 'frecuencia' in cols_lower:
                val_col = cols_lower['valor']
                freq_col = cols_lower['frecuencia']
            else:
                # tomar primera columna no numérica como etiquetas y primera numérica como frecuencia
                numeric_cols = df.select_dtypes(include='number').columns.tolist()
                non_numeric = [c for c in df.columns if c not in numeric_cols]
                if not numeric_cols:
                    raise ValueError('No se encontró columna numérica para frecuencias en el DataFrame simple.')
                freq_col = numeric_cols[0]
                val_col = non_numeric[0] if non_numeric else df.index.name if df.index.name else df.index.astype(str)
        else:
            val_col = 'Valor'
            freq_col = 'Frecuencia'

        labels = df[val_col].astype(str).tolist() if isinstance(val_col, str) else list(val_col)
        heights = df[freq_col].tolist()
        positions = range(len(heights))
        palette = plt.cm.Blues(np.linspace(0.55, 0.9, len(heights)))
        bars = ax.bar(positions, heights, color=palette, edgecolor='#1F2937', alpha=0.95)
        
        # Añadir valores sobre las barras
        for bar, height in zip(bars, heights):
            ax.text(bar.get_x() + bar.get_width()/2., height + max(0.1, height * 0.015),
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        ax.set_xticks(list(positions))
        ax.set_xticklabels(labels, rotation=40, ha='right')
        ax.set_title(titulo_simple, fontsize=14, fontweight='bold', pad=12)
        ax.set_xlabel('Valor', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)

    else:
        # Agrupada: aceptar que la columna de intervalos se llame 'Intervalo' o 'Clase' o esté en el índice
        if 'Intervalo' in df.columns and 'Frecuencia' in df.columns:
            labels = df['Intervalo'].astype(str).tolist()
            heights = df['Frecuencia'].tolist()
        elif 'Clase' in df.columns and 'Frecuencia' in df.columns:
            labels = df['Clase'].astype(str).tolist()
            heights = df['Frecuencia'].tolist()
        else:
            # buscar una columna de frecuencia
            freq_col = None
            for c in df.columns:
                if c.lower() in ('frecuencia', 'freq', 'f'):
                    freq_col = c
                    break
            if freq_col is None:
                numeric_cols = df.select_dtypes(include='number').columns.tolist()
                if numeric_cols:
                    freq_col = numeric_cols[0]
                else:
                    raise ValueError('No se encontró columna de frecuencias en el DataFrame agrupado.')

            # intervalos en el índice?
            if isinstance(df.index, pd.IntervalIndex) or df.index.dtype == object:
                labels = df.index.astype(str).tolist()
                heights = df[freq_col].tolist()
            else:
                # tomar la primera columna no numérica como etiquetas
                numeric_cols = df.select_dtypes(include='number').columns.tolist()
                non_numeric = [c for c in df.columns if c not in numeric_cols]
                if non_numeric:
                    labels = df[non_numeric[0]].astype(str).tolist()
                    heights = df[freq_col].tolist()
                else:
                    labels = df.index.astype(str).tolist()
                    heights = df[freq_col].tolist()

        positions = range(len(heights))
        palette = plt.cm.YlOrRd(np.linspace(0.45, 0.9, len(heights)))
        bars = ax.bar(positions, heights, color=palette, edgecolor='#1F2937', alpha=0.95)
        
        # Añadir valores sobre las barras
        for bar, height in zip(bars, heights):
            ax.text(bar.get_x() + bar.get_width()/2., height + max(0.1, height * 0.015),
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        ax.set_xticks(list(positions))
        ax.set_xticklabels(labels, rotation=40, ha='right')
        ax.set_title(titulo_agrupada, fontsize=14, fontweight='bold', pad=12)
        ax.set_xlabel('Intervalo', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)

    ax.grid(True, alpha=0.25, axis='y', linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    plt.tight_layout()
    return fig

