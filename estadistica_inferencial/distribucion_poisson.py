"""
Distribución de Poisson - Para eventos raros en intervalos de tiempo/espacio
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import factorial
import seaborn as sns

class DistribucionPoisson:
    """Clase para la distribución de Poisson"""
    
    def __init__(self, lambd):
        """
        Inicializa la distribución de Poisson
        lambd (λ): tasa promedio de ocurrencia (debe ser > 0)
        """
        if lambd <= 0:
            raise ValueError("Lambda debe ser mayor que 0")
        
        self.lambd = lambd
        self.distribucion = stats.poisson(lambd)
    
    def probabilidad(self, k):
        """
        Calcula P(X = k) usando la fórmula de Poisson
        P(X = k) = (λ^k × e^(-λ)) / k!
        """
        if not isinstance(k, int) or k < 0:
            return {
                'k': k,
                'probabilidad': 0,
                'es_valido': False,
                'razon': 'k debe ser un entero no negativo'
            }
        
        # Calcular probabilidad
        prob = (self.lambd ** k) * np.exp(-self.lambd) / factorial(k)
        
        return {
            'k': k,
            'probabilidad': float(prob),
            'lambda': self.lambd,
            'formula': f'P(X={k}) = ({self.lambd}^{k} × e^(-{self.lambd})) / {k}!',
            'porcentaje': round(float(prob) * 100, 4),
            'es_valido': True
        }
    
    def probabilidad_acumulada(self, k, tipo='menor_igual'):
        """
        Calcula probabilidades acumuladas
        tipo: 'menor_igual' (≤), 'menor' (<), 'mayor_igual' (≥), 'mayor' (>)
        """
        if not isinstance(k, int) or k < 0:
            raise ValueError('k debe ser un entero no negativo')
        
        if tipo == 'menor_igual':  # P(X ≤ k)
            prob_acum = self.distribucion.cdf(k)
            formula = f'P(X ≤ {k})'
        elif tipo == 'menor':  # P(X < k)
            prob_acum = self.distribucion.cdf(k - 1) if k > 0 else 0
            formula = f'P(X < {k})'
        elif tipo == 'mayor_igual':  # P(X ≥ k)
            prob_acum = 1 - self.distribucion.cdf(k - 1) if k > 0 else 1
            formula = f'P(X ≥ {k})'
        elif tipo == 'mayor':  # P(X > k)
            prob_acum = 1 - self.distribucion.cdf(k)
            formula = f'P(X > {k})'
        else:
            raise ValueError("tipo debe ser 'menor_igual', 'menor', 'mayor_igual' o 'mayor'")
        
        return {
            'k': k,
            'tipo': tipo,
            'probabilidad_acumulada': float(prob_acum),
            'porcentaje': round(float(prob_acum) * 100, 2),
            'formula': formula,
            'complemento': 1 - float(prob_acum)
        }
    
    def probabilidad_intervalo(self, k1, k2):
        """
        Calcula P(k1 ≤ X ≤ k2)
        """
        if k1 > k2:
            k1, k2 = k2, k1
        
        prob = sum(self.probabilidad(k)['probabilidad'] for k in range(k1, k2 + 1))
        
        return {
            'k1': k1,
            'k2': k2,
            'probabilidad': float(prob),
            'porcentaje': round(float(prob) * 100, 2),
            'formula': f'P({k1} ≤ X ≤ {k2}) = Σ P(X=k) para k={k1} hasta k={k2}'
        }
    
    def estadisticas(self):
        """Calcula las estadísticas de la distribución"""
        media = self.lambd
        varianza = self.lambd
        desv_std = np.sqrt(self.lambd)
        
        return {
            'lambda': self.lambd,
            'media': media,
            'varianza': varianza,
            'desviacion_estandar': desv_std,
            'coeficiente_variacion': desv_std / media if media != 0 else None,
            'asimetria': 1 / np.sqrt(self.lambd),
            'curtosis': 3 + (1 / self.lambd)
        }
    
    def graficar_probabilidades(self, k_max=None, ax=None):
        """
        Genera gráfica de barras con las probabilidades P(X=k)
        
        Parameters:
        - k_max: valor máximo de k para graficar (si None, usa 3λ o mínimo 15)
        - ax: eje de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        # Definir rango de k
        if k_max is None:
            k_max = max(int(3 * self.lambd) + 5, 15)
        
        k_values = np.arange(0, k_max + 1)
        probabilidades = [self.probabilidad(k)['probabilidad'] for k in k_values]
        
        # Crear gráfica de barras
        bars = ax.bar(k_values, probabilidades, color='steelblue', alpha=0.7, 
                     edgecolor='navy', linewidth=1.5)
        
        # Resaltar la moda (valor con mayor probabilidad)
        moda_idx = np.argmax(probabilidades)
        bars[moda_idx].set_color('orange')
        bars[moda_idx].set_label(f'Moda (k={k_values[moda_idx]})')
        
        # Línea de la media
        ax.axvline(self.lambd, color='red', linestyle='--', linewidth=2,
                  label=f'λ = {self.lambd}')
        
        ax.set_xlabel('Número de eventos (k)', fontsize=12, fontweight='bold')
        ax.set_ylabel('P(X = k)', fontsize=12, fontweight='bold')
        ax.set_title(f'Distribución de Poisson: λ = {self.lambd}', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticks(k_values)
        
        return ax
    
    def graficar_acumulada(self, k_max=None, ax=None):
        """
        Genera gráfica de la función de distribución acumulada F(k) = P(X ≤ k)
        
        Parameters:
        - k_max: valor máximo de k
        - ax: eje de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        if k_max is None:
            k_max = max(int(3 * self.lambd) + 5, 15)
        
        k_values = np.arange(0, k_max + 1)
        prob_acumuladas = [self.distribucion.cdf(k) for k in k_values]
        
        # Gráfica escalonada
        ax.step(k_values, prob_acumuladas, where='post', color='darkgreen',
               linewidth=2.5, label='F(k) = P(X ≤ k)')
        
        # Marcar puntos
        ax.plot(k_values, prob_acumuladas, 'o', color='darkgreen', 
               markersize=6, alpha=0.7)
        
        # Líneas de referencia
        ax.axhline(0.5, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        ax.axhline(0.95, color='gray', linestyle=':', linewidth=1, alpha=0.5,
                  label='95% probabilidad')
        
        ax.set_xlabel('Número de eventos (k)', fontsize=12, fontweight='bold')
        ax.set_ylabel('P(X ≤ k)', fontsize=12, fontweight='bold')
        ax.set_title(f'Función de Distribución Acumulada: λ = {self.lambd}',
                    fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xticks(k_values)
        
        return ax
    
    def graficar_comparacion(self, otros_lambdas, k_max=None, ax=None):
        """
        Compara distribuciones de Poisson con diferentes valores de λ
        
        Parameters:
        - otros_lambdas: lista de valores de lambda para comparar
        - k_max: valor máximo de k
        - ax: eje de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 7))
        
        # Calcular k_max global
        if k_max is None:
            max_lambda = max([self.lambd] + otros_lambdas)
            k_max = max(int(3 * max_lambda) + 5, 20)
        
        k_values = np.arange(0, k_max + 1)
        
        # Graficar distribución actual
        probs = [self.probabilidad(k)['probabilidad'] for k in k_values]
        ax.plot(k_values, probs, 'o-', linewidth=2.5, markersize=6,
               label=f'λ = {self.lambd}')
        
        # Graficar otras distribuciones
        colores = plt.cm.Set1(np.linspace(0, 1, len(otros_lambdas)))
        for i, lambd in enumerate(otros_lambdas):
            dist = DistribucionPoisson(lambd)
            probs = [dist.probabilidad(k)['probabilidad'] for k in k_values]
            ax.plot(k_values, probs, 'o-', linewidth=2, markersize=5,
                   label=f'λ = {lambd}', color=colores[i], alpha=0.7)
        
        ax.set_xlabel('Número de eventos (k)', fontsize=12, fontweight='bold')
        ax.set_ylabel('P(X = k)', fontsize=12, fontweight='bold')
        ax.set_title('Comparación de Distribuciones de Poisson',
                    fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(k_values[::2])  # Mostrar cada 2 valores
        
        return ax
    
    def graficar_intervalos(self, intervalos, ax=None):
        """
        Visualiza probabilidades en intervalos específicos
        
        Parameters:
        - intervalos: lista de tuplas [(k1, k2), ...] representando intervalos
        - ax: eje de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        k_max = max([intervalo[1] for intervalo in intervalos]) + 5
        k_values = np.arange(0, k_max + 1)
        probabilidades = [self.probabilidad(k)['probabilidad'] for k in k_values]
        
        # Graficar todas las barras
        ax.bar(k_values, probabilidades, color='lightgray', alpha=0.5,
              edgecolor='gray', linewidth=1, label='Otras probabilidades')
        
        # Resaltar intervalos
        colores = plt.cm.Set3(np.linspace(0, 1, len(intervalos)))
        for i, (k1, k2) in enumerate(intervalos):
            k_intervalo = np.arange(k1, k2 + 1)
            probs_intervalo = [probabilidades[k] for k in k_intervalo if k < len(probabilidades)]
            prob_total = sum(probs_intervalo)
            
            ax.bar(k_intervalo, probs_intervalo, color=colores[i], alpha=0.8,
                  edgecolor='black', linewidth=1.5,
                  label=f'P({k1} ≤ X ≤ {k2}) = {prob_total:.4f}')
        
        ax.set_xlabel('Número de eventos (k)', fontsize=12, fontweight='bold')
        ax.set_ylabel('P(X = k)', fontsize=12, fontweight='bold')
        ax.set_title(f'Probabilidades en Intervalos: λ = {self.lambd}',
                    fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticks(k_values)
        
        return ax
    
    def tabla_probabilidades(self, k_max=None):
        """Genera tabla completa de probabilidades"""
        if k_max is None:
            # Calcular hasta donde la probabilidad sea significativa
            k_max = int(self.lambd + 4 * np.sqrt(self.lambd))
        
        datos = []
        prob_acumulada = 0
        
        for k in range(k_max + 1):
            prob_info = self.probabilidad(k)
            prob_k = prob_info['probabilidad']
            prob_acumulada += prob_k
            
            datos.append({
                'k': k,
                'P(X=k)': round(prob_k, 6),
                'Porcentaje': f"{round(prob_k * 100, 2)}%",
                'P(X≤k)': round(prob_acumulada, 6),
                'P(X≤k) %': f"{round(prob_acumulada * 100, 2)}%"
            })
        
        return pd.DataFrame(datos)
    
    def generar_muestra(self, tamaño_muestra):
        """Genera una muestra aleatoria"""
        muestra = self.distribucion.rvs(size=tamaño_muestra)
        
        return {
            'muestra': muestra,
            'tamaño': tamaño_muestra,
            'media_muestra': float(np.mean(muestra)),
            'varianza_muestra': float(np.var(muestra, ddof=1)),
            'media_teorica': self.lambd,
            'varianza_teorica': self.lambd,
            'frecuencias': {int(k): int(np.sum(muestra == k)) for k in np.unique(muestra)}
        }
    
    def graficar(self, k_max=None, figsize=(15, 10)):
        """Genera gráficos completos de la distribución"""
        if k_max is None:
            k_max = int(self.lambd + 4 * np.sqrt(self.lambd))
        
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # Preparar datos
        x = np.arange(0, k_max + 1)
        probabilidades = [self.probabilidad(k)['probabilidad'] for k in x]
        prob_acumuladas = np.cumsum(probabilidades)
        
        # 1. Función de masa de probabilidad
        ax1 = fig.add_subplot(gs[0, 0])
        bars = ax1.bar(x, probabilidades, alpha=0.7, color='coral', edgecolor='black')
        ax1.set_xlabel('Número de eventos (k)', fontsize=11)
        ax1.set_ylabel('P(X = k)', fontsize=11)
        ax1.set_title(f'Función de Masa\nPoisson(λ={self.lambd})', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Resaltar la moda
        stats_info = self.estadisticas()
        if isinstance(stats_info['moda'], list):
            for moda_val in stats_info['moda']:
                if 0 <= moda_val <= k_max:
                    bars[moda_val].set_color('red')
        else:
            if 0 <= stats_info['moda'] <= k_max:
                bars[stats_info['moda']].set_color('red')
        
        # 2. Función de distribución acumulada
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.step(x, prob_acumuladas, where='post', linewidth=2, color='darkgreen')
        ax2.scatter(x, prob_acumuladas, color='darkgreen', s=30, zorder=5)
        ax2.set_xlabel('k', fontsize=11)
        ax2.set_ylabel('P(X ≤ k)', fontsize=11)
        ax2.set_title('Función de Distribución\nAcumulada', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1.05)
        
        # 3. Comparación con distribución normal (si λ es grande)
        ax3 = fig.add_subplot(gs[0, 2])
        if self.lambd >= 10:
            # Aproximación normal
            mu = self.lambd
            sigma = np.sqrt(self.lambd)
            x_norm = np.linspace(0, k_max, 1000)
            y_norm = stats.norm.pdf(x_norm, mu, sigma)
            
            ax3.bar(x, probabilidades, alpha=0.6, color='coral', 
                   label='Poisson', width=0.8)
            ax3.plot(x_norm, y_norm, 'b-', linewidth=2, 
                    label=f'Normal({mu:.1f}, {sigma:.1f}²)')
            ax3.set_xlabel('x', fontsize=11)
            ax3.set_ylabel('Densidad / Probabilidad', fontsize=11)
            ax3.set_title('Aproximación Normal\n(λ ≥ 10)', fontsize=12, fontweight='bold')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        else:
            # Gráfico de barras con estadísticas
            ax3.bar(x, probabilidades, alpha=0.7, color='coral')
            ax3.axvline(stats_info['media'], color='red', linestyle='--', 
                       linewidth=2, label=f'Media = λ = {stats_info["media"]:.2f}')
            ax3.set_xlabel('k', fontsize=11)
            ax3.set_ylabel('P(X = k)', fontsize=11)
            ax3.set_title('Distribución con Media', fontsize=12, fontweight='bold')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # 4. Comparación con otras λ
        ax4 = fig.add_subplot(gs[1, 0])
        lambdas_comparar = [self.lambd * 0.5, self.lambd, self.lambd * 1.5]
        colores = ['blue', 'coral', 'green']
        
        for lam, color in zip(lambdas_comparar, colores):
            if lam > 0:
                x_comp = np.arange(0, int(lam + 3 * np.sqrt(lam)) + 1)
                probs_comp = [stats.poisson.pmf(k, lam) for k in x_comp]
                ax4.plot(x_comp, probs_comp, marker='o', label=f'λ={lam:.1f}', 
                        color=color, linewidth=2, markersize=4)
        
        ax4.set_xlabel('k', fontsize=11)
        ax4.set_ylabel('P(X = k)', fontsize=11)
        ax4.set_title('Comparación de λ', fontsize=12, fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Probabilidades acumuladas por región
        ax5 = fig.add_subplot(gs[1, 1])
        
        # Dividir en regiones
        k_25 = self.distribucion.ppf(0.25)
        k_75 = self.distribucion.ppf(0.75)
        
        colores_barras = ['lightblue' if k < k_25 else 'lightcoral' if k > k_75 else 'lightgreen' 
                          for k in x]
        ax5.bar(x, probabilidades, color=colores_barras, alpha=0.7, edgecolor='black')
        ax5.axvline(k_25, color='blue', linestyle='--', linewidth=1.5, label=f'P25 = {k_25:.0f}')
        ax5.axvline(k_75, color='red', linestyle='--', linewidth=1.5, label=f'P75 = {k_75:.0f}')
        ax5.set_xlabel('k', fontsize=11)
        ax5.set_ylabel('P(X = k)', fontsize=11)
        ax5.set_title('Distribución por Cuartiles', fontsize=12, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Tabla de estadísticas
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.axis('tight')
        ax6.axis('off')
        
        tabla_datos = [
            ['Estadística', 'Valor', 'Propiedad'],
            ['λ (lambda)', f'{self.lambd:.2f}', 'Parámetro'],
            ['Media (μ)', f'{stats_info["media"]:.2f}', 'μ = λ'],
            ['Varianza (σ²)', f'{stats_info["varianza"]:.2f}', 'σ² = λ'],
            ['Desv. Est. (σ)', f'{stats_info["desviacion_estandar"]:.2f}', 'σ = √λ'],
            ['Moda', f'{stats_info["moda"]}', '⌊λ⌋'],
            ['Asimetría', f'{stats_info["asimetria"]:.4f}', '1/√λ'],
        ]
        
        table = ax6.table(cellText=tabla_datos[1:], colLabels=tabla_datos[0],
                         cellLoc='center', loc='center',
                         colWidths=[0.35, 0.25, 0.4])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Colorear encabezado
        for i in range(len(tabla_datos[0])):
            cell = table[(0, i)]
            cell.set_facecolor('#FF9800')
            cell.set_text_props(weight='bold', color='white')
        
        ax6.set_title('Estadísticas de Poisson', fontsize=12, fontweight='bold', pad=20)
        
        plt.suptitle(f'Distribución de Poisson (λ = {self.lambd})', 
                    fontsize=16, fontweight='bold')
        return fig

def ejemplos_aplicaciones_poisson():
    """Ejemplos prácticos de la distribución de Poisson"""
    
    print("=" * 60)
    print("EJEMPLOS DE APLICACIÓN DE LA DISTRIBUCIÓN DE POISSON")
    print("=" * 60)
    
    # Ejemplo 1: Llamadas telefónicas
    print("\n📞 EJEMPLO 1: CENTRO DE LLAMADAS")
    print("-" * 60)
    print("Un centro de llamadas recibe en promedio 5 llamadas por minuto.")
    print("¿Cuál es la probabilidad de recibir exactamente 7 llamadas en un minuto?")
    
    poisson1 = DistribucionPoisson(5)
    prob_7 = poisson1.probabilidad(7)
    print(f"\nP(X = 7) = {prob_7['probabilidad']:.6f} ({prob_7['porcentaje']:.2f}%)")
    
    prob_mas_8 = poisson1.probabilidad_acumulada(8, 'mayor')
    print(f"P(X > 8) = {prob_mas_8['probabilidad_acumulada']:.6f} ({prob_mas_8['porcentaje']:.2f}%)")
    
    # Ejemplo 2: Accidentes de tráfico
    print("\n\n🚗 EJEMPLO 2: ACCIDENTES DE TRÁFICO")
    print("-" * 60)
    print("En una carretera ocurren en promedio 2 accidentes por día.")
    print("¿Cuál es la probabilidad de que NO ocurra ningún accidente?")
    
    poisson2 = DistribucionPoisson(2)
    prob_0 = poisson2.probabilidad(0)
    print(f"\nP(X = 0) = {prob_0['probabilidad']:.6f} ({prob_0['porcentaje']:.2f}%)")
    
    prob_menos_3 = poisson2.probabilidad_acumulada(3, 'menor_igual')
    print(f"P(X ≤ 3) = {prob_menos_3['probabilidad_acumulada']:.6f} ({prob_menos_3['porcentaje']:.2f}%)")
    
    # Ejemplo 3: Defectos en manufactura
    print("\n\n🏭 EJEMPLO 3: CONTROL DE CALIDAD")
    print("-" * 60)
    print("Una fábrica produce 1000 unidades/hora con 3 defectos promedio.")
    print("¿Cuál es la probabilidad de encontrar entre 2 y 5 defectos?")
    
    poisson3 = DistribucionPoisson(3)
    prob_2_5 = poisson3.probabilidad_intervalo(2, 5)
    print(f"\nP(2 ≤ X ≤ 5) = {prob_2_5['probabilidad']:.6f} ({prob_2_5['porcentaje']:.2f}%)")
    
    return poisson1, poisson2, poisson3

# Ejemplo de uso
if __name__ == "__main__":
    # Ejecutar ejemplos
    p1, p2, p3 = ejemplos_aplicaciones_poisson()
    
    # Generar gráficos
    print("\n\nGenerando gráficos...")
    fig1 = p1.graficar()
    plt.show()
    
    # Tabla de probabilidades
    print("\n\nTABLA DE PROBABILIDADES (λ=5):")
    tabla = p1.tabla_probabilidades(15)
    print(tabla.head(10))