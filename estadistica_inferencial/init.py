"""
Módulo de Estadística Inferencial
Contiene todas las funciones para probabilidades y distribuciones
"""

from .probabilidades import ProbabilidadesElementales

from .distribuciones import (
    DistribucionBernoulli,
    DistribucionBinomial
)

from .distribucion_normal import DistribucionNormal

from .distribucion_poisson import DistribucionPoisson

from .regresion_correlacion import (
    CorrelacionLineal,
    RegresionLinealSimple,
    RegresionNoLineal,
    RegresionLinealMultiple
)

from .bayes import TeoremaBayes

from .diagramas_arbol import DiagramaArbol

from .estimacion_tamano_muestra import EstimacionTamanoMuestra
from .anova import (
    anova_un_factor,
    anova_dos_factores_sin_replicacion,
    anova_dos_factores_con_replicacion,
)

__all__ = [
    # Probabilidades
    'ProbabilidadesElementales',
    
    # Distribuciones discretas
    'DistribucionBernoulli',
    'DistribucionBinomial',
    'DistribucionPoisson',
    
    # Distribuciones continuas
    'DistribucionNormal',
    
    # Regresión y correlación
    'CorrelacionLineal',
    'RegresionLinealSimple',
    'RegresionNoLineal',
    'RegresionLinealMultiple',
    
    # Teoremas
    'TeoremaBayes',
    
    # Visualizaciones
    'DiagramaArbol',

    # Estimacion y tamano de muestra
    'EstimacionTamanoMuestra',

    # ANOVA
    'anova_un_factor',
    'anova_dos_factores_sin_replicacion',
    'anova_dos_factores_con_replicacion'
]

__version__ = '1.0'
__author__ = 'Ana Paula Vásquez, María Mendez, Ariana Morales'