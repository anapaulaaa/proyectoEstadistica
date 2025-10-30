"""
Módulo de Estadística Descriptiva
Contiene todas las funciones para análisis descriptivo de datos
"""

from .analisis_estadistico import (
    calcular_tendencia_central,
    generar_dfs,
    generar_dfsvai
)

from .medidas_dispersión import (
    calcular_rango,
    calcular_varianza,
    calcular_desviacion_estandar,
    calcular_coeficiente_variacion,
    analisis_completo_dispersion,
    generar_tabla_dispersion,
    graficar_dispersion
)

from .medidas_forma import (
    calcular_asimetria,
    calcular_curtosis,
    analisis_completo_forma,
    generar_tabla_forma,
    graficar_forma
)

from .medidas_posicion import (
    calcular_cuartiles,
    calcular_deciles,
    calcular_percentiles,
    analisis_completo_posicion,
    generar_tabla_posicion,
    crear_boxplot
)

from .graficas import (
    graficar_tendencia,
    graficar_frecuencia
)

__all__ = [
    # Análisis estadístico
    'calcular_tendencia_central',
    'generar_dfs',
    'generar_dfsvai',
    
    # Dispersión
    'calcular_rango',
    'calcular_varianza',
    'calcular_desviacion_estandar',
    'calcular_coeficiente_variacion',
    'analisis_completo_dispersion',
    'generar_tabla_dispersion',
    'graficar_dispersion',
    
    # Forma
    'calcular_asimetria',
    'calcular_curtosis',
    'analisis_completo_forma',
    'generar_tabla_forma',
    'graficar_forma',
    
    # Posición
    'calcular_cuartiles',
    'calcular_deciles',
    'calcular_percentiles',
    'analisis_completo_posicion',
    'generar_tabla_posicion',
    'crear_boxplot',
    
    # Gráficas
    'graficar_tendencia',
    'graficar_frecuencia'
]

__version__ = '1.0'
__author__ = 'Ana Paula Vásquez, María Mendez, Ariana Morales'