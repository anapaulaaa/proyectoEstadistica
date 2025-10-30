import pandas as pd
import numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt
import seaborn as sns

class TeoremaBayes:
    """Clase para aplicar el Teorema de Bayes"""
    
    def __init__(self):
        self.hipotesis = {}
        self.evidencia = {}
        self.probabilidades_conjuntas = {}
        self.resultados_bayes = {}
    
    def definir_hipotesis(self, hipotesis_dict):
        """
        Define las hipótesis a priori
        hipotesis_dict: {nombre_hipotesis: probabilidad_a_priori}
        """
        # Verificar que las probabilidades sumen 1
        suma = sum(hipotesis_dict.values())
        if abs(suma - 1.0) > 1e-10:
            raise ValueError(f"Las probabilidades a priori deben sumar 1. Suma actual: {suma}")
        
        self.hipotesis = hipotesis_dict.copy()
        return self.hipotesis
    
    def definir_verosimilitudes(self, verosimilitudes_dict):
        """
        Define las verosimilitudes P(E|H)
        verosimilitudes_dict: {nombre_hipotesis: {evidencia: probabilidad}}
        """
        # Verificar que todas las hipótesis estén definidas
        for hipotesis in verosimilitudes_dict:
            if hipotesis not in self.hipotesis:
                raise ValueError(f"La hipótesis '{hipotesis}' no está definida")
        
        self.verosimilitudes = verosimilitudes_dict.copy()
        return self.verosimilitudes
    
    def calcular_probabilidad_evidencia(self, evidencia):
        """
        Calcula P(E) usando la ley de probabilidad total
        P(E) = Σ P(E|Hi) * P(Hi)
        """
        prob_evidencia = 0
        detalles = []
        
        for hipotesis, prob_hipotesis in self.hipotesis.items():
            if hipotesis in self.verosimilitudes and evidencia in self.verosimilitudes[hipotesis]:
                verosimilitud = self.verosimilitudes[hipotesis][evidencia]
                contribucion = verosimilitud * prob_hipotesis
                prob_evidencia += contribucion
                
                detalles.append({
                    'hipotesis': hipotesis,
                    'P(H)': prob_hipotesis,
                    'P(E|H)': verosimilitud,
                    'P(E|H) * P(H)': contribucion
                })
        
        return {
            'probabilidad_evidencia': prob_evidencia,
            'detalles_calculo': detalles,
            'formula': 'P(E) = Σ P(E|Hi) * P(Hi)'
        }
    
    def calcular_bayes(self, evidencia):
        """
        Aplica el Teorema de Bayes para calcular probabilidades a posteriori
        P(Hi|E) = P(E|Hi) * P(Hi) / P(E)
        """
        # Calcular P(E)
        info_evidencia = self.calcular_probabilidad_evidencia(evidencia)
        prob_evidencia = info_evidencia['probabilidad_evidencia']
        
        if prob_evidencia == 0:
            raise ValueError(f"La probabilidad de la evidencia '{evidencia}' es 0")
        
        resultados = []
        
        for hipotesis, prob_priori in self.hipotesis.items():
            if hipotesis in self.verosimilitudes and evidencia in self.verosimilitudes[hipotesis]:
                verosimilitud = self.verosimilitudes[hipotesis][evidencia]
                
                # Calcular probabilidad a posteriori
                numerador = verosimilitud * prob_priori
                prob_posteriori = numerador / prob_evidencia
                
                resultado = {
                    'hipotesis': hipotesis,
                    'prob_priori': prob_priori,
                    'verosimilitud': verosimilitud,
                    'numerador': numerador,
                    'prob_posteriori': prob_posteriori,
                    'prob_posteriori_porcentaje': round(prob_posteriori * 100, 2),
                    'fraccion_priori': str(Fraction(prob_priori).limit_denominator()),
                    'fraccion_posteriori': str(Fraction(prob_posteriori).limit_denominator(1000))
                }
                resultados.append(resultado)
        
        self.resultados_bayes[evidencia] = {
            'evidencia': evidencia,
            'prob_evidencia': prob_evidencia,
            'resultados_hipotesis': resultados,
            'info_evidencia': info_evidencia
        }
        
        return self.resultados_bayes[evidencia]
    
    def comparar_probabilidades(self, evidencia):
        """
        Compara probabilidades a priori vs a posteriori
        """
        if evidencia not in self.resultados_bayes:
            self.calcular_bayes(evidencia)
        
        resultado = self.resultados_bayes[evidencia]
        comparacion = []
        
        for res in resultado['resultados_hipotesis']:
            hipotesis = res['hipotesis']
            cambio = res['prob_posteriori'] - res['prob_priori']
            cambio_porcentual = (cambio / res['prob_priori']) * 100 if res['prob_priori'] > 0 else 0
            
            comparacion.append({
                'hipotesis': hipotesis,
                'prob_priori': res['prob_priori'],
                'prob_posteriori': res['prob_posteriori'],
                'cambio_absoluto': cambio,
                'cambio_porcentual': cambio_porcentual,
                'interpretacion': self._interpretar_cambio(cambio_porcentual)
            })
        
        return comparacion
    
    def _interpretar_cambio(self, cambio_porcentual):
        """Interpreta el cambio porcentual"""
        if cambio_porcentual > 50:
            return "Aumento muy significativo"
        elif cambio_porcentual > 20:
            return "Aumento significativo"
        elif cambio_porcentual > 5:
            return "Aumento moderado"
        elif cambio_porcentual > -5:
            return "Sin cambio significativo"
        elif cambio_porcentual > -20:
            return "Disminución moderada"
        elif cambio_porcentual > -50:
            return "Disminución significativa"
        else:
            return "Disminución muy significativa"
    
    def generar_tabla_bayes(self, evidencia):
        """
        Genera una tabla detallada de los cálculos de Bayes
        """
        if evidencia not in self.resultados_bayes:
            self.calcular_bayes(evidencia)
        
        resultado = self.resultados_bayes[evidencia]
        
        datos_tabla = []
        for res in resultado['resultados_hipotesis']:
            datos_tabla.append({
                'Hipótesis': res['hipotesis'],
                'P(H) - A Priori': f"{res['prob_priori']:.4f}",
                'P(E|H) - Verosimilitud': f"{res['verosimilitud']:.4f}",
                'P(E|H) × P(H)': f"{res['numerador']:.6f}",
                'P(H|E) - A Posteriori': f"{res['prob_posteriori']:.4f}",
                'Porcentaje Final': f"{res['prob_posteriori_porcentaje']:.2f}%"
            })
        
        df = pd.DataFrame(datos_tabla)
        
        # Agregar fila de totales
        total_numeradores = sum(res['numerador'] for res in resultado['resultados_hipotesis'])
        total_posteriori = sum(res['prob_posteriori'] for res in resultado['resultados_hipotesis'])
        
        df.loc[len(df)] = {
            'Hipótesis': 'TOTAL',
            'P(H) - A Priori': '1.0000',
            'P(E|H) - Verosimilitud': '—',
            'P(E|H) × P(H)': f"{total_numeradores:.6f}",
            'P(H|E) - A Posteriori': f"{total_posteriori:.4f}",
            'Porcentaje Final': f"{total_posteriori*100:.2f}%"
        }
        
        return df
    
    def graficar_comparacion(self, evidencia, figsize=(12, 8)):
        """
        Genera gráficos de comparación antes/después de aplicar Bayes
        """
        if evidencia not in self.resultados_bayes:
            self.calcular_bayes(evidencia)
        
        resultado = self.resultados_bayes[evidencia]
        
        # Datos para gráfico
        hipotesis_nombres = [res['hipotesis'] for res in resultado['resultados_hipotesis']]
        prob_priori = [res['prob_priori'] for res in resultado['resultados_hipotesis']]
        prob_posteriori = [res['prob_posteriori'] for res in resultado['resultados_hipotesis']]
        
        # Crear subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        
        # Gráfico 1: Barras comparativas
        x = np.arange(len(hipotesis_nombres))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, prob_priori, width, label='A Priori', alpha=0.7, color='skyblue')
        bars2 = ax1.bar(x + width/2, prob_posteriori, width, label='A Posteriori', alpha=0.7, color='orange')
        
        ax1.set_xlabel('Hipótesis')
        ax1.set_ylabel('Probabilidad')
        ax1.set_title(f'Comparación A Priori vs A Posteriori\nEvidencia: {evidencia}')
        ax1.set_xticks(x)
        ax1.set_xticklabels(hipotesis_nombres)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Añadir valores sobre las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{height:.3f}', ha='center', va='bottom', fontsize=9)
        
        # Gráfico 2: Pie chart A Priori
        ax2.pie(prob_priori, labels=hipotesis_nombres, autopct='%1.1f%%', 
                startangle=90, colors=plt.cm.Set3.colors)
        ax2.set_title('Probabilidades A Priori')
        
        # Gráfico 3: Pie chart A Posteriori
        ax3.pie(prob_posteriori, labels=hipotesis_nombres, autopct='%1.1f%%', 
                startangle=90, colors=plt.cm.Set3.colors)
        ax3.set_title('Probabilidades A Posteriori')
        
        # Gráfico 4: Cambios porcentuales
        comparacion = self.comparar_probabilidades(evidencia)
        cambios = [comp['cambio_porcentual'] for comp in comparacion]
        colores = ['green' if c > 0 else 'red' if c < 0 else 'gray' for c in cambios]
        
        bars = ax4.bar(hipotesis_nombres, cambios, color=colores, alpha=0.7)
        ax4.set_xlabel('Hipótesis')
        ax4.set_ylabel('Cambio Porcentual (%)')
        ax4.set_title('Cambio Porcentual en Probabilidades')
        ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax4.grid(True, alpha=0.3)
        
        # Rotar etiquetas si son muy largas
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def resumen_completo(self, evidencia):
        """
        Genera un resumen completo del análisis de Bayes
        """
        if evidencia not in self.resultados_bayes:
            self.calcular_bayes(evidencia)
        
        resultado = self.resultados_bayes[evidencia]
        comparacion = self.comparar_probabilidades(evidencia)
        
        resumen = {
            'evidencia_observada': evidencia,
            'probabilidad_evidencia': resultado['prob_evidencia'],
            'hipotesis_mas_probable': max(resultado['resultados_hipotesis'], 
                                        key=lambda x: x['prob_posteriori']),
            'hipotesis_menos_probable': min(resultado['resultados_hipotesis'], 
                                         key=lambda x: x['prob_posteriori']),
            'mayor_cambio_positivo': max(comparacion, key=lambda x: x['cambio_porcentual']),
            'mayor_cambio_negativo': min(comparacion, key=lambda x: x['cambio_porcentual']),
            'tabla_completa': self.generar_tabla_bayes(evidencia),
            'comparaciones': comparacion
        }
        
        return resumen

def ejemplo_test_medico():
    """
    Ejemplo clásico: Test médico para detectar una enfermedad
    """
    print("=== EJEMPLO: TEST MÉDICO ===")
    print("Una enfermedad afecta al 1% de la población")
    print("Test tiene 95% de precisión para detectar la enfermedad")
    print("Test tiene 90% de especificidad (90% de negativos correctos)")
    print()
    
    bayes = TeoremaBAyes()
    
    # Definir hipótesis a priori
    hipotesis = {
        'Enfermo': 0.01,      # 1% de la población
        'Sano': 0.99          # 99% de la población
    }
    bayes.definir_hipotesis(hipotesis)
    
    # Definir verosimilitudes
    verosimilitudes = {
        'Enfermo': {
            'Positivo': 0.95,    # Sensibilidad del test
            'Negativo': 0.05     # Falsos negativos
        },
        'Sano': {
            'Positivo': 0.10,    # Falsos positivos
            'Negativo': 0.90     # Especificidad del test
        }
    }
    bayes.definir_verosimilitudes(verosimilitudes)
    
    # Calcular para test positivo
    print("--- RESULTADO POSITIVO ---")
    resultado_pos = bayes.calcular_bayes('Positivo')
    
    print(f"P(Evidencia = Positivo) = {resultado_pos['prob_evidencia']:.6f}")
    print()
    
    for res in resultado_pos['resultados_hipotesis']:
        print(f"P({res['hipotesis']}|Positivo) = {res['prob_posteriori']:.6f} ({res['prob_posteriori_porcentaje']:.2f}%)")
    
    print("\n--- INTERPRETACIÓN ---")
    print("Aunque el test sea positivo, solo hay ~8.7% de probabilidad de estar realmente enfermo!")
    print("Esto se debe a la baja prevalencia de la enfermedad.")
    
    # Mostrar tabla
    print("\n--- TABLA DETALLADA ---")
    tabla = bayes.generar_tabla_bayes('Positivo')
    print(tabla.to_string(index=False))
    
    # Comparar cambios
    print("\n--- CAMBIOS EN PROBABILIDADES ---")
    comparacion = bayes.comparar_probabilidades('Positivo')
    for comp in comparacion:
        print(f"{comp['hipotesis']}: {comp['prob_priori']:.4f} → {comp['prob_posteriori']:.4f} "
              f"(Cambio: {comp['cambio_porcentual']:.1f}% - {comp['interpretacion']})")
    
    return bayes

def ejemplo_spam():
    """
    Ejemplo: Clasificador de spam usando Bayes
    """
    print("\n\n=== EJEMPLO: FILTRO DE SPAM ===")
    print("Clasificar emails como spam o no spam basado en palabras clave")
    print()
    
    bayes = TeoremaBAyes()
    
    # Probabilidades a priori (basadas en datos históricos)
    hipotesis = {
        'Spam': 0.30,         # 30% de emails son spam
        'No_Spam': 0.70       # 70% de emails no son spam
    }
    bayes.definir_hipotesis(hipotesis)
    
    # Verosimilitudes para diferentes palabras
    verosimilitudes = {
        'Spam': {
            'gratis': 0.80,      # 80% de spams contienen "gratis"
            'oferta': 0.60,      # 60% de spams contienen "oferta"
            'trabajo': 0.20,     # 20% de spams contienen "trabajo"
            'reunion': 0.05      # 5% de spams contienen "reunión"
        },
        'No_Spam': {
            'gratis': 0.10,      # 10% de no-spams contienen "gratis"
            'oferta': 0.15,      # 15% de no-spams contienen "oferta"
            'trabajo': 0.40,     # 40% de no-spams contienen "trabajo"
            'reunion': 0.30      # 30% de no-spams contienen "reunión"
        }
    }
    bayes.definir_verosimilitudes(verosimilitudes)
    
    # Analizar diferentes palabras
    palabras_test = ['gratis', 'oferta', 'trabajo', 'reunion']
    
    for palabra in palabras_test:
        print(f"\n--- ANÁLISIS PARA: '{palabra.upper()}' ---")
        resultado = bayes.calcular_bayes(palabra)
        
        for res in resultado['resultados_hipotesis']:
            print(f"P({res['hipotesis']}|{palabra}) = {res['prob_posteriori']:.4f} ({res['prob_posteriori_porcentaje']:.1f}%)")
        
        # Determinar clasificación
        prob_spam = next(r['prob_posteriori'] for r in resultado['resultados_hipotesis'] if r['hipotesis'] == 'Spam')
        clasificacion = "SPAM" if prob_spam > 0.5 else "NO SPAM"
        confianza = max(prob_spam, 1-prob_spam) * 100
        
        print(f"→ Clasificación: {clasificacion} (Confianza: {confianza:.1f}%)")
    
    return bayes

if __name__ == "__main__":
    # Ejecutar ejemplos
    bayes_medico = ejemplo_test_medico()
    bayes_spam = ejemplo_spam()
    
    # Generar gráficos
    try:
        fig1 = bayes_medico.graficar_comparacion('Positivo')
        plt.show()
    except:
        print("Error al generar gráfico del ejemplo médico")
    
    try:
        fig2 = bayes_spam.graficar_comparacion('gratis')
        plt.show()
    except:
        print("Error al generar gráfico del ejemplo spam")