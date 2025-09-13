import matplotlib.pyplot as plt
import pandas as pd

def graficar_tendencia(columna, bins=10):
    plt.hist(columna, bins=bins, edgecolor='black')
    plt.title('Distribución de Edad')
    plt.xlabel('Edad')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graficar_frecuencia(df, tipo='simple', titulo_simple='Frecuencia Simple', titulo_agrupada='Frecuencia con Intervalos'):
    plt.figure(figsize=(10,5))

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
        plt.bar(positions, heights)
        plt.xticks(positions, labels, rotation=45, ha='right')
        plt.title(titulo_simple)
        plt.xlabel('Valor')
        plt.ylabel('Frecuencia')

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
        plt.bar(positions, heights)
        plt.xticks(positions, labels, rotation=45, ha='right')
        plt.title(titulo_agrupada)
        plt.xlabel('Intervalo')
        plt.ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()
