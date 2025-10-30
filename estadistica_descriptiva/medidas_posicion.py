"""
Medidas de Posición - Cuartiles, Percentiles, Deciles
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calcular_cuartiles(datos):
    """
    Calcula los cuartiles Q1, Q2 (mediana), Q3
    """
    q1 = np.percentile(datos, 25)
    q2 = np.percentile(datos, 50)  # Mediana
    q3 = np.percentile(datos, 75)
    
    # Rango intercuartílico
    iqr = q3 - q1
    
    return {
        'Q1': round(q1, 2),
        'Q2_Mediana': round(q2, 2),
        'Q3': round(q3, 2),
        'IQR_Rango_Intercuartilico': round(iqr, 2),
        'interpretacion': {
            'Q1': f'25% de los datos son menores o iguales a {round(q1, 2)}',
            'Q2': f'50% de los datos son menores o iguales a {round(q2, 2)} (Mediana)',
            'Q3': f'75% de los datos son menores o iguales a {round(q3, 2)}',
            'IQR': f'El 50% central de los datos varía en {round(iqr, 2)} unidades'
        }
    }

def calcular_deciles(datos):
    """
    Calcula los 9 deciles (D1, D2, ..., D9)
    """
    deciles = {}
    for i in range(1, 10):
        percentil = i * 10
        valor = np.percentile(datos, percentil)
        deciles[f'D{i}'] = round(valor, 2)
        deciles[f'D{i}_interpretacion'] = f'{percentil}% de los datos son menores o iguales a {round(valor, 2)}'
    
    return deciles

def calcular_percentiles(datos, percentiles_deseados=None):
    """
    Calcula percentiles específicos o los más comunes
    
    percentiles_deseados: lista de percentiles a calcular (ej: [10, 25, 50, 75, 90])
    """
    if percentiles_deseados is None:
        # Percentiles comunes
        percentiles_deseados = [5, 10, 25, 50, 75, 90, 95, 99]
    
    resultados = {}
    for p in percentiles_deseados:
        valor = np.percentile(datos, p)
        resultados[f'P{p}'] = round(valor, 2)
        resultados[f'P{p}_interpretacion'] = f'{p}% de los datos son menores o iguales a {round(valor, 2)}'
    
    return resultados

def calcular_valores_extremos(datos):
    """
    Identifica valores atípicos usando el método IQR
    """
    q1 = np.percentile(datos, 25)
    q3 = np.percentile(datos, 75)
    iqr = q3 - q1
    
    # Límites para outliers
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    
    # Identificar outliers
    outliers = [x for x in datos if x < limite_inferior or x > limite_superior]
    
    return {
        'limite_inferior': round(limite_inferior, 2),
        'limite_superior': round(limite_superior, 2),
        'outliers': outliers,
        'cantidad_outliers': len(outliers),
        'porcentaje_outliers': round(len(outliers) / len(datos) * 100, 2),
        'interpretacion': f'Se detectaron {len(outliers)} valores atípicos ({round(len(outliers) / len(datos) * 100, 2)}%)'
    }

def analisis_completo_posicion(datos):
    """
    Realiza un análisis completo de medidas de posición
    """
    return {
        'cuartiles': calcular_cuartiles(datos),
        'deciles': calcular_deciles(datos),
        'percentiles': calcular_percentiles(datos),
        'valores_extremos': calcular_valores_extremos(datos),
        'minimo': round(np.min(datos), 2),
        'maximo': round(np.max(datos), 2),
        'rango': round(np.max(datos) - np.min(datos), 2)
    }

def crear_boxplot(datos, titulo="Diagrama de Caja y Bigotes"):
    """
    Crea un boxplot para visualizar las medidas de posición
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Boxplot vertical
    bp = ax1.boxplot(datos, vert=True, patch_artist=True, 
                     showmeans=True, meanline=True)
    
    # Personalizar colores
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][0].set_alpha(0.7)
    bp['medians'][0].set_color('red')
    bp['medians'][0].set_linewidth(2)
    bp['means'][0].set_color('green')
    bp['means'][0].set_linewidth(2)
    
    # Agregar cuartiles como texto
    cuartiles = calcular_cuartiles(datos)
    ax1.text(1.15, cuartiles['Q1'], f"Q1 = {cuartiles['Q1']}", 
             verticalalignment='center', fontsize=10, color='blue')
    ax1.text(1.15, cuartiles['Q2_Mediana'], f"Q2 = {cuartiles['Q2_Mediana']}", 
             verticalalignment='center', fontsize=10, color='red')
    ax1.text(1.15, cuartiles['Q3'], f"Q3 = {cuartiles['Q3']}", 
             verticalalignment='center', fontsize=10, color='blue')
    
    ax1.set_ylabel('Valores', fontsize=12)
    ax1.set_title(titulo, fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Boxplot horizontal con outliers destacados
    bp2 = ax2.boxplot(datos, vert=False, patch_artist=True,
                      showmeans=True, meanline=True)
    bp2['boxes'][0].set_facecolor('lightgreen')
    bp2['boxes'][0].set_alpha(0.7)
    bp2['medians'][0].set_color('red')
    bp2['medians'][0].set_linewidth(2)
    
    ax2.set_xlabel('Valores', fontsize=12)
    ax2.set_title('Boxplot Horizontal', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def crear_grafico_percentiles(datos, titulo="Percentiles"):
    """
    Crea un gráfico visual de percentiles
    """
    percentiles = list(range(0, 101, 5))
    valores = [np.percentile(datos, p) for p in percentiles]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(percentiles, valores, marker='o', linewidth=2, 
            markersize=5, color='steelblue')
    
    # Marcar cuartiles
    cuartiles = calcular_cuartiles(datos)
    ax.axhline(y=cuartiles['Q1'], color='orange', linestyle='--', 
               alpha=0.7, label=f'Q1 = {cuartiles["Q1"]}')
    ax.axhline(y=cuartiles['Q2_Mediana'], color='red', linestyle='--', 
               alpha=0.7, label=f'Q2 = {cuartiles["Q2_Mediana"]}')
    ax.axhline(y=cuartiles['Q3'], color='green', linestyle='--', 
               alpha=0.7, label=f'Q3 = {cuartiles["Q3"]}')
    
    ax.set_xlabel('Percentil', fontsize=12)
    ax.set_ylabel('Valor', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def generar_tabla_posicion(datos):
    """
    Genera una tabla resumen de todas las medidas de posición
    """
    analisis = analisis_completo_posicion(datos)
    
    datos_tabla = []
    
    # Cuartiles
    datos_tabla.append(['Q1 (Cuartil 1)', analisis['cuartiles']['Q1'], 
                       analisis['cuartiles']['interpretacion']['Q1']])
    datos_tabla.append(['Q2 (Mediana)', analisis['cuartiles']['Q2_Mediana'], 
                       analisis['cuartiles']['interpretacion']['Q2']])
    datos_tabla.append(['Q3 (Cuartil 3)', analisis['cuartiles']['Q3'], 
                       analisis['cuartiles']['interpretacion']['Q3']])
    datos_tabla.append(['IQR', analisis['cuartiles']['IQR_Rango_Intercuartilico'], 
                       analisis['cuartiles']['interpretacion']['IQR']])
    
    # Algunos deciles importantes
    datos_tabla.append(['D1 (Decil 1)', analisis['deciles']['D1'], 
                       analisis['deciles']['D1_interpretacion']])
    datos_tabla.append(['D5 (Decil 5)', analisis['deciles']['D5'], 
                       analisis['deciles']['D5_interpretacion']])
    datos_tabla.append(['D9 (Decil 9)', analisis['deciles']['D9'], 
                       analisis['deciles']['D9_interpretacion']])
    
    # Percentiles clave
    datos_tabla.append(['P25', analisis['percentiles']['P25'], 
                       analisis['percentiles']['P25_interpretacion']])
    datos_tabla.append(['P75', analisis['percentiles']['P75'], 
                       analisis['percentiles']['P75_interpretacion']])
    datos_tabla.append(['P90', analisis['percentiles']['P90'], 
                       analisis['percentiles']['P90_interpretacion']])
    
    # Valores extremos
    datos_tabla.append(['Mínimo', analisis['minimo'], 'Valor más pequeño en los datos'])
    datos_tabla.append(['Máximo', analisis['maximo'], 'Valor más grande en los datos'])
    datos_tabla.append(['Rango', analisis['rango'], 'Diferencia entre máximo y mínimo'])
    
    df = pd.DataFrame(datos_tabla, columns=['Medida', 'Valor', 'Interpretación'])
    return df

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo (edades)
    datos = np.random.randint(17, 35, 500)
    
    print("=== ANÁLISIS DE MEDIDAS DE POSICIÓN ===\n")
    
    # Cuartiles
    cuartiles = calcular_cuartiles(datos)
    print("CUARTILES:")
    print(f"Q1: {cuartiles['Q1']}")
    print(f"Q2 (Mediana): {cuartiles['Q2_Mediana']}")
    print(f"Q3: {cuartiles['Q3']}")
    print(f"IQR: {cuartiles['IQR_Rango_Intercuartilico']}\n")
    
    # Tabla completa
    print("TABLA RESUMEN:")
    tabla = generar_tabla_posicion(datos)
    print(tabla.to_string(index=False))
    
    # Valores extremos
    extremos = calcular_valores_extremos(datos)
    print(f"\nVALORES ATÍPICOS:")
    print(f"Cantidad: {extremos['cantidad_outliers']}")
    print(f"Porcentaje: {extremos['porcentaje_outliers']}%")
    
    # Gráficos
    fig1 = crear_boxplot(datos)
    fig2 = crear_grafico_percentiles(datos)
    plt.show()