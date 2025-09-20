import pandas as pd
import numpy as np
from fractions import Fraction
from itertools import combinations, product

class ProbabilidadesElementales:
    """Clase para cálculos de probabilidades elementales"""
    
    def __init__(self):
        self.eventos = {}
        self.espacio_muestral = set()
    
    def definir_espacio_muestral(self, elementos):
        """
        Define el espacio muestral
        elementos: lista de elementos del espacio muestral
        """
        self.espacio_muestral = set(elementos)
        return self.espacio_muestral
    
    def definir_evento(self, nombre, elementos):
        """
        Define un evento
        nombre: nombre del evento (str)
        elementos: lista de elementos que forman el evento
        """
        evento_set = set(elementos)
        if not evento_set.issubset(self.espacio_muestral):
            raise ValueError("El evento debe ser subconjunto del espacio muestral")
        
        self.eventos[nombre] = evento_set
        return evento_set
    
    def probabilidad_simple(self, evento_nombre):
        """
        Calcula la probabilidad de un evento simple
        P(A) = |A| / |Ω|
        """
        if evento_nombre not in self.eventos:
            raise ValueError(f"Evento '{evento_nombre}' no definido")
        
        evento = self.eventos[evento_nombre]
        if len(self.espacio_muestral) == 0:
            return 0
        
        prob = len(evento) / len(self.espacio_muestral)
        prob_fraccion = Fraction(len(evento), len(self.espacio_muestral))
        
        return {
            'probabilidad': round(prob, 4),
            'fraccion': str(prob_fraccion),
            'porcentaje': round(prob * 100, 2),
            'elementos_evento': list(evento),
            'cardinalidad_evento': len(evento),
            'cardinalidad_espacio': len(self.espacio_muestral)
        }
    
    def union_eventos(self, evento1, evento2):
        """
        Calcula la unión de dos eventos
        A ∪ B
        """
        if evento1 not in self.eventos or evento2 not in self.eventos:
            raise ValueError("Ambos eventos deben estar definidos")
        
        union = self.eventos[evento1].union(self.eventos[evento2])
        return union
    
    def interseccion_eventos(self, evento1, evento2):
        """
        Calcula la intersección de dos eventos
        A ∩ B
        """
        if evento1 not in self.eventos or evento2 not in self.eventos:
            raise ValueError("Ambos eventos deben estar definidos")
        
        interseccion = self.eventos[evento1].intersection(self.eventos[evento2])
        return interseccion
    
    def eventos_excluyentes(self, evento1, evento2):
        """
        Verifica si dos eventos son mutuamente excluyentes
        P(A ∩ B) = 0
        """
        interseccion = self.interseccion_eventos(evento1, evento2)
        return len(interseccion) == 0
    
    def probabilidad_union_excluyentes(self, evento1, evento2):
        """
        Probabilidad de la unión de eventos mutuamente excluyentes
        P(A ∪ B) = P(A) + P(B) cuando A y B son excluyentes
        """
        if not self.eventos_excluyentes(evento1, evento2):
            raise ValueError("Los eventos no son mutuamente excluyentes")
        
        prob_a = self.probabilidad_simple(evento1)['probabilidad']
        prob_b = self.probabilidad_simple(evento2)['probabilidad']
        prob_union = prob_a + prob_b
        
        return {
            'probabilidad_union': round(prob_union, 4),
            'probabilidad_a': prob_a,
            'probabilidad_b': prob_b,
            'son_excluyentes': True,
            'formula': 'P(A ∪ B) = P(A) + P(B)'
        }
    
    def probabilidad_union_no_excluyentes(self, evento1, evento2):
        """
        Probabilidad de la unión de eventos no excluyentes
        P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
        """
        prob_a = self.probabilidad_simple(evento1)['probabilidad']
        prob_b = self.probabilidad_simple(evento2)['probabilidad']
        
        interseccion = self.interseccion_eventos(evento1, evento2)
        prob_interseccion = len(interseccion) / len(self.espacio_muestral)
        
        prob_union = prob_a + prob_b - prob_interseccion
        
        return {
            'probabilidad_union': round(prob_union, 4),
            'probabilidad_a': prob_a,
            'probabilidad_b': prob_b,
            'probabilidad_interseccion': round(prob_interseccion, 4),
            'son_excluyentes': False,
            'formula': 'P(A ∪ B) = P(A) + P(B) - P(A ∩ B)',
            'elementos_interseccion': list(interseccion)
        }
    
    def probabilidad_complemento(self, evento_nombre):
        """
        Calcula la probabilidad del complemento de un evento
        P(A') = 1 - P(A)
        """
        prob_evento = self.probabilidad_simple(evento_nombre)['probabilidad']
        prob_complemento = 1 - prob_evento
        
        # Elementos del complemento
        evento = self.eventos[evento_nombre]
        complemento = self.espacio_muestral - evento
        
        return {
            'probabilidad_complemento': round(prob_complemento, 4),
            'probabilidad_evento': prob_evento,
            'elementos_complemento': list(complemento),
            'cardinalidad_complemento': len(complemento),
            'formula': "P(A') = 1 - P(A)"
        }
    
    def probabilidad_condicional(self, evento_a, evento_b):
        """
        Calcula la probabilidad condicional P(A|B)
        P(A|B) = P(A ∩ B) / P(B)
        """
        if evento_a not in self.eventos or evento_b not in self.eventos:
            raise ValueError("Ambos eventos deben estar definidos")
        
        prob_b = self.probabilidad_simple(evento_b)['probabilidad']
        if prob_b == 0:
            raise ValueError("No se puede calcular probabilidad condicional: P(B) = 0")
        
        interseccion = self.interseccion_eventos(evento_a, evento_b)
        prob_interseccion = len(interseccion) / len(self.espacio_muestral)
        
        prob_condicional = prob_interseccion / prob_b
        
        return {
            'probabilidad_condicional': round(prob_condicional, 4),
            'probabilidad_interseccion': round(prob_interseccion, 4),
            'probabilidad_b': prob_b,
            'elementos_interseccion': list(interseccion),
            'formula': 'P(A|B) = P(A ∩ B) / P(B)'
        }
    
    def eventos_independientes(self, evento_a, evento_b):
        """
        Verifica si dos eventos son independientes
        A y B son independientes si P(A ∩ B) = P(A) × P(B)
        """
        prob_a = self.probabilidad_simple(evento_a)['probabilidad']
        prob_b = self.probabilidad_simple(evento_b)['probabilidad']
        
        interseccion = self.interseccion_eventos(evento_a, evento_b)
        prob_interseccion = len(interseccion) / len(self.espacio_muestral)
        
        producto_independiente = prob_a * prob_b
        
        # Tolerancia para errores de redondeo
        tolerancia = 1e-10
        son_independientes = abs(prob_interseccion - producto_independiente) < tolerancia
        
        return {
            'son_independientes': son_independientes,
            'probabilidad_a': prob_a,
            'probabilidad_b': prob_b,
            'probabilidad_interseccion': round(prob_interseccion, 4),
            'producto_independiente': round(producto_independiente, 4),
            'diferencia': abs(prob_interseccion - producto_independiente),
            'formula': 'P(A ∩ B) = P(A) × P(B) si son independientes'
        }
    
    def probabilidad_eventos_independientes(self, evento_a, evento_b):
        """
        Calcula probabilidades asumiendo independencia
        """
        if not self.eventos_independientes(evento_a, evento_b)['son_independientes']:
            print(f"Advertencia: Los eventos {evento_a} y {evento_b} no parecen ser independientes")
        
        prob_a = self.probabilidad_simple(evento_a)['probabilidad']
        prob_b = self.probabilidad_simple(evento_b)['probabilidad']
        
        prob_interseccion = prob_a * prob_b
        prob_union = prob_a + prob_b - prob_interseccion
        
        return {
            'probabilidad_a': prob_a,
            'probabilidad_b': prob_b,
            'probabilidad_interseccion': round(prob_interseccion, 4),
            'probabilidad_union': round(prob_union, 4),
            'formulas': {
                'interseccion': 'P(A ∩ B) = P(A) × P(B)',
                'union': 'P(A ∪ B) = P(A) + P(B) - P(A) × P(B)'
            }
        }
    
    def resumen_eventos(self):
        """
        Genera un resumen de todos los eventos definidos
        """
        resumen = {
            'espacio_muestral': {
                'elementos': list(self.espacio_muestral),
                'cardinalidad': len(self.espacio_muestral)
            },
            'eventos': {}
        }
        
        for nombre, evento in self.eventos.items():
            prob = self.probabilidad_simple(nombre)
            resumen['eventos'][nombre] = {
                'elementos': list(evento),
                'cardinalidad': len(evento),
                'probabilidad': prob['probabilidad'],
                'fraccion': prob['fraccion'],
                'porcentaje': prob['porcentaje']
            }
        
        return resumen

def ejemplo_uso():
    """Ejemplo de uso de la clase ProbabilidadesElementales"""
    
    # Crear instancia
    prob = ProbabilidadesElementales()
    
    # Ejemplo: Lanzamiento de dos dados
    espacio = []
    for i in range(1, 7):
        for j in range(1, 7):
            espacio.append((i, j))
    
    prob.definir_espacio_muestral(espacio)
    
    # Definir eventos
    suma_7 = [(i, j) for i, j in espacio if i + j == 7]
    suma_par = [(i, j) for i, j in espacio if (i + j) % 2 == 0]
    primer_dado_6 = [(6, j) for j in range(1, 7)]
    
    prob.definir_evento("Suma_7", suma_7)
    prob.definir_evento("Suma_Par", suma_par)
    prob.definir_evento("Primer_6", primer_dado_6)
    
    # Calcular probabilidades
    print("=== EJEMPLO: Lanzamiento de dos dados ===")
    print("\nProbabilidad simple:")
    print(prob.probabilidad_simple("Suma_7"))
    
    print("\nEventos excluyentes:")
    print(f"¿Suma_7 y Primer_6 son excluyentes? {prob.eventos_excluyentes('Suma_7', 'Primer_6')}")
    
    print("\nEventos independientes:")
    print(prob.eventos_independientes("Suma_7", "Primer_6"))
    
    print("\nResumen completo:")
    print(prob.resumen_eventos())

if __name__ == "__main__":
    ejemplo_uso()