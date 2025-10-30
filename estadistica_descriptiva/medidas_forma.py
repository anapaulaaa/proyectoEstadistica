"""
Medidas de Forma - Asimetría (Skewness) y Curtosis (Kurtosis)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def calcular_asimetria(datos):
    """
    Calcula el coeficiente de asimetría (skewness)
    
    Asimetría > 0: Distribución sesgada a la derecha (cola derecha más larga)
    Asimetría = 0: Distribución simétrica
    Asimetría < 0: Distribución sesgada a la izquierda (cola izquierda más larga)
    """
    asimetria = stats.skew(datos)
    
    # Interpretación
    if asimetria > 0.5:
        interpretacion = "Asimetría positiva (sesgada a la derecha)"
        descripcion = "La mayoría de los datos se concentran a la izquierda, con cola larga hacia la derecha"
    elif asimetria < -0.5:
        interpretacion = "Asimetría negativa (sesgada a la izquierda)"
        descripcion = "La mayoría de los datos se concentran a la derecha, con cola larga hacia la izquierda"
    else:
        interpretacion = "Aproximadamente simétrica"
        descripcion = "Los datos están distribuidos de manera balanceada alrededor de la media"
    
    # Clasificación detallada
    if abs(asimetria) < 0.15:
        clasificacion = "Muy simétrica"
    elif abs(asimetria) < 0.5:
        clasificacion = "Moderadamente simétrica"
    elif abs(asimetria) < 1:
        clasificacion = "Asimetría moderada"
    else:
        clasificacion = "Asimetría alta"
    
    media = np.mean(datos)
    mediana = np.median(datos)
    
    return {
        'asimetria': round(asimetria, 4),
        'interpretacion': interpretacion,
        'descripcion': descripcion,
        'clasificacion': clasificacion,
        'media': round(media, 2),
        'mediana': round(mediana, 2),
        'relacion_media_mediana': 'Media > Mediana' if media > mediana else 'Media < Mediana' if media < mediana else 'Media = Mediana',
        'formula': 'Skewness = E[(X-μ)³] / σ³'
    }

def calcular_curtosis(datos):
    """
    Calcula el coeficiente de curtosis (kurtosis)
    
    Curtosis > 0: Distribución leptocúrtica (más puntiaguda que la normal)
    Curtosis = 0: Distribución mesocúrtica (similar a la normal)
    Curtosis < 0: Distribución platicúrtica (más plana que la normal)
    """
    # Curtosis con corrección de Fisher (excess kurtosis)
    curtosis = stats.kurtosis(datos, fisher=True)
    
    # Interpretación
    if curtosis > 0:
        interpretacion = "Leptocúrtica (más puntiaguda que la normal)"
        descripcion = "Mayor concentración de datos alrededor de la media y colas más pesadas"
    elif curtosis < 0:
        interpretacion = "Platicúrtica (más plana que la normal)"
        descripcion = "Menor concentración de datos alrededor de la media y colas más ligeras"
    else:
        interpretacion = "Mesocúrtica (similar a la normal)"
        descripcion = "Distribución similar a la curva normal en términos de apuntamiento"
    
    # Clasificación detallada
    if abs(curtosis) < 0.5:
        clasificacion = "Cercana a la normal"
    elif abs(curtosis) < 1:
        clasificacion = "Moderadamente diferente de la normal"
    elif abs(curtosis) < 2:
        clasificacion = "Considerablemente diferente de la normal"
    else:
        clasificacion = "Muy diferente de la normal"
    
    return {
        'curtosis': round(curtosis, 4),
        'interpretacion': interpretacion,
        'descripcion': descripcion,
        'clasificacion': clasificacion,
        'formula': 'Kurtosis = E[(X-μ)⁴] / σ⁴ - 3'
    }

def analisis_completo_forma(datos):
    """
    Realiza un análisis completo de las medidas de forma
    """
    asimetria = calcular_asimetria(datos)
    curtosis = calcular_curtosis(datos)
    
    # Análisis conjunto
    if abs(asimetria['asimetria']) < 0.5 and abs(curtosis['curtosis']) < 0.5:
        forma_general = "La distribución es aproximadamente normal"
    elif abs(asimetria['asimetria']) < 0.5:
        forma_general = "La distribución es simétrica pero difiere en curtosis de la normal"
    elif abs(curtosis['curtosis']) < 0.5:
        forma_general = "La distribución tiene curtosis normal pero es asimétrica"
    else:
        forma_general = "La distribución difiere significativamente de la normal"
    
    return {
        'asimetria': asimetria,
        'curtosis': curtosis,
        'forma_general': forma_general,
        'es_aproximadamente_normal': abs(asimetria['asimetria']) < 0.5 and abs(curtosis['curtosis']) < 0.5
    }

def generar_tabla_forma(datos):
    """
    Genera una tabla resumen de las medidas de forma
    """
    analisis = analisis_completo_forma(datos)
    
    datos_tabla = [
        ['Asimetría (Skewness)', 
         analisis['asimetria']['asimetria'],
         analisis['asimetria']['interpretacion']],
        
        ['Clasificación de Asimetría', 
         '—',
         analisis['asimetria']['clasificacion']],
        
        ['Curtosis (Kurtosis)', 
         analisis['curtosis']['curtosis'],
         analisis['curtosis']['interpretacion']],
        
        ['Clasificación de Curtosis', 
         '—',
         analisis['curtosis']['clasificacion']],
        
        ['Forma General', 
         '—',
         analisis['forma_general']]
    ]
    
    df = pd.DataFrame(datos_tabla, columns=['Medida', 'Valor', 'Interpretación'])
    return df

def graficar_forma(datos, titulo="Análisis de Forma de la Distribución"):
    """
    Crea gráficos para visualizar las medidas de forma
    """
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    analisis = analisis_completo_forma(datos)
    media = np.mean(datos)
    mediana = np.median(datos)
    desv = np.std(datos)
    
    # 1. Histograma con curva de densidad
    ax1 = fig.add_subplot(gs[0, :2])
    n, bins, patches = ax1.hist(datos, bins=30, density=True, alpha=0.7, 
                                 color='steelblue', edgecolor='black')
    
    # Agregar curva de densidad estimada
    from scipy.stats import gaussian_kde
    density = gaussian_kde(datos)
    xs = np.linspace(datos.min(), datos.max(), 200)
    ax1.plot(xs, density(xs), 'r-', linewidth=2, label='Densidad estimada')
    
    # Marcar media y mediana
    ax1.axvline(media, color='green', linestyle='--', linewidth=2, label=f'Media = {media:.2f}')
    ax1.axvline(mediana, color='orange', linestyle='--', linewidth=2, label=f'Mediana = {mediana:.2f}')
    
    ax1.set_xlabel('Valores')
    ax1.set_ylabel('Densidad')
    ax1.set_title('Distribución de Datos con Media y Mediana')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Comparación con distribución normal
    ax2 = fig.add_subplot(gs[0, 2])
    from scipy.stats import norm
    
    # Histograma normalizado
    ax2.hist(datos, bins=25, density=True, alpha=0.6, color='steelblue', 
             label='Datos reales', edgecolor='black')
    
    # Curva normal teórica
    xmin, xmax = ax2.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, media, desv)
    ax2.plot(x, p, 'r-', linewidth=2, label='Normal teórica')
    
    ax2.set_title('Comparación con\nDistribución Normal')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # 3. Q-Q Plot (Gráfico cuantil-cuantil)
    ax3 = fig.add_subplot(gs[1, 0])
    stats.probplot(datos, dist="norm", plot=ax3)
    ax3.set_title('Q-Q Plot\n(Comparación con Normal)')
    ax3.grid(True, alpha=0.3)
    
    # 4. Boxplot
    ax4 = fig.add_subplot(gs[1, 1])
    bp = ax4.boxplot(datos, vert=True, patch_artist=True)
    bp['boxes'][0].set_facecolor('lightcoral')
    bp['boxes'][0].set_alpha(0.7)
    ax4.set_ylabel('Valores')
    ax4.set_title('Diagrama de Caja\n(Visualización de Asimetría)')
    ax4.grid(True, alpha=0.3)
    
    # 5. Gráfico de asimetría visual
    ax5 = fig.add_subplot(gs[1, 2])
    asim = analisis['asimetria']['asimetria']
    kurt = analisis['curtosis']['curtosis']
    
    colores = ['blue' if asim < -0.5 else 'green' if asim > 0.5 else 'gray']
    ax5.bar(['Asimetría'], [asim], color=colores, alpha=0.7, width=0.5)
    ax5.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax5.axhline(y=0.5, color='orange', linestyle=':', linewidth=1, alpha=0.5)
    ax5.axhline(y=-0.5, color='orange', linestyle=':', linewidth=1, alpha=0.5)
    ax5.set_ylabel('Coeficiente')
    ax5.set_title(f'Asimetría = {asim:.3f}\n{analisis["asimetria"]["clasificacion"]}')
    ax5.grid(True, alpha=0.3, axis='y')
    
    # 6. Gráfico de curtosis visual
    ax6 = fig.add_subplot(gs[2, 0])
    colores_kurt = ['blue' if kurt < -0.5 else 'red' if kurt > 0.5 else 'gray']
    ax6.bar(['Curtosis'], [kurt], color=colores_kurt, alpha=0.7, width=0.5)
    ax6.axhline(y=0, color='green', linestyle='--', linewidth=1)
    ax6.axhline(y=0.5, color='orange', linestyle=':', linewidth=1, alpha=0.5)
    ax6.axhline(y=-0.5, color='orange', linestyle=':', linewidth=1, alpha=0.5)
    ax6.set_ylabel('Coeficiente')
    ax6.set_title(f'Curtosis = {kurt:.3f}\n{analisis["curtosis"]["clasificacion"]}')
    ax6.grid(True, alpha=0.3, axis='y')
    
    # 7. Tabla de interpretación
    ax7 = fig.add_subplot(gs[2, 1:])
    ax7.axis('tight')
    ax7.axis('off')
    
    tabla_datos = [
        ['Medida', 'Valor', 'Interpretación'],
        ['Asimetría', f'{asim:.4f}', analisis['asimetria']['interpretacion']],
        ['Tipo', '—', analisis['asimetria']['clasificacion']],
        ['Curtosis', f'{kurt:.4f}', analisis['curtosis']['interpretacion']],
        ['Tipo', '—', analisis['curtosis']['clasificacion']],
        ['Conclusión', '—', analisis['forma_general']]
    ]
    
    table = ax7.table(cellText=tabla_datos[1:], colLabels=tabla_datos[0],
                     cellLoc='left', loc='center',
                     colWidths=[0.2, 0.15, 0.65])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Colorear encabezado
    for i in range(len(tabla_datos[0])):
        cell = table[(0, i)]
        cell.set_facecolor('#FF5722')
        cell.set_text_props(weight='bold', color='white')
    
    ax7.set_title('Interpretación de Medidas de Forma', fontsize=12, 
                  fontweight='bold', pad=20)
    
    plt.suptitle(titulo, fontsize=16, fontweight='bold')
    return fig

def interpretar_forma_distribucion(asimetria_valor, curtosis_valor):
    """
    Proporciona una interpretación detallada de la forma de la distribución
    """
    interpretacion = []
    
    # Interpretación de asimetría
    if asimetria_valor > 0.5:
        interpretacion.append("📊 ASIMETRÍA POSITIVA: Los datos tienen una cola larga hacia la derecha.")
        interpretacion.append("   → La media es mayor que la mediana.")
        interpretacion.append("   → Hay valores extremos altos que jalan la distribución.")
    elif asimetria_valor < -0.5:
        interpretacion.append("📊 ASIMETRÍA NEGATIVA: Los datos tienen una cola larga hacia la izquierda.")
        interpretacion.append("   → La media es menor que la mediana.")
        interpretacion.append("   → Hay valores extremos bajos que jalan la distribución.")
    else:
        interpretacion.append("📊 DISTRIBUCIÓN SIMÉTRICA: Los datos están balanceados.")
        interpretacion.append("   → La media y mediana son muy similares.")
    
    # Interpretación de curtosis
    if curtosis_valor > 0.5:
        interpretacion.append("\n📈 LEPTOCÚRTICA: Distribución más puntiaguda que la normal.")
        interpretacion.append("   → Mayor concentración de datos cerca de la media.")
        interpretacion.append("   → Colas más pesadas (más valores extremos).")
    elif curtosis_valor < -0.5:
        interpretacion.append("\n📈 PLATICÚRTICA: Distribución más plana que la normal.")
        interpretacion.append("   → Menor concentración de datos cerca de la media.")
        interpretacion.append("   → Colas más ligeras (menos valores extremos).")
    else:
        interpretacion.append("\n📈 MESOCÚRTICA: Similar a la distribución normal.")
        interpretacion.append("   → Apuntamiento comparable a la curva normal.")
    
    return "\n".join(interpretacion)

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo
    datos = np.random.randint(17, 35, 500)
    
    print("=== ANÁLISIS DE MEDIDAS DE FORMA ===\n")
    
    # Análisis completo
    analisis = analisis_completo_forma(datos)
    
    print("TABLA RESUMEN:")
    tabla = generar_tabla_forma(datos)
    print(tabla.to_string(index=False))
    
    print(f"\n{analisis['forma_general']}")
    
    print("\nINTERPRETACIÓN DETALLADA:")
    interpretacion = interpretar_forma_distribucion(
        analisis['asimetria']['asimetria'],
        analisis['curtosis']['curtosis']
    )
    print(interpretacion)
    
    # Gráficos
    fig = graficar_forma(datos)
    plt.show()