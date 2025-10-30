"""
Medidas de Dispersión - Varianza, Desviación Estándar, Rango, CV
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calcular_rango(datos):
    """
    Calcula el rango (diferencia entre máximo y mínimo)
    """
    minimo = np.min(datos)
    maximo = np.max(datos)
    rango = maximo - minimo
    
    return {
        'rango': round(rango, 2),
        'minimo': round(minimo, 2),
        'maximo': round(maximo, 2),
        'interpretacion': f'Los datos varían en un rango de {round(rango, 2)} unidades'
    }

def calcular_varianza(datos, poblacion=False):
    """
    Calcula la varianza (muestral o poblacional)
    
    poblacion: True para varianza poblacional, False para muestral
    """
    if poblacion:
        varianza = np.var(datos, ddof=0)
        tipo = 'poblacional'
        formula = 'σ² = Σ(xi - μ)² / N'
    else:
        varianza = np.var(datos, ddof=1)
        tipo = 'muestral'
        formula = 's² = Σ(xi - x̄)² / (n-1)'
    
    media = np.mean(datos)
    
    return {
        'varianza': round(varianza, 4),
        'tipo': tipo,
        'media': round(media, 2),
        'n': len(datos),
        'formula': formula,
        'interpretacion': f'La varianza {tipo} es {round(varianza, 4)}, indicando la dispersión promedio al cuadrado'
    }

def calcular_desviacion_estandar(datos, poblacion=False):
    """
    Calcula la desviación estándar (muestral o poblacional)
    """
    if poblacion:
        desviacion = np.std(datos, ddof=0)
        tipo = 'poblacional'
        simbolo = 'σ'
        formula = 'σ = √[Σ(xi - μ)² / N]'
    else:
        desviacion = np.std(datos, ddof=1)
        tipo = 'muestral'
        simbolo = 's'
        formula = 's = √[Σ(xi - x̄)² / (n-1)]'
    
    media = np.mean(datos)
    varianza = desviacion ** 2
    
    return {
        'desviacion_estandar': round(desviacion, 4),
        'simbolo': simbolo,
        'tipo': tipo,
        'varianza': round(varianza, 4),
        'media': round(media, 2),
        'formula': formula,
        'interpretacion': f'Los datos se desvían en promedio {round(desviacion, 4)} unidades de la media'
    }

def calcular_coeficiente_variacion(datos):
    """
    Calcula el coeficiente de variación (CV)
    CV = (desviación estándar / media) × 100
    """
    media = np.mean(datos)
    desviacion = np.std(datos, ddof=1)
    
    if media == 0:
        return {
            'error': 'No se puede calcular CV con media igual a cero'
        }
    
    cv = (desviacion / abs(media)) * 100
    
    # Interpretación del CV
    if cv < 15:
        interpretacion_cv = 'Baja variabilidad - Datos homogéneos'
    elif cv < 30:
        interpretacion_cv = 'Variabilidad moderada'
    else:
        interpretacion_cv = 'Alta variabilidad - Datos heterogéneos'
    
    return {
        'coeficiente_variacion': round(cv, 2),
        'coeficiente_variacion_porcentaje': f'{round(cv, 2)}%',
        'desviacion_estandar': round(desviacion, 4),
        'media': round(media, 2),
        'formula': 'CV = (s / x̄) × 100',
        'interpretacion': interpretacion_cv,
        'conclusion': f'El CV de {round(cv, 2)}% indica {interpretacion_cv.lower()}'
    }

def calcular_desviacion_media(datos):
    """
    Calcula la desviación media o desviación promedio
    DM = Σ|xi - x̄| / n
    """
    media = np.mean(datos)
    desviacion_media = np.mean(np.abs(datos - media))
    
    return {
        'desviacion_media': round(desviacion_media, 4),
        'media': round(media, 2),
        'formula': 'DM = Σ|xi - x̄| / n',
        'interpretacion': f'La desviación promedio absoluta de la media es {round(desviacion_media, 4)}'
    }

def calcular_rango_intercuartilico(datos):
    """
    Calcula el rango intercuartílico (IQR)
    IQR = Q3 - Q1
    """
    q1 = np.percentile(datos, 25)
    q3 = np.percentile(datos, 75)
    iqr = q3 - q1
    
    return {
        'IQR': round(iqr, 2),
        'Q1': round(q1, 2),
        'Q3': round(q3, 2),
        'formula': 'IQR = Q3 - Q1',
        'interpretacion': f'El 50% central de los datos varía en {round(iqr, 2)} unidades'
    }

def analisis_completo_dispersion(datos, poblacion=False):
    """
    Realiza un análisis completo de todas las medidas de dispersión
    """
    return {
        'rango': calcular_rango(datos),
        'varianza': calcular_varianza(datos, poblacion),
        'desviacion_estandar': calcular_desviacion_estandar(datos, poblacion),
        'coeficiente_variacion': calcular_coeficiente_variacion(datos),
        'desviacion_media': calcular_desviacion_media(datos),
        'rango_intercuartilico': calcular_rango_intercuartilico(datos)
    }

def generar_tabla_dispersion(datos, poblacion=False):
    """
    Genera una tabla resumen de todas las medidas de dispersión
    """
    analisis = analisis_completo_dispersion(datos, poblacion)
    
    datos_tabla = [
        ['Rango', 
         analisis['rango']['rango'],
         analisis['rango']['interpretacion']],
        
        ['Rango Intercuartílico (IQR)', 
         analisis['rango_intercuartilico']['IQR'],
         analisis['rango_intercuartilico']['interpretacion']],
        
        ['Varianza', 
         analisis['varianza']['varianza'],
         analisis['varianza']['interpretacion']],
        
        ['Desviación Estándar', 
         analisis['desviacion_estandar']['desviacion_estandar'],
         analisis['desviacion_estandar']['interpretacion']],
        
        ['Desviación Media', 
         analisis['desviacion_media']['desviacion_media'],
         analisis['desviacion_media']['interpretacion']],
        
        ['Coeficiente de Variación (CV)', 
         analisis['coeficiente_variacion']['coeficiente_variacion_porcentaje'],
         analisis['coeficiente_variacion']['conclusion']]
    ]
    
    df = pd.DataFrame(datos_tabla, columns=['Medida', 'Valor', 'Interpretación'])
    return df

def graficar_dispersion(datos, titulo="Análisis de Dispersión"):
    """
    Crea gráficos para visualizar las medidas de dispersión
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    media = np.mean(datos)
    desv_std = np.std(datos, ddof=1)
    
    # 1. Histograma con media y desviación estándar
    ax1 = axes[0, 0]
    ax1.hist(datos, bins=20, alpha=0.7, color='steelblue', edgecolor='black')
    ax1.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media = {media:.2f}')
    ax1.axvline(media - desv_std, color='orange', linestyle=':', linewidth=2, 
                label=f'μ - σ = {media - desv_std:.2f}')
    ax1.axvline(media + desv_std, color='orange', linestyle=':', linewidth=2, 
                label=f'μ + σ = {media + desv_std:.2f}')
    ax1.set_xlabel('Valores')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Distribución con Media y Desviación Estándar')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Boxplot
    ax2 = axes[0, 1]
    bp = ax2.boxplot(datos, vert=True, patch_artist=True)
    bp['boxes'][0].set_facecolor('lightgreen')
    bp['boxes'][0].set_alpha(0.7)
    ax2.set_ylabel('Valores')
    ax2.set_title('Diagrama de Caja (Rango y Cuartiles)')
    ax2.grid(True, alpha=0.3)
    
    # 3. Dispersión respecto a la media
    ax3 = axes[1, 0]
    desviaciones = np.abs(datos - media)
    ax3.scatter(range(len(datos)), desviaciones, alpha=0.5, color='purple')
    ax3.axhline(desv_std, color='red', linestyle='--', linewidth=2, 
                label=f'Desv. Est. = {desv_std:.2f}')
    ax3.set_xlabel('Observación')
    ax3.set_ylabel('|xi - Media|')
    ax3.set_title('Desviaciones Respecto a la Media')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Tabla resumen
    ax4 = axes[1, 1]
    ax4.axis('tight')
    ax4.axis('off')
    
    analisis = analisis_completo_dispersion(datos)
    
    tabla_datos = [
        ['Medida', 'Valor'],
        ['Rango', f"{analisis['rango']['rango']:.2f}"],
        ['IQR', f"{analisis['rango_intercuartilico']['IQR']:.2f}"],
        ['Varianza', f"{analisis['varianza']['varianza']:.4f}"],
        ['Desv. Estándar', f"{analisis['desviacion_estandar']['desviacion_estandar']:.4f}"],
        ['CV', analisis['coeficiente_variacion']['coeficiente_variacion_porcentaje']],
    ]
    
    table = ax4.table(cellText=tabla_datos[1:], colLabels=tabla_datos[0],
                     cellLoc='center', loc='center', colWidths=[0.5, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    
    # Colorear encabezado
    for i in range(len(tabla_datos[0])):
        cell = table[(0, i)]
        cell.set_facecolor('#4CAF50')
        cell.set_text_props(weight='bold', color='white')
    
    ax4.set_title('Resumen de Medidas', fontsize=12, fontweight='bold', pad=20)
    
    plt.suptitle(titulo, fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    return fig

def comparar_variabilidad(datos1, datos2, nombre1="Grupo 1", nombre2="Grupo 2"):
    """
    Compara la variabilidad entre dos conjuntos de datos usando CV
    """
    cv1 = calcular_coeficiente_variacion(datos1)
    cv2 = calcular_coeficiente_variacion(datos2)
    
    if cv1['coeficiente_variacion'] < cv2['coeficiente_variacion']:
        mas_homogeneo = nombre1
        menos_homogeneo = nombre2
    else:
        mas_homogeneo = nombre2
        menos_homogeneo = nombre1
    
    return {
        nombre1: cv1,
        nombre2: cv2,
        'conclusion': f'{mas_homogeneo} es más homogéneo que {menos_homogeneo}',
        'diferencia_cv': abs(cv1['coeficiente_variacion'] - cv2['coeficiente_variacion'])
    }

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo
    datos = np.random.randint(17, 35, 500)
    
    print("=== ANÁLISIS DE MEDIDAS DE DISPERSIÓN ===\n")
    
    # Análisis completo
    analisis = analisis_completo_dispersion(datos)
    
    print("TABLA RESUMEN:")
    tabla = generar_tabla_dispersion(datos)
    print(tabla.to_string(index=False))
    
    print(f"\nDETALLE DE COEFICIENTE DE VARIACIÓN:")
    cv = analisis['coeficiente_variacion']
    print(f"CV = {cv['coeficiente_variacion_porcentaje']}")
    print(f"Interpretación: {cv['interpretacion']}")
    
    # Gráficos
    fig = graficar_dispersion(datos)
    plt.show()