"""
Distribución Normal (Gaussiana) - La distribución más importante en estadística
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import erf
import seaborn as sns

class DistribucionNormal:
    """Clase para la distribución Normal"""
    
    def __init__(self, mu, sigma):
        """
        Inicializa la distribución Normal
        mu (μ): media
        sigma (σ): desviación estándar (debe ser > 0)
        """
        if sigma <= 0:
            raise ValueError("La desviación estándar (sigma) debe ser mayor que 0")
        
        self.mu = mu
        self.sigma = sigma
        self.varianza = sigma ** 2
        self.distribucion = stats.norm(mu, sigma)
    
    def densidad(self, x):
        """
        Calcula la función de densidad de probabilidad f(x)
        f(x) = (1 / (σ√(2π))) × e^(-(x-μ)²/(2σ²))
        """
        coef = 1 / (self.sigma * np.sqrt(2 * np.pi))
        exponente = -((x - self.mu) ** 2) / (2 * self.varianza)
        densidad = coef * np.exp(exponente)
        
        return {
            'x': x,
            'densidad': float(densidad),
            'mu': self.mu,
            'sigma': self.sigma,
            'formula': f'f({x}) = (1/(σ√(2π))) × e^(-(x-μ)²/(2σ²))'
        }
    
    def probabilidad(self, a, b=None):
        """
        Calcula P(a ≤ X ≤ b) o P(X ≤ a) si b es None
        """
        if b is None:
            # P(X ≤ a)
            prob = self.distribucion.cdf(a)
            return {
                'tipo': 'acumulada',
                'limite': a,
                'probabilidad': float(prob),
                'porcentaje': round(float(prob) * 100, 2),
                'formula': f'P(X ≤ {a})'
            }
        else:
            # P(a ≤ X ≤ b)
            if a > b:
                a, b = b, a
            
            prob = self.distribucion.cdf(b) - self.distribucion.cdf(a)
            return {
                'tipo': 'intervalo',
                'limite_inferior': a,
                'limite_superior': b,
                'probabilidad': float(prob),
                'porcentaje': round(float(prob) * 100, 2),
                'formula': f'P({a} ≤ X ≤ {b}) = Φ({b}) - Φ({a})'
            }
    
    def probabilidad_mayor(self, x):
        """Calcula P(X > x)"""
        prob = 1 - self.distribucion.cdf(x)
        return {
            'x': x,
            'probabilidad': float(prob),
            'porcentaje': round(float(prob) * 100, 2),
            'formula': f'P(X > {x}) = 1 - Φ({x})'
        }
    
    def probabilidad_menor(self, x):
        """Calcula P(X < x)"""
        prob = self.distribucion.cdf(x)
        return {
            'x': x,
            'probabilidad': float(prob),
            'porcentaje': round(float(prob) * 100, 2),
            'formula': f'P(X < {x}) = Φ({x})'
        }
    
    def valor_z(self, x):
        """
        Calcula el valor Z estandarizado
        Z = (X - μ) / σ
        """
        z = (x - self.mu) / self.sigma
        return {
            'x': x,
            'z': round(z, 4),
            'mu': self.mu,
            'sigma': self.sigma,
            'formula': f'Z = ({x} - {self.mu}) / {self.sigma} = {z:.4f}',
            'interpretacion': f'{x} está a {abs(z):.2f} desviaciones estándar {"por encima" if z > 0 else "por debajo"} de la media'
        }
    
    def percentil(self, p):
        """
        Encuentra el valor x tal que P(X ≤ x) = p
        """
        if not 0 < p < 1:
            raise ValueError("El percentil debe estar entre 0 y 1")
        
        x = self.distribucion.ppf(p)
        return {
            'percentil': p,
            'percentil_porcentaje': f'{p * 100:.1f}%',
            'valor': float(x),
            'interpretacion': f'El {p*100:.1f}% de los valores son menores o iguales a {x:.4f}'
        }
    
    def regla_empirica(self):
        """
        Calcula las probabilidades según la regla empírica (68-95-99.7)
        """
        # P(μ - σ ≤ X ≤ μ + σ) ≈ 68%
        prob_1sigma = self.probabilidad(self.mu - self.sigma, self.mu + self.sigma)
        
        # P(μ - 2σ ≤ X ≤ μ + 2σ) ≈ 95%
        prob_2sigma = self.probabilidad(self.mu - 2*self.sigma, self.mu + 2*self.sigma)
        
        # P(μ - 3σ ≤ X ≤ μ + 3σ) ≈ 99.7%
        prob_3sigma = self.probabilidad(self.mu - 3*self.sigma, self.mu + 3*self.sigma)
        
        return {
            '1_sigma': {
                'intervalo': f'[{self.mu - self.sigma:.2f}, {self.mu + self.sigma:.2f}]',
                'probabilidad': prob_1sigma['probabilidad'],
                'porcentaje': prob_1sigma['porcentaje'],
                'teorico': 68.27
            },
            '2_sigma': {
                'intervalo': f'[{self.mu - 2*self.sigma:.2f}, {self.mu + 2*self.sigma:.2f}]',
                'probabilidad': prob_2sigma['probabilidad'],
                'porcentaje': prob_2sigma['porcentaje'],
                'teorico': 95.45
            },
            '3_sigma': {
                'intervalo': f'[{self.mu - 3*self.sigma:.2f}, {self.mu + 3*self.sigma:.2f}]',
                'probabilidad': prob_3sigma['probabilidad'],
                'porcentaje': prob_3sigma['porcentaje'],
                'teorico': 99.73
            }
        }
    
    def estadisticas(self):
        """Retorna las estadísticas de la distribución"""
        return {
            'media': self.mu,
            'mediana': self.mu,
            'moda': self.mu,
            'varianza': self.varianza,
            'desviacion_estandar': self.sigma,
            'asimetria': 0,  # Simétrica
            'curtosis': 0,   # Mesocúrtica
            'propiedad': 'En la Normal: Media = Mediana = Moda'
        }
    
    def generar_muestra(self, tamaño_muestra):
        """Genera una muestra aleatoria"""
        muestra = self.distribucion.rvs(size=tamaño_muestra)
        
        return {
            'muestra': muestra,
            'tamaño': tamaño_muestra,
            'media_muestra': float(np.mean(muestra)),
            'varianza_muestra': float(np.var(muestra, ddof=1)),
            'desviacion_muestra': float(np.std(muestra, ddof=1)),
            'media_teorica': self.mu,
            'varianza_teorica': self.varianza,
            'desviacion_teorica': self.sigma
        }
    
    def intervalo_confianza(self, nivel_confianza=0.95):
        """
        Calcula el intervalo de confianza para un nivel dado
        """
        alpha = 1 - nivel_confianza
        z_critico = stats.norm.ppf(1 - alpha/2)
        
        limite_inferior = self.mu - z_critico * self.sigma
        limite_superior = self.mu + z_critico * self.sigma
        
        return {
            'nivel_confianza': nivel_confianza,
            'nivel_confianza_porcentaje': f'{nivel_confianza * 100:.0f}%',
            'z_critico': round(z_critico, 4),
            'limite_inferior': round(limite_inferior, 4),
            'limite_superior': round(limite_superior, 4),
            'intervalo': f'[{limite_inferior:.4f}, {limite_superior:.4f}]',
            'interpretacion': f'Con {nivel_confianza*100:.0f}% de confianza, los valores están en [{limite_inferior:.2f}, {limite_superior:.2f}]'
        }
    
    def tabla_normal_estandar(self, z_min=-3, z_max=3, paso=0.5):
        """Genera tabla de valores Z y probabilidades"""
        z_valores = np.arange(z_min, z_max + paso, paso)
        
        datos = []
        for z in z_valores:
            prob_menor = stats.norm.cdf(z)
            prob_mayor = 1 - prob_menor
            x_valor = self.mu + z * self.sigma
            
            datos.append({
                'Z': round(z, 2),
                'X': round(x_valor, 2),
                'P(Z ≤ z)': round(prob_menor, 4),
                'P(Z > z)': round(prob_mayor, 4),
                '%': f'{prob_menor * 100:.1f}%'
            })
        
        return pd.DataFrame(datos)
    
    def graficar(self, figsize=(16, 12)):
        """Genera gráficos completos de la distribución"""
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        # Rango para graficar
        x_min = self.mu - 4 * self.sigma
        x_max = self.mu + 4 * self.sigma
        x = np.linspace(x_min, x_max, 1000)
        y = self.distribucion.pdf(x)
        
        # 1. Curva normal básica
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(x, y, 'b-', linewidth=2, label='Densidad')
        ax1.fill_between(x, y, alpha=0.3)
        ax1.axvline(self.mu, color='red', linestyle='--', linewidth=2, 
                   label=f'μ = {self.mu}')
        ax1.set_xlabel('X', fontsize=11)
        ax1.set_ylabel('Densidad f(x)', fontsize=11)
        ax1.set_title(f'Distribución Normal\nN(μ={self.mu}, σ²={self.varianza})', 
                     fontsize=13, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Regla empírica
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.plot(x, y, 'b-', linewidth=2)
        
        # Colorear regiones
        # 1 sigma
        x_1s = x[(x >= self.mu - self.sigma) & (x <= self.mu + self.sigma)]
        y_1s = self.distribucion.pdf(x_1s)
        ax2.fill_between(x_1s, y_1s, alpha=0.3, color='green', label='68% (±1σ)')
        
        # 2 sigma
        x_2s_left = x[(x >= self.mu - 2*self.sigma) & (x < self.mu - self.sigma)]
        x_2s_right = x[(x > self.mu + self.sigma) & (x <= self.mu + 2*self.sigma)]
        ax2.fill_between(x_2s_left, self.distribucion.pdf(x_2s_left), 
                        alpha=0.3, color='yellow')
        ax2.fill_between(x_2s_right, self.distribucion.pdf(x_2s_right), 
                        alpha=0.3, color='yellow', label='95% (±2σ)')
        
        ax2.axvline(self.mu, color='red', linestyle='--', linewidth=1.5)
        ax2.set_title('Regla Empírica\n68-95-99.7', fontsize=11, fontweight='bold')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        # 3. Función de distribución acumulada
        ax3 = fig.add_subplot(gs[1, 0])
        y_cdf = self.distribucion.cdf(x)
        ax3.plot(x, y_cdf, 'g-', linewidth=2)
        ax3.axhline(0.5, color='red', linestyle=':', alpha=0.5)
        ax3.axvline(self.mu, color='red', linestyle=':', alpha=0.5)
        ax3.set_xlabel('X', fontsize=11)
        ax3.set_ylabel('F(x) = P(X ≤ x)', fontsize=11)
        ax3.set_title('Función Acumulada', fontsize=11, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # 4. Comparación con diferentes σ
        ax4 = fig.add_subplot(gs[1, 1])
        sigmas = [self.sigma * 0.5, self.sigma, self.sigma * 1.5]
        colores = ['blue', 'red', 'green']
        
        for sig, color in zip(sigmas, colores):
            x_comp = np.linspace(self.mu - 4*sig, self.mu + 4*sig, 500)
            y_comp = stats.norm.pdf(x_comp, self.mu, sig)
            ax4.plot(x_comp, y_comp, color=color, linewidth=2, 
                    label=f'σ = {sig:.2f}', alpha=0.7)
        
        ax4.set_xlabel('X', fontsize=11)
        ax4.set_ylabel('Densidad', fontsize=11)
        ax4.set_title('Efecto de σ\n(μ constante)', fontsize=11, fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Comparación con diferentes μ
        ax5 = fig.add_subplot(gs[1, 2])
        mus = [self.mu - self.sigma, self.mu, self.mu + self.sigma]
        colores_mu = ['purple', 'red', 'orange']
        
        for mu_comp, color in zip(mus, colores_mu):
            x_comp = np.linspace(mu_comp - 4*self.sigma, mu_comp + 4*self.sigma, 500)
            y_comp = stats.norm.pdf(x_comp, mu_comp, self.sigma)
            ax5.plot(x_comp, y_comp, color=color, linewidth=2, 
                    label=f'μ = {mu_comp:.2f}', alpha=0.7)
        
        ax5.set_xlabel('X', fontsize=11)
        ax5.set_ylabel('Densidad', fontsize=11)
        ax5.set_title('Efecto de μ\n(σ constante)', fontsize=11, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Estandarización (valores Z)
        ax6 = fig.add_subplot(gs[2, 0])
        z_vals = np.linspace(-4, 4, 1000)
        y_z = stats.norm.pdf(z_vals, 0, 1)
        ax6.plot(z_vals, y_z, 'b-', linewidth=2)
        ax6.fill_between(z_vals, y_z, alpha=0.3)
        
        # Marcar puntos importantes
        for z_val in [-2, -1, 0, 1, 2]:
            ax6.axvline(z_val, color='gray', linestyle=':', alpha=0.5)
        
        ax6.set_xlabel('Z', fontsize=11)
        ax6.set_ylabel('φ(z)', fontsize=11)
        ax6.set_title('Normal Estándar\nN(0, 1)', fontsize=11, fontweight='bold')
        ax6.grid(True, alpha=0.3)
        
        # 7. Q-Q Plot
        ax7 = fig.add_subplot(gs[2, 1])
        muestra = self.generar_muestra(500)['muestra']
        stats.probplot(muestra, dist="norm", plot=ax7)
        ax7.set_title('Q-Q Plot\n(Muestra vs Normal)', fontsize=11, fontweight='bold')
        ax7.grid(True, alpha=0.3)
        
        # 8. Tabla de estadísticas y regla empírica
        ax8 = fig.add_subplot(gs[2, 2])
        ax8.axis('tight')
        ax8.axis('off')
        
        regla = self.regla_empirica()
        
        tabla_datos = [
            ['Concepto', 'Valor'],
            ['Media (μ)', f'{self.mu:.2f}'],
            ['Desv. Est. (σ)', f'{self.sigma:.2f}'],
            ['Varianza (σ²)', f'{self.varianza:.2f}'],
            ['', ''],
            ['Regla Empírica:', ''],
            ['μ ± 1σ', f"{regla['1_sigma']['porcentaje']:.1f}%"],
            ['μ ± 2σ', f"{regla['2_sigma']['porcentaje']:.1f}%"],
            ['μ ± 3σ', f"{regla['3_sigma']['porcentaje']:.1f}%"],
        ]
        
        table = ax8.table(cellText=tabla_datos[1:], colLabels=tabla_datos[0],
                         cellLoc='center', loc='center',
                         colWidths=[0.6, 0.4])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Colorear encabezado
        for i in range(len(tabla_datos[0])):
            cell = table[(0, i)]
            cell.set_facecolor('#2196F3')
            cell.set_text_props(weight='bold', color='white')
        
        ax8.set_title('Estadísticas', fontsize=11, fontweight='bold', pad=20)
        
        plt.suptitle(f'Análisis Completo - Distribución Normal N({self.mu}, {self.sigma}²)', 
                    fontsize=16, fontweight='bold')
        return fig

def ejemplos_aplicaciones_normal():
    """Ejemplos prácticos de la distribución Normal"""
    
    print("=" * 70)
    print("EJEMPLOS DE APLICACIÓN DE LA DISTRIBUCIÓN NORMAL")
    print("=" * 70)
    
    # Ejemplo 1: Alturas humanas
    print("\n📏 EJEMPLO 1: ALTURAS DE PERSONAS")
    print("-" * 70)
    print("Las alturas siguen N(μ=170cm, σ=10cm)")
    print("¿Qué porcentaje de personas miden más de 180cm?")
    
    normal1 = DistribucionNormal(170, 10)
    prob_mayor_180 = normal1.probabilidad_mayor(180)
    print(f"\nP(X > 180) = {prob_mayor_180['probabilidad']:.4f} ({prob_mayor_180['porcentaje']:.2f}%)")
    
    z_180 = normal1.valor_z(180)
    print(f"Valor Z: {z_180['z']}")
    print(f"Interpretación: {z_180['interpretacion']}")
    
    # Ejemplo 2: Notas de examen
    print("\n\n📝 EJEMPLO 2: CALIFICACIONES")
    print("-" * 70)
    print("Las notas siguen N(μ=75, σ=8)")
    print("¿Cuál es la probabilidad de obtener entre 70 y 85 puntos?")
    
    normal2 = DistribucionNormal(75, 8)
    prob_70_85 = normal2.probabilidad(70, 85)
    print(f"\nP(70 ≤ X ≤ 85) = {prob_70_85['probabilidad']:.4f} ({prob_70_85['porcentaje']:.2f}%)")
    
    # ¿Qué nota necesitas para estar en el top 10%?
    percentil_90 = normal2.percentil(0.90)
    print(f"\nPara estar en el top 10%, necesitas: {percentil_90['valor']:.2f} puntos")
    
    # Ejemplo 3: Regla empírica
    print("\n\n📊 EJEMPLO 3: REGLA EMPÍRICA")
    print("-" * 70)
    regla = normal2.regla_empirica()
    print(f"68% de las notas están entre: {regla['1_sigma']['intervalo']}")
    print(f"95% de las notas están entre: {regla['2_sigma']['intervalo']}")
    print(f"99.7% de las notas están entre: {regla['3_sigma']['intervalo']}")
    
    return normal1, normal2

# Ejemplo de uso
if __name__ == "__main__":
    # Ejecutar ejemplos
    n1, n2 = ejemplos_aplicaciones_normal()
    
    # Generar gráficos
    print("\n\nGenerando gráficos...")
    fig = n1.graficar()
    plt.show()
    
    # Tabla de valores Z
    print("\n\nTABLA DE VALORES Z:")
    tabla_z = n1.tabla_normal_estandar()
    print(tabla_z)