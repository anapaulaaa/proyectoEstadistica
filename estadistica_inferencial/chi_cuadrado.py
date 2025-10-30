"""
Prueba de Chi-cuadrado (χ²)
Módulo para pruebas de independencia y bondad de ajuste
"""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


class PruebaChiCuadrado:
    """Clase para realizar pruebas de Chi-cuadrado"""
    
    def __init__(self):
        self.tabla_contingencia = None
        self.chi2_stat = None
        self.p_value = None
        self.grados_libertad = None
        self.valores_esperados = None
    
    def prueba_independencia(self, tabla_observada):
        """
        Prueba de independencia entre dos variables categóricas
        
        Parámetros:
        -----------
        tabla_observada : array-like o DataFrame
            Tabla de contingencia con frecuencias observadas
        
        Retorna:
        --------
        dict : Resultados de la prueba
        """
        # Convertir a numpy array si es necesario
        if isinstance(tabla_observada, pd.DataFrame):
            self.tabla_contingencia = tabla_observada.values
        else:
            self.tabla_contingencia = np.array(tabla_observada)
        
        # Realizar la prueba
        self.chi2_stat, self.p_value, self.grados_libertad, self.valores_esperados = \
            stats.chi2_contingency(self.tabla_contingencia)
        
        # Interpretación
        alpha = 0.05
        if self.p_value < alpha:
            conclusion = "Rechazamos H₀: Las variables SÍ están relacionadas (dependientes)"
            decision = "Rechazar H₀"
        else:
            conclusion = "No rechazamos H₀: Las variables NO están relacionadas (independientes)"
            decision = "No rechazar H₀"
        
        resultados = {
            'chi2_estadistico': self.chi2_stat,
            'p_value': self.p_value,
            'grados_libertad': self.grados_libertad,
            'valores_esperados': self.valores_esperados,
            'valores_observados': self.tabla_contingencia,
            'decision': decision,
            'conclusion': conclusion,
            'alpha': alpha
        }
        
        return resultados
    
    def bondad_ajuste(self, observados, esperados=None):
        """
        Prueba de bondad de ajuste (si los datos se ajustan a una distribución esperada)
        
        Parámetros:
        -----------
        observados : array-like
            Frecuencias observadas
        esperados : array-like, opcional
            Frecuencias esperadas. Si es None, se asume distribución uniforme
        
        Retorna:
        --------
        dict : Resultados de la prueba
        """
        observados = np.array(observados)
        
        # Si no se proporcionan esperados, asumir distribución uniforme
        if esperados is None:
            n_total = observados.sum()
            n_categorias = len(observados)
            esperados = np.array([n_total / n_categorias] * n_categorias)
        else:
            esperados = np.array(esperados)
        
        # Realizar la prueba
        self.chi2_stat, self.p_value = stats.chisquare(observados, esperados)
        self.grados_libertad = len(observados) - 1
        
        # Interpretación
        alpha = 0.05
        if self.p_value < alpha:
            conclusion = "Rechazamos H₀: Los datos NO se ajustan a la distribución esperada"
            decision = "Rechazar H₀"
        else:
            conclusion = "No rechazamos H₀: Los datos SÍ se ajustan a la distribución esperada"
            decision = "No rechazar H₀"
        
        resultados = {
            'chi2_estadistico': self.chi2_stat,
            'p_value': self.p_value,
            'grados_libertad': self.grados_libertad,
            'valores_observados': observados,
            'valores_esperados': esperados,
            'decision': decision,
            'conclusion': conclusion,
            'alpha': alpha
        }
        
        return resultados
    
    def calcular_residuos(self):
        """
        Calcula los residuos estandarizados (para ver qué celdas contribuyen más)
        """
        if self.valores_esperados is None:
            raise ValueError("Primero debe ejecutar una prueba")
        
        residuos = (self.tabla_contingencia - self.valores_esperados) / np.sqrt(self.valores_esperados)
        return residuos
    
    def graficar_comparacion(self, observados, esperados, categorias=None, titulo="Comparación: Observados vs Esperados"):
        """
        Crea un gráfico de barras comparando valores observados vs esperados
        
        Parámetros:
        -----------
        observados : array-like
            Valores observados
        esperados : array-like
            Valores esperados
        categorias : list, opcional
            Nombres de las categorías
        titulo : str
            Título del gráfico
        
        Retorna:
        --------
        Figure : Figura de matplotlib
        """
        if categorias is None:
            categorias = [f'Cat {i+1}' for i in range(len(observados))]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(categorias))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, observados, width, label='Observados', 
                      color='steelblue', edgecolor='black', alpha=0.8)
        bars2 = ax.bar(x + width/2, esperados, width, label='Esperados', 
                      color='coral', edgecolor='black', alpha=0.8)
        
        # Agregar valores en las barras
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Categorías', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categorias, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def graficar_heatmap(self, tabla, titulo="Tabla de Contingencia", etiquetas_filas=None, etiquetas_columnas=None):
        """
        Crea un heatmap de la tabla de contingencia
        
        Parámetros:
        -----------
        tabla : array-like
            Tabla de contingencia
        titulo : str
            Título del gráfico
        etiquetas_filas : list, opcional
            Nombres de las filas
        etiquetas_columnas : list, opcional
            Nombres de las columnas
        
        Retorna:
        --------
        Figure : Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(tabla, cmap='YlOrRd', aspect='auto')
        
        # Configurar etiquetas
        if etiquetas_filas is None:
            etiquetas_filas = [f'Fila {i+1}' for i in range(tabla.shape[0])]
        if etiquetas_columnas is None:
            etiquetas_columnas = [f'Col {i+1}' for i in range(tabla.shape[1])]
        
        ax.set_xticks(np.arange(len(etiquetas_columnas)))
        ax.set_yticks(np.arange(len(etiquetas_filas)))
        ax.set_xticklabels(etiquetas_columnas)
        ax.set_yticklabels(etiquetas_filas)
        
        # Rotar etiquetas
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Agregar valores en las celdas
        for i in range(len(etiquetas_filas)):
            for j in range(len(etiquetas_columnas)):
                text = ax.text(j, i, int(tabla[i, j]),
                             ha="center", va="center", color="black", 
                             fontweight='bold', fontsize=12)
        
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        fig.colorbar(im, ax=ax, label='Frecuencia')
        
        plt.tight_layout()
        return fig


def ejemplo_uso():
    """Ejemplo de uso de la clase"""
    chi = PruebaChiCuadrado()
    
    # Ejemplo 1: Prueba de independencia
    print("=" * 70)
    print("EJEMPLO 1: Prueba de Independencia")
    print("=" * 70)
    print("¿El género está relacionado con la preferencia de producto?")
    print()
    
    # Tabla de contingencia: Género (filas) x Preferencia (columnas)
    tabla = np.array([
        [30, 20, 10],  # Masculino
        [15, 25, 20]   # Femenino
    ])
    
    resultados = chi.prueba_independencia(tabla)
    
    print(f"χ² = {resultados['chi2_estadistico']:.4f}")
    print(f"p-value = {resultados['p_value']:.4f}")
    print(f"Grados de libertad = {resultados['grados_libertad']}")
    print(f"\nDecisión: {resultados['decision']}")
    print(f"Conclusión: {resultados['conclusion']}")
    
    # Ejemplo 2: Bondad de ajuste
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Bondad de Ajuste")
    print("=" * 70)
    print("¿Los dados están equilibrados?")
    print()
    
    observados = [18, 22, 15, 20, 19, 26]  # Lanzamientos de un dado
    
    resultados2 = chi.bondad_ajuste(observados)
    
    print(f"χ² = {resultados2['chi2_estadistico']:.4f}")
    print(f"p-value = {resultados2['p_value']:.4f}")
    print(f"Grados de libertad = {resultados2['grados_libertad']}")
    print(f"\nDecisión: {resultados2['decision']}")
    print(f"Conclusión: {resultados2['conclusion']}")


if __name__ == "__main__":
    ejemplo_uso()
