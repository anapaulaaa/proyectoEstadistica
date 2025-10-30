import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import comb
import seaborn as sns
from fractions import Fraction

class DistribucionBernoulli:
    """Clase para la distribución de Bernoulli"""
    
    def __init__(self, p):
        """
        Inicializa la distribución de Bernoulli
        p: probabilidad de éxito (0 < p < 1)
        """
        if not 0 <= p <= 1:
            raise ValueError("La probabilidad p debe estar entre 0 y 1")
        
        self.p = p
        self.q = 1 - p  # Probabilidad de fracaso
        self.distribucion = stats.bernoulli(p)
    
    def probabilidad(self, k):
        """
        Calcula P(X = k) para k ∈ {0, 1}
        """
        if k not in [0, 1]:
            return 0
        
        prob = self.p if k == 1 else self.q
        return {
            'k': k,
            'probabilidad': prob,
            'fraccion': str(Fraction(prob).limit_denominator()),
            'porcentaje': round(prob * 100, 2),
            'formula': f"P(X={k}) = p^{k} * (1-p)^{1-k} = {self.p}^{k} * {self.q}^{1-k}"
        }
    
    def estadisticas(self):
        """Calcula las estadísticas de la distribución"""
        media = self.p
        varianza = self.p * self.q
        desviacion = np.sqrt(varianza)
        
        return {
            'media': media,
            'varianza': varianza,
            'desviacion_estandar': desviacion,
            'moda': 1 if self.p > 0.5 else 0 if self.p < 0.5 else "0 y 1",
            'asimetria': (self.q - self.p) / np.sqrt(self.p * self.q) if self.p * self.q > 0 else None,
            'parametros': {'p': self.p, 'q': self.q}
        }
    
    def generar_muestra(self, n):
        """Genera una muestra aleatoria de tamaño n"""
        muestra = self.distribucion.rvs(size=n)
        
        return {
            'muestra': muestra,
            'tamaño': n,
            'exitos': np.sum(muestra),
            'fracasos': n - np.sum(muestra),
            'proporcion_exitos': np.mean(muestra),
            'proporcion_fracasos': 1 - np.mean(muestra)
        }
    
    def tabla_probabilidades(self):
        """Genera tabla con todas las probabilidades"""
        datos = []
        for k in [0, 1]:
            prob_info = self.probabilidad(k)
            datos.append({
                'X': k,
                'Evento': 'Fracaso' if k == 0 else 'Éxito',
                'P(X=k)': prob_info['probabilidad'],
                'Fracción': prob_info['fraccion'],
                'Porcentaje': f"{prob_info['porcentaje']}%"
            })
        
        return pd.DataFrame(datos)
    
    def graficar(self, figsize=(10, 6)):
        """Genera gráficos de la distribución"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Gráfico de barras
        x = [0, 1]
        probabilidades = [self.q, self.p]
        colores = ['red', 'green']
        
        bars = ax1.bar(x, probabilidades, color=colores, alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Resultado (X)')
        ax1.set_ylabel('Probabilidad P(X=k)')
        ax1.set_title(f'Distribución de Bernoulli (p={self.p})')
        ax1.set_xticks([0, 1])
        ax1.set_xticklabels(['Fracaso (0)', 'Éxito (1)'])
        ax1.grid(True, alpha=0.3)
        
        # Añadir valores sobre las barras
        for bar, prob in zip(bars, probabilidades):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{prob:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico circular
        ax2.pie(probabilidades, labels=['Fracaso', 'Éxito'], 
                colors=colores, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Distribución de Probabilidades')
        
        plt.tight_layout()
        return fig

class DistribucionBinomial:
    """Clase para la distribución Binomial"""
    
    def __init__(self, n, p):
        """
        Inicializa la distribución Binomial
        n: número de ensayos
        p: probabilidad de éxito en cada ensayo
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n debe ser un entero positivo")
        if not 0 <= p <= 1:
            raise ValueError("La probabilidad p debe estar entre 0 y 1")
        
        self.n = n
        self.p = p
        self.q = 1 - p
        self.distribucion = stats.binom(n, p)
    
    def probabilidad(self, k):
        """
        Calcula P(X = k) usando la fórmula binomial
        P(X = k) = C(n,k) * p^k * (1-p)^(n-k)
        """
        if not isinstance(k, int) or k < 0 or k > self.n:
            return {
                'k': k,
                'probabilidad': 0,
                'es_valido': False,
                'razon': f"k debe ser un entero entre 0 y {self.n}"
            }
        
        coef_binomial = comb(self.n, k, exact=True)
        prob = coef_binomial * (self.p ** k) * (self.q ** (self.n - k))
        
        return {
            'k': k,
            'probabilidad': prob,
            'coeficiente_binomial': coef_binomial,
            'fraccion': str(Fraction(prob).limit_denominator(10000)),
            'porcentaje': round(prob * 100, 4),
            'formula': f"P(X={k}) = C({self.n},{k}) * {self.p}^{k} * {self.q}^{self.n-k}",
            'formula_numerica': f"P(X={k}) = {coef_binomial} * {self.p**k:.6f} * {self.q**(self.n-k):.6f}",
            'es_valido': True
        }
    
    def probabilidad_acumulada(self, k, tipo='menor_igual'):
        """
        Calcula probabilidades acumuladas
        tipo: 'menor_igual' (≤), 'menor' (<), 'mayor_igual' (≥), 'mayor' (>)
        """
        if not isinstance(k, int) or k < 0 or k > self.n:
            raise ValueError(f"k debe ser un entero entre 0 y {self.n}")
        
        if tipo == 'menor_igual':  # P(X ≤ k)
            prob_acum = sum(self.probabilidad(i)['probabilidad'] for i in range(k + 1))
            formula = f"P(X ≤ {k})"
        elif tipo == 'menor':  # P(X < k)
            prob_acum = sum(self.probabilidad(i)['probabilidad'] for i in range(k))
            formula = f"P(X < {k})"
        elif tipo == 'mayor_igual':  # P(X ≥ k)
            prob_acum = sum(self.probabilidad(i)['probabilidad'] for i in range(k, self.n + 1))
            formula = f"P(X ≥ {k})"
        elif tipo == 'mayor':  # P(X > k)
            prob_acum = sum(self.probabilidad(i)['probabilidad'] for i in range(k + 1, self.n + 1))
            formula = f"P(X > {k})"
        else:
            raise ValueError("tipo debe ser 'menor_igual', 'menor', 'mayor_igual' o 'mayor'")
        
        return {
            'k': k,
            'tipo': tipo,
            'probabilidad_acumulada': prob_acum,
            'porcentaje': round(prob_acum * 100, 2),
            'formula': formula,
            'complemento': 1 - prob_acum
        }
    
    def estadisticas(self):
        """Calcula las estadísticas de la distribución"""
        media = self.n * self.p
        varianza = self.n * self.p * self.q
        desviacion = np.sqrt(varianza)
        
        # Moda
        if (self.n + 1) * self.p == int((self.n + 1) * self.p):
            moda = [int((self.n + 1) * self.p) - 1, int((self.n + 1) * self.p)]
        else:
            moda = int((self.n + 1) * self.p)
        
        return {
            'media': media,
            'varianza': varianza,
            'desviacion_estandar': desviacion,
            'moda': moda,
            'asimetria': (self.q - self.p) / np.sqrt(self.n * self.p * self.q) if self.n * self.p * self.q > 0 else None,
            'parametros': {'n': self.n, 'p': self.p, 'q': self.q}
        }
    
    def tabla_probabilidades(self, mostrar_acumulada=True):
        """Genera tabla completa de probabilidades"""
        datos = []
        prob_acumulada = 0
        
        for k in range(self.n + 1):
            prob_info = self.probabilidad(k)
            prob_k = prob_info['probabilidad']
            prob_acumulada += prob_k
            
            fila = {
                'k': k,
                'P(X=k)': round(prob_k, 6),
                'Porcentaje': f"{round(prob_k * 100, 2)}%",
                'C(n,k)': prob_info['coeficiente_binomial']
            }
            
            if mostrar_acumulada:
                fila['P(X≤k)'] = round(prob_acumulada, 6)
                fila['P(X≤k) %'] = f"{round(prob_acumulada * 100, 2)}%"
            
            datos.append(fila)
        
        return pd.DataFrame(datos)
    
    def generar_muestra(self, tamaño_muestra):
        """Genera una muestra aleatoria"""
        muestra = self.distribucion.rvs(size=tamaño_muestra)
        
        return {
            'muestra': muestra,
            'tamaño': tamaño_muestra,
            'media_muestra': np.mean(muestra),
            'varianza_muestra': np.var(muestra, ddof=1),
            'media_teorica': self.n * self.p,
            'varianza_teorica': self.n * self.p * self.q,
            'frecuencias': {str(k): np.sum(muestra == k) for k in range(self.n + 1) if np.sum(muestra == k) > 0}
        }
    
    def graficar(self, figsize=(15, 10), mostrar_normal=False):
        """Genera gráficos completos de la distribución"""
        fig = plt.figure(figsize=figsize)
        
        # Preparar datos
        x = np.arange(0, self.n + 1)
        probabilidades = [self.probabilidad(k)['probabilidad'] for k in x]
        prob_acumuladas = np.cumsum(probabilidades)
        
        # Layout de subplots
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # 1. Función de masa de probabilidad
        ax1 = fig.add_subplot(gs[0, 0])
        bars = ax1.bar(x, probabilidades, alpha=0.7, color='steelblue', edgecolor='black')
        ax1.set_xlabel('Número de éxitos (k)')
        ax1.set_ylabel('P(X = k)')
        ax1.set_title(f'Función de Masa\nBinomial(n={self.n}, p={self.p})')
        ax1.grid(True, alpha=0.3)
        
        # Resaltar la moda
        stats_info = self.estadisticas()
        if isinstance(stats_info['moda'], list):
            for moda_val in stats_info['moda']:
                if 0 <= moda_val <= self.n:
                    bars[moda_val].set_color('red')
        else:
            if 0 <= stats_info['moda'] <= self.n:
                bars[stats_info['moda']].set_color('red')
        
        # 2. Función de distribución acumulada
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.step(x, prob_acumuladas, where='post', linewidth=2, color='green')
        ax2.scatter(x, prob_acumuladas, color='green', s=30, zorder=5)
        ax2.set_xlabel('k')
        ax2.set_ylabel('P(X ≤ k)')
        ax2.set_title('Función de Distribución\nAcumulada')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1.05)
        
        # 3. Comparación con distribución normal (si es apropiado)
        ax3 = fig.add_subplot(gs[0, 2])
        if mostrar_normal and self.n * self.p >= 5 and self.n * self.q >= 5:
            # Aproximación normal
            mu = self.n * self.p
            sigma = np.sqrt(self.n * self.p * self.q)
            x_norm = np.linspace(0, self.n, 1000)
            y_norm = stats.norm.pdf(x_norm, mu, sigma)
            
            ax3.bar(x, probabilidades, alpha=0.6, color='steelblue', 
                   label='Binomial', width=0.8)
            ax3.plot(x_norm, y_norm, 'r-', linewidth=2, 
                    label=f'Normal({mu:.1f}, {sigma:.1f}²)')
            ax3.set_xlabel('x')
            ax3.set_ylabel('Densidad / Probabilidad')
            ax3.set_title('Comparación con\nAproximación Normal')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        else:
            # Gráfico de barras con estadísticas
            ax3.bar(x, probabilidades, alpha=0.7, color='steelblue')
            ax3.axvline(stats_info['media'], color='red', linestyle='--', 
                       linewidth=2, label=f'Media = {stats_info["media"]:.2f}')
            ax3.axvline(stats_info['media'] - stats_info['desviacion_estandar'], 
                       color='orange', linestyle=':', alpha=0.7, 
                       label=f'μ ± σ')
            ax3.axvline(stats_info['media'] + stats_info['desviacion_estandar'], 
                       color='orange', linestyle=':', alpha=0.7)
            ax3.set_xlabel('k')
            ax3.set_ylabel('P(X = k)')
            ax3.set_title('Distribución con\nEstadísticas')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # 4. Heatmap de probabilidades (si n no es muy grande)
        if self.n <= 20:
            ax4 = fig.add_subplot(gs[1, 0])
            prob_matrix = np.array(probabilidades).reshape(1, -1)
            im = ax4.imshow(prob_matrix, cmap='YlOrRd', aspect='auto')
            ax4.set_xticks(range(len(x)))
            ax4.set_xticklabels(x)
            ax4.set_yticks([])
            ax4.set_xlabel('k')
            ax4.set_title('Mapa de Calor\nde Probabilidades')
            
            # Añadir valores en el heatmap
            for i in range(len(probabilidades)):
                ax4.text(i, 0, f'{probabilidades[i]:.3f}', 
                        ha='center', va='center', fontsize=8)
            
            plt.colorbar(im, ax=ax4, orientation='horizontal', pad=0.1)
        else:
            ax4 = fig.add_subplot(gs[1, 0])
            ax4.hist([k for k in x for _ in range(int(probabilidades[k] * 1000))], 
                    bins=min(20, self.n//2), alpha=0.7, color='steelblue', edgecolor='black')
            ax4.set_xlabel('k')
            ax4.set_ylabel('Frecuencia simulada')
            ax4.set_title('Histograma Simulado')
            ax4.grid(True, alpha=0.3)
        
        # 5. Tabla de estadísticas
        ax5 = fig.add_subplot(gs[1, 1:])
        ax5.axis('tight')
        ax5.axis('off')
        
        # Crear tabla de estadísticas
        stats_data = [
            ['Parámetro', 'Valor', 'Fórmula'],
            ['n (ensayos)', f'{self.n}', '—'],
            ['p (prob. éxito)', f'{self.p}', '—'],
            ['q (prob. fracaso)', f'{self.q:.4f}', '1 - p'],
            ['Media (μ)', f'{stats_info["media"]:.4f}', 'n × p'],
            ['Varianza (σ²)', f'{stats_info["varianza"]:.4f}', 'n × p × q'],
            ['Desv. Estándar (σ)', f'{stats_info["desviacion_estandar"]:.4f}', '√(n × p × q)'],
            ['Moda', f'{stats_info["moda"]}', '⌊(n+1)p⌋'],
        ]
        
        if stats_info["asimetria"] is not None:
            stats_data.append(['Asimetría', f'{stats_info["asimetria"]:.4f}', '(q-p)/√(npq)'])
        
        table = ax5.table(cellText=stats_data[1:], colLabels=stats_data[0],
                         cellLoc='center', loc='center',
                         colWidths=[0.3, 0.3, 0.4])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        
        # Estilizar la tabla
        for i in range(len(stats_data)):
            for j in range(len(stats_data[0])):
                cell = table[(i, j)]
                if i == 0:  # Header
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax5.set_title('Estadísticas de la Distribución', pad=20, fontsize=12, fontweight='bold')
        
        return fig
    
    def intervalo_confianza(self, nivel_confianza=0.95):
        """
        Calcula intervalos de confianza para el número de éxitos
        """
        alpha = 1 - nivel_confianza
        
        # Método exacto usando distribución binomial
        limite_inferior = self.distribucion.ppf(alpha/2)
        limite_superior = self.distribucion.ppf(1 - alpha/2)
        
        # Aproximación normal (si aplicable)
        mu = self.n * self.p
        sigma = np.sqrt(self.n * self.p * self.q)
        
        z_score = stats.norm.ppf(1 - alpha/2)
        limite_inf_normal = max(0, mu - z_score * sigma)
        limite_sup_normal = min(self.n, mu + z_score * sigma)
        
        return {
            'nivel_confianza': nivel_confianza,
            'metodo_exacto': {
                'limite_inferior': int(np.ceil(limite_inferior)) if limite_inferior >= 0 else 0,
                'limite_superior': int(np.floor(limite_superior)) if limite_superior <= self.n else self.n
            },
            'aproximacion_normal': {
                'limite_inferior': limite_inf_normal,
                'limite_superior': limite_sup_normal,
                'aplicable': self.n * self.p >= 5 and self.n * self.q >= 5
            },
            'interpretacion': f"Con {nivel_confianza*100}% de confianza, el número de éxitos estará en el intervalo calculado"
        }

def comparar_distribuciones():
    """Función para comparar diferentes distribuciones binomiales"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Diferentes combinaciones de parámetros
    parametros = [
        {'n': 10, 'p': 0.3, 'titulo': 'n=10, p=0.3'},
        {'n': 20, 'p': 0.5, 'titulo': 'n=20, p=0.5'},
        {'n': 50, 'p': 0.1, 'titulo': 'n=50, p=0.1'},
        {'n': 30, 'p': 0.8, 'titulo': 'n=30, p=0.8'}
    ]
    
    for i, params in enumerate(parametros):
        row, col = divmod(i, 2)
        ax = axes[row, col]
        
        # Crear distribución
        dist = DistribucionBinomial(params['n'], params['p'])
        x = np.arange(0, params['n'] + 1)
        probabilidades = [dist.probabilidad(k)['probabilidad'] for k in x]
        
        # Graficar
        ax.bar(x, probabilidades, alpha=0.7, color=f'C{i}', edgecolor='black')
        
        # Estadísticas
        stats_info = dist.estadisticas()
        ax.axvline(stats_info['media'], color='red', linestyle='--', 
                  linewidth=2, label=f'μ = {stats_info["media"]:.1f}')
        
        ax.set_xlabel('Número de éxitos (k)')
        ax.set_ylabel('P(X = k)')
        ax.set_title(f'Binomial: {params["titulo"]}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Comparación de Distribuciones Binomiales', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def ejemplo_bernoulli():
    """Ejemplo práctico de distribución de Bernoulli"""
    print("=== EJEMPLO: DISTRIBUCIÓN DE BERNOULLI ===")
    print("Lanzar una moneda sesgada (p=0.7 para cara)")
    print()
    
    # Crear distribución
    bernoulli = DistribucionBernoulli(0.7)
    
    # Mostrar probabilidades
    print("Probabilidades:")
    for k in [0, 1]:
        prob_info = bernoulli.probabilidad(k)
        evento = "Cruz" if k == 0 else "Cara"
        print(f"P(X={k}) [{evento}] = {prob_info['probabilidad']:.3f} ({prob_info['porcentaje']}%)")
    
    # Estadísticas
    stats = bernoulli.estadisticas()
    print(f"\nEstadísticas:")
    print(f"Media = {stats['media']:.3f}")
    print(f"Varianza = {stats['varianza']:.3f}")
    print(f"Desviación estándar = {stats['desviacion_estandar']:.3f}")
    
    # Generar muestra
    muestra = bernoulli.generar_muestra(1000)
    print(f"\nMuestra de 1000 lanzamientos:")
    print(f"Éxitos observados: {muestra['exitos']}")
    print(f"Proporción de éxitos: {muestra['proporcion_exitos']:.3f}")
    print(f"Proporción esperada: {bernoulli.p}")
    
    return bernoulli

def ejemplo_binomial():
    """Ejemplo práctico de distribución binomial"""
    print("\n=== EJEMPLO: DISTRIBUCIÓN BINOMIAL ===")
    print("Lanzar 10 monedas justas (n=10, p=0.5)")
    print()
    
    # Crear distribución
    binomial = DistribucionBinomial(10, 0.5)
    
    # Mostrar algunas probabilidades específicas
    valores_interes = [0, 5, 10]
    print("Probabilidades específicas:")
    for k in valores_interes:
        prob_info = binomial.probabilidad(k)
        print(f"P(X={k}) = {prob_info['probabilidad']:.6f} ({prob_info['porcentaje']:.2f}%)")
    
    # Probabilidades acumuladas
    print(f"\nProbabilidades acumuladas:")
    print(f"P(X ≤ 5) = {binomial.probabilidad_acumulada(5)['probabilidad_acumulada']:.6f}")
    print(f"P(X ≥ 7) = {binomial.probabilidad_acumulada(7, 'mayor_igual')['probabilidad_acumulada']:.6f}")
    
    # Estadísticas
    stats = binomial.estadisticas()
    print(f"\nEstadísticas:")
    print(f"Media = {stats['media']}")
    print(f"Varianza = {stats['varianza']}")
    print(f"Desviación estándar = {stats['desviacion_estandar']:.3f}")
    print(f"Moda = {stats['moda']}")
    
    # Intervalo de confianza
    ic = binomial.intervalo_confianza(0.95)
    print(f"\nIntervalo de confianza 95%:")
    print(f"Método exacto: [{ic['metodo_exacto']['limite_inferior']}, {ic['metodo_exacto']['limite_superior']}]")
    
    return binomial

if __name__ == "__main__":
    # Ejecutar ejemplos
    bern = ejemplo_bernoulli()
    binom = ejemplo_binomial()
    
    # Generar gráficos
    try:
        fig1 = bern.graficar()
        plt.show()
        
        fig2 = binom.graficar(mostrar_normal=True)
        plt.show()
        
        fig3 = comparar_distribuciones()
        plt.show()
        
    except Exception as e:
        print(f"Error al generar gráficos: {e}")