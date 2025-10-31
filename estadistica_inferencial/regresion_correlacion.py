"""
Análisis de Correlación y Regresión (Simple y Múltiple)
Incluye: Lineal, Exponencial, Logarítmica
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import seaborn as sns

class CorrelacionLineal:
    """Clase para análisis de correlación"""
    
    def __init__(self, x, y):
        """
        Inicializa con dos variables
        x: variable independiente
        y: variable dependiente
        """
        self.x = np.array(x)
        self.y = np.array(y)
        
        if len(self.x) != len(self.y):
            raise ValueError("x e y deben tener la misma longitud")
    
    def coeficiente_correlacion_pearson(self):
        """
        Calcula el coeficiente de correlación de Pearson (r)
        r ∈ [-1, 1]
        """
        r, p_valor = stats.pearsonr(self.x, self.y)
        
        # Interpretación
        if abs(r) < 0.3:
            interpretacion = "Correlación débil"
        elif abs(r) < 0.7:
            interpretacion = "Correlación moderada"
        else:
            interpretacion = "Correlación fuerte"
        
        if r > 0:
            direccion = "positiva (directa)"
        elif r < 0:
            direccion = "negativa (inversa)"
        else:
            direccion = "nula"
        
        return {
            'r': round(r, 4),
            'r_cuadrado': round(r**2, 4),
            'p_valor': round(p_valor, 6),
            'significativo': p_valor < 0.05,
            'interpretacion': f"{interpretacion} {direccion}",
            'fuerza': interpretacion,
            'direccion': direccion,
            'formula': 'r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]'
        }
    
    def matriz_correlacion(self):
        """Genera matriz de correlación"""
        datos = np.column_stack([self.x, self.y])
        matriz = np.corrcoef(datos.T)
        
        return pd.DataFrame(matriz, 
                          columns=['X', 'Y'],
                          index=['X', 'Y'])
    
    def graficar_correlacion(self):
        """Visualiza la correlación"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Diagrama de dispersión
        ax1 = axes[0]
        ax1.scatter(self.x, self.y, alpha=0.6, s=50, color='steelblue')
        ax1.set_xlabel('X', fontsize=12)
        ax1.set_ylabel('Y', fontsize=12)
        ax1.set_title('Diagrama de Dispersión', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Agregar coeficiente de correlación
        corr = self.coeficiente_correlacion_pearson()
        ax1.text(0.05, 0.95, f"r = {corr['r']:.4f}\n{corr['interpretacion']}", 
                transform=ax1.transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
        
        # Matriz de correlación (heatmap)
        ax2 = axes[1]
        matriz = self.matriz_correlacion()
        sns.heatmap(matriz, annot=True, cmap='coolwarm', center=0,
                   vmin=-1, vmax=1, ax=ax2, square=True, 
                   cbar_kws={'label': 'Correlación'})
        ax2.set_title('Matriz de Correlación', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        return fig


class RegresionLinealSimple:
    """Clase para regresión lineal simple: y = a + bx"""
    
    def __init__(self, x, y):
        self.x = np.array(x).reshape(-1, 1)
        self.y = np.array(y)
        self.n = len(self.x)
        
        # Ajustar el modelo
        self.modelo = LinearRegression()
        self.modelo.fit(self.x, self.y)
        
        # Parámetros
        self.a = self.modelo.intercept_
        self.b = self.modelo.coef_[0]
        
        # Predicciones
        self.y_pred = self.modelo.predict(self.x)
        
        # Métricas
        self._calcular_metricas()
    
    def _calcular_metricas(self):
        """Calcula R², error estándar, etc."""
        self.r2 = r2_score(self.y, self.y_pred)
        self.r = np.sqrt(self.r2) if self.b > 0 else -np.sqrt(self.r2)
        
        # Error estándar de la estimación
        self.residuos = self.y - self.y_pred
        self.mse = mean_squared_error(self.y, self.y_pred)
        self.rmse = np.sqrt(self.mse)
        
        # Suma de cuadrados
        y_media = np.mean(self.y)
        self.sct = np.sum((self.y - y_media) ** 2)  # Total
        self.scr = np.sum((self.y_pred - y_media) ** 2)  # Regresión
        self.sce = np.sum(self.residuos ** 2)  # Error
    
    def ecuacion(self):
        """Retorna la ecuación de regresión"""
        signo = '+' if self.b >= 0 else ''
        return {
            'ecuacion': f'y = {self.a:.4f} {signo}{self.b:.4f}x',
            'a_intercepto': round(self.a, 4),
            'b_pendiente': round(self.b, 4),
            'interpretacion_a': f'Cuando x=0, y={self.a:.4f}',
            'interpretacion_b': f'Por cada unidad que aumenta x, y {"aumenta" if self.b > 0 else "disminuye"} en {abs(self.b):.4f}'
        }
    
    def predecir(self, x_nuevo):
        """Predice y para un nuevo valor de x"""
        x_nuevo = np.array(x_nuevo).reshape(-1, 1)
        y_pred = self.modelo.predict(x_nuevo)
        
        return {
            'x': x_nuevo.flatten().tolist(),
            'y_predicho': y_pred.tolist(),
            'ecuacion_usada': f'y = {self.a:.4f} + {self.b:.4f}x'
        }
    
    def resumen_estadistico(self):
        """Genera resumen completo del modelo"""
        return {
            'ecuacion': self.ecuacion()['ecuacion'],
            'r_correlacion': round(self.r, 4),
            'r2_determinacion': round(self.r2, 4),
            'r2_porcentaje': f'{round(self.r2 * 100, 2)}%',
            'rmse': round(self.rmse, 4),
            'interpretacion_r2': f'El modelo explica el {round(self.r2 * 100, 2)}% de la variabilidad de Y',
            'suma_cuadrados': {
                'total': round(self.sct, 4),
                'regresion': round(self.scr, 4),
                'error': round(self.sce, 4)
            }
        }
    
    def graficar(self):
        """Genera gráficos del análisis de regresión"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Línea de regresión
        ax1 = axes[0, 0]
        ax1.scatter(self.x, self.y, alpha=0.6, s=50, color='steelblue', label='Datos reales')
        ax1.plot(self.x, self.y_pred, 'r-', linewidth=2, label='Línea de regresión')
        ax1.set_xlabel('X', fontsize=11)
        ax1.set_ylabel('Y', fontsize=11)
        ax1.set_title(f'Regresión Lineal\n{self.ecuacion()["ecuacion"]}', 
                     fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Agregar R²
        ax1.text(0.05, 0.95, f"R² = {self.r2:.4f}\nr = {self.r:.4f}", 
                transform=ax1.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='lightgreen', alpha=0.7))
        
        # 2. Residuos vs Valores ajustados
        ax2 = axes[0, 1]
        ax2.scatter(self.y_pred, self.residuos, alpha=0.6, s=50, color='purple')
        ax2.axhline(y=0, color='red', linestyle='--', linewidth=2)
        ax2.set_xlabel('Valores Ajustados (ŷ)', fontsize=11)
        ax2.set_ylabel('Residuos (y - ŷ)', fontsize=11)
        ax2.set_title('Gráfico de Residuos', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. Q-Q plot de residuos
        ax3 = axes[1, 0]
        stats.probplot(self.residuos, dist="norm", plot=ax3)
        ax3.set_title('Q-Q Plot de Residuos\n(Normalidad)', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # 4. Histograma de residuos
        ax4 = axes[1, 1]
        ax4.hist(self.residuos, bins=15, alpha=0.7, color='orange', edgecolor='black')
        ax4.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax4.set_xlabel('Residuos', fontsize=11)
        ax4.set_ylabel('Frecuencia', fontsize=11)
        ax4.set_title('Distribución de Residuos', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


class RegresionNoLineal:
    """Clase para regresiones exponencial y logarítmica"""
    
    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)
        
        if len(self.x) != len(self.y):
            raise ValueError("x e y deben tener la misma longitud")
    
    def regresion_exponencial(self):
        """
        Ajusta modelo exponencial: y = a × e^(bx)
        Mediante transformación logarítmica: ln(y) = ln(a) + bx
        """
        # Verificar que y > 0
        if np.any(self.y <= 0):
            return {
                'error': 'La regresión exponencial requiere que todos los valores de y sean positivos'
            }
        
        # Transformar y aplicar regresión lineal
        ln_y = np.log(self.y)
        x_reshape = self.x.reshape(-1, 1)
        
        modelo = LinearRegression()
        modelo.fit(x_reshape, ln_y)
        
        b = modelo.coef_[0]
        ln_a = modelo.intercept_
        a = np.exp(ln_a)
        
        # Predicciones
        y_pred = a * np.exp(b * self.x)
        
        # R²
        r2 = r2_score(self.y, y_pred)
        
        return {
            'tipo': 'Exponencial',
            'ecuacion': f'y = {a:.4f} × e^({b:.4f}x)',
            'a': round(a, 4),
            'b': round(b, 4),
            'r2': round(r2, 4),
            'r2_porcentaje': f'{round(r2 * 100, 2)}%',
            'y_predicho': y_pred,
            'interpretacion': f'Crecimiento {"exponencial" if b > 0 else "decrecimiento exponencial"}'
        }
    
    def regresion_logaritmica(self):
        """
        Ajusta modelo logarítmico: y = a + b × ln(x)
        """
        # Verificar que x > 0
        if np.any(self.x <= 0):
            return {
                'error': 'La regresión logarítmica requiere que todos los valores de x sean positivos'
            }
        
        # Transformar x y aplicar regresión lineal
        ln_x = np.log(self.x).reshape(-1, 1)
        
        modelo = LinearRegression()
        modelo.fit(ln_x, self.y)
        
        a = modelo.intercept_
        b = modelo.coef_[0]
        
        # Predicciones
        y_pred = a + b * np.log(self.x)
        
        # R²
        r2 = r2_score(self.y, y_pred)
        
        return {
            'tipo': 'Logarítmica',
            'ecuacion': f'y = {a:.4f} + {b:.4f} × ln(x)',
            'a': round(a, 4),
            'b': round(b, 4),
            'r2': round(r2, 4),
            'r2_porcentaje': f'{round(r2 * 100, 2)}%',
            'y_predicho': y_pred,
            'interpretacion': 'Crecimiento logarítmico (se desacelera)'
        }
    
    def regresion_potencial(self):
        """
        Ajusta modelo potencial: y = a × x^b
        Mediante transformación logarítmica: ln(y) = ln(a) + b×ln(x)
        """
        # Verificar que x > 0 e y > 0
        if np.any(self.x <= 0) or np.any(self.y <= 0):
            return {
                'error': 'La regresión potencial requiere que x e y sean positivos'
            }
        
        # Transformar
        ln_x = np.log(self.x).reshape(-1, 1)
        ln_y = np.log(self.y)
        
        modelo = LinearRegression()
        modelo.fit(ln_x, ln_y)
        
        b = modelo.coef_[0]
        ln_a = modelo.intercept_
        a = np.exp(ln_a)
        
        # Predicciones
        y_pred = a * (self.x ** b)
        
        # R²
        r2 = r2_score(self.y, y_pred)
        
        return {
            'tipo': 'Potencial',
            'ecuacion': f'y = {a:.4f} × x^{b:.4f}',
            'a': round(a, 4),
            'b': round(b, 4),
            'r2': round(r2, 4),
            'r2_porcentaje': f'{round(r2 * 100, 2)}%',
            'y_predicho': y_pred,
            'interpretacion': 'Relación de tipo potencia'
        }
    
    def comparar_modelos(self):
        """Compara los cuatro modelos y recomienda el mejor"""
        lineal = RegresionLinealSimple(self.x, self.y)
        exponencial = self.regresion_exponencial()
        logaritmica = self.regresion_logaritmica()
        potencial = self.regresion_potencial()
        
        modelos = {
            'Lineal': {'r2': lineal.r2, 'ecuacion': lineal.ecuacion()['ecuacion']},
            'Exponencial': {'r2': exponencial.get('r2', 0), 'ecuacion': exponencial.get('ecuacion', 'N/A')},
            'Logarítmica': {'r2': logaritmica.get('r2', 0), 'ecuacion': logaritmica.get('ecuacion', 'N/A')},
            'Potencial': {'r2': potencial.get('r2', 0), 'ecuacion': potencial.get('ecuacion', 'N/A')}
        }
        
        # Encontrar el mejor modelo
        mejor_modelo = max(modelos.items(), key=lambda x: x[1]['r2'])
        
        return {
            'modelos': modelos,
            'mejor_modelo': mejor_modelo[0],
            'mejor_r2': mejor_modelo[1]['r2'],
            'mejor_ecuacion': mejor_modelo[1]['ecuacion'],
            'recomendacion': f"El modelo {mejor_modelo[0]} tiene el mejor ajuste con R²={mejor_modelo[1]['r2']:.4f}"
        }
        
        # Encontrar el mejor
        mejor = max(modelos.items(), key=lambda x: x[1]['r2'])
        
        return {
            'modelos': modelos,
            'mejor_modelo': mejor[0],
            'mejor_r2': round(mejor[1]['r2'], 4),
            'mejor_ecuacion': mejor[1]['ecuacion'],
            'recomendacion': f'El modelo {mejor[0]} tiene el mejor ajuste (R² = {mejor[1]["r2"]:.4f})'
        }
    
    def graficar_comparacion(self):
        """Grafica todos los modelos para comparar (Lineal, Exponencial, Logarítmica, Potencial)"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        
        # Calcular modelos
        lineal = RegresionLinealSimple(self.x, self.y)
        exponencial = self.regresion_exponencial()
        logaritmica = self.regresion_logaritmica()
        potencial = self.regresion_potencial()
        
        # Ordenar x para graficar líneas suaves
        x_sorted = np.sort(self.x)
        
        # 1. Modelo Lineal
        ax1 = axes[0, 0]
        ax1.scatter(self.x, self.y, alpha=0.6, s=50, color='steelblue', label='Datos originales')
        x_line = x_sorted.reshape(-1, 1)
        y_line = lineal.modelo.predict(x_line)
        ax1.plot(x_sorted, y_line, 'r-', linewidth=2.5, label='Ajuste lineal')
        ax1.set_xlabel('X', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Y', fontsize=11, fontweight='bold')
        ax1.set_title(f'📊 Modelo Lineal\ny = a + bx\nR² = {lineal.r2:.4f}', fontweight='bold', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # 2. Modelo Exponencial
        ax2 = axes[0, 1]
        ax2.scatter(self.x, self.y, alpha=0.6, s=50, color='steelblue', label='Datos originales')
        if 'error' not in exponencial:
            idx_sorted = np.argsort(self.x)
            ax2.plot(self.x[idx_sorted], exponencial['y_predicho'][idx_sorted], 
                    'g-', linewidth=2.5, label='Ajuste exponencial')
            ax2.set_title(f'📈 Modelo Exponencial\ny = a × e^(bx)\nR² = {exponencial["r2"]:.4f}', 
                         fontweight='bold', fontsize=12)
        else:
            ax2.text(0.5, 0.5, '⚠️ ' + exponencial['error'], ha='center', va='center',
                    transform=ax2.transAxes, fontsize=9, color='red', wrap=True)
            ax2.set_title('📈 Modelo Exponencial\nNo disponible', fontweight='bold', fontsize=12)
        ax2.set_xlabel('X', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Y', fontsize=11, fontweight='bold')
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        # 3. Modelo Logarítmico
        ax3 = axes[0, 2]
        ax3.scatter(self.x, self.y, alpha=0.6, s=50, color='steelblue', label='Datos originales')
        if 'error' not in logaritmica:
            idx_sorted = np.argsort(self.x)
            ax3.plot(self.x[idx_sorted], logaritmica['y_predicho'][idx_sorted], 
                    color='purple', linewidth=2.5, label='Ajuste logarítmico')
            ax3.set_title(f'📉 Modelo Logarítmico\ny = a + b × ln(x)\nR² = {logaritmica["r2"]:.4f}', 
                         fontweight='bold', fontsize=12)
        else:
            ax3.text(0.5, 0.5, '⚠️ ' + logaritmica['error'], ha='center', va='center',
                    transform=ax3.transAxes, fontsize=9, color='red', wrap=True)
            ax3.set_title('📉 Modelo Logarítmico\nNo disponible', fontweight='bold', fontsize=12)
        ax3.set_xlabel('X', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Y', fontsize=11, fontweight='bold')
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)
        
        # 4. Modelo Potencial
        ax4 = axes[1, 0]
        ax4.scatter(self.x, self.y, alpha=0.6, s=50, color='steelblue', label='Datos originales')
        if 'error' not in potencial:
            idx_sorted = np.argsort(self.x)
            ax4.plot(self.x[idx_sorted], potencial['y_predicho'][idx_sorted], 
                    color='orange', linewidth=2.5, label='Ajuste potencial')
            ax4.set_title(f'⚡ Modelo Potencial\ny = a × x^b\nR² = {potencial["r2"]:.4f}', 
                         fontweight='bold', fontsize=12)
        else:
            ax4.text(0.5, 0.5, '⚠️ ' + potencial['error'], ha='center', va='center',
                    transform=ax4.transAxes, fontsize=9, color='red', wrap=True)
            ax4.set_title('⚡ Modelo Potencial\nNo disponible', fontweight='bold', fontsize=12)
        ax4.set_xlabel('X', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Y', fontsize=11, fontweight='bold')
        ax4.legend(loc='best')
        ax4.grid(True, alpha=0.3)
        
        # 5. Comparación de R² (gráfico de barras)
        ax5 = axes[1, 1]
        comparacion = self.comparar_modelos()
        modelos_nombres = list(comparacion['modelos'].keys())
        r2_valores = [comparacion['modelos'][m]['r2'] for m in modelos_nombres]
        
        colores = ['#E53935' if m == comparacion['mejor_modelo'] else '#64B5F6' 
                  for m in modelos_nombres]
        bars = ax5.bar(modelos_nombres, r2_valores, color=colores, alpha=0.8, 
                      edgecolor='black', linewidth=2)
        ax5.set_ylabel('R² (Coeficiente de Determinación)', fontsize=11, fontweight='bold')
        ax5.set_title('🏆 Comparación de Modelos\n(Mejor modelo en rojo)', fontweight='bold', fontsize=12)
        ax5.set_ylim(0, 1.1)
        ax5.grid(True, alpha=0.3, axis='y')
        ax5.axhline(y=0.7, color='green', linestyle='--', linewidth=1.5, alpha=0.5, label='R²=0.7 (buen ajuste)')
        ax5.legend(loc='upper right')
        
        # Agregar valores sobre las barras
        for bar, val, nombre in zip(bars, r2_valores, modelos_nombres):
            height = bar.get_height()
            emoji = '👑' if nombre == comparacion['mejor_modelo'] else '📊'
            ax5.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                    f'{emoji}\n{val:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # 6. Resumen de ecuaciones
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        resumen_texto = "📋 RESUMEN DE MODELOS\n" + "="*40 + "\n\n"
        
        for nombre, datos in comparacion['modelos'].items():
            emoji = '🏆' if nombre == comparacion['mejor_modelo'] else '📊'
            resumen_texto += f"{emoji} {nombre}:\n"
            resumen_texto += f"   Ecuación: {datos['ecuacion']}\n"
            resumen_texto += f"   R² = {datos['r2']:.4f} ({datos['r2']*100:.2f}%)\n\n"
        
        resumen_texto += "="*40 + "\n"
        resumen_texto += f"🏆 MEJOR: {comparacion['mejor_modelo']}\n"
        resumen_texto += f"📊 R² = {comparacion['mejor_r2']:.4f}\n\n"
        resumen_texto += f"💡 {comparacion['recomendacion']}"
        
        ax6.text(0.05, 0.95, resumen_texto, transform=ax6.transAxes,
                fontsize=9, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        fig.suptitle('📊 ANÁLISIS COMPLETO DE REGRESIÓN - Comparación de Modelos', 
                    fontsize=14, fontweight='bold', y=1.00)
        plt.subplots_adjust(top=0.96)
        
        return fig


class RegresionLinealMultiple:
    """Regresión lineal múltiple: y = b0 + b1×x1 + b2×x2 + ... + bn×xn"""
    
    def __init__(self, X, y):
        """
        X: matriz de variables independientes (n_muestras, n_variables)
        y: variable dependiente
        """
        self.X = np.array(X)
        self.y = np.array(y)
        
        if len(self.X.shape) == 1:
            self.X = self.X.reshape(-1, 1)
        
        self.n_muestras, self.n_variables = self.X.shape
        
        # Ajustar modelo
        self.modelo = LinearRegression()
        self.modelo.fit(self.X, self.y)
        
        # Coeficientes
        self.coeficientes = self.modelo.coef_
        self.intercepto = self.modelo.intercept_
        
        # Predicciones
        self.y_pred = self.modelo.predict(self.X)
        
        # Métricas
        self._calcular_metricas()
    
    def _calcular_metricas(self):
        """Calcula métricas del modelo"""
        self.r2 = r2_score(self.y, self.y_pred)
        self.r2_ajustado = 1 - (1 - self.r2) * (self.n_muestras - 1) / (self.n_muestras - self.n_variables - 1)
        self.rmse = np.sqrt(mean_squared_error(self.y, self.y_pred))
        self.residuos = self.y - self.y_pred
    
    def ecuacion(self, nombres_variables=None):
        """Genera la ecuación de regresión"""
        if nombres_variables is None:
            nombres_variables = [f'X{i+1}' for i in range(self.n_variables)]
        
        ecuacion = f'Y = {self.intercepto:.4f}'
        for i, (coef, nombre) in enumerate(zip(self.coeficientes, nombres_variables)):
            signo = '+' if coef >= 0 else ''
            ecuacion += f' {signo}{coef:.4f}×{nombre}'
        
        return {
            'ecuacion': ecuacion,
            'intercepto': round(self.intercepto, 4),
            'coeficientes': {nombre: round(coef, 4) 
                           for nombre, coef in zip(nombres_variables, self.coeficientes)}
        }
    
    def resumen(self):
        """Resumen estadístico del modelo"""
        return {
            'r2': round(self.r2, 4),
            'r2_ajustado': round(self.r2_ajustado, 4),
            'rmse': round(self.rmse, 4),
            'n_variables': self.n_variables,
            'n_muestras': self.n_muestras,
            'interpretacion': f'El modelo explica el {round(self.r2 * 100, 2)}% de la variabilidad'
        }
    
    def predecir(self, X_nuevo):
        """Predice valores para nuevos datos"""
        X_nuevo = np.array(X_nuevo)
        if len(X_nuevo.shape) == 1:
            X_nuevo = X_nuevo.reshape(1, -1)
        
        y_pred = self.modelo.predict(X_nuevo)
        return y_pred


# Ejemplos de uso
if __name__ == "__main__":
    print("=" * 70)
    print("EJEMPLOS DE REGRESIÓN Y CORRELACIÓN")
    print("=" * 70)
    
    # Datos de ejemplo
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([2.3, 4.1, 5.8, 7.9, 10.2, 11.8, 14.1, 16.3, 18.0, 20.1])
    
    # 1. Correlación
    print("\n📊 ANÁLISIS DE CORRELACIÓN")
    print("-" * 70)
    corr = CorrelacionLineal(x, y)
    resultado_corr = corr.coeficiente_correlacion_pearson()
    print(f"r = {resultado_corr['r']}")
    print(f"Interpretación: {resultado_corr['interpretacion']}")
    
    # 2. Regresión lineal simple
    print("\n📈 REGRESIÓN LINEAL SIMPLE")
    print("-" * 70)
    reg_simple = RegresionLinealSimple(x, y)
    print(f"Ecuación: {reg_simple.ecuacion()['ecuacion']}")
    print(f"R² = {reg_simple.r2:.4f}")
    
    # 3. Modelos no lineales
    print("\n📉 MODELOS NO LINEALES")
    print("-" * 70)
    reg_nolineal = RegresionNoLineal(x, y)
    comparacion = reg_nolineal.comparar_modelos()
    print(f"Mejor modelo: {comparacion['mejor_modelo']}")
    print(f"Ecuación: {comparacion['mejor_ecuacion']}")
    
    # Generar gráficos
    print("\n\nGenerando gráficos...")
    fig1 = corr.graficar_correlacion()
    fig2 = reg_simple.graficar()
    fig3 = reg_nolineal.graficar_comparacion()
    plt.show()