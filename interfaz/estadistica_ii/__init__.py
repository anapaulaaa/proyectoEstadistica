"""Submodulos de interfaz para temas de Estadistica II."""

from .modulo_estimacion import abrir_modulo_estimacion_tamano_muestra
from .modulo_estimacion import abrir_modulo_tamano_muestra
from .modulo_estimacion import abrir_modulo_estimacion_puntual
from .modulo_intervalos_confianza import abrir_modulo_intervalos_confianza
from .modulo_muestreo import abrir_modulo_muestreo
from .modulo_anova import abrir_modulo_anova_menu
from .modulo_anova import abrir_modulo_anova_1_factor
from .modulo_anova import abrir_modulo_anova_2_factores
from .modulo_anova import abrir_modulo_ejercicios_anova

__all__ = [
    "abrir_modulo_estimacion_tamano_muestra",
    "abrir_modulo_tamano_muestra",
    "abrir_modulo_estimacion_puntual",
    "abrir_modulo_intervalos_confianza",
    "abrir_modulo_muestreo",
    "abrir_modulo_anova_menu",
    "abrir_modulo_anova_1_factor",
    "abrir_modulo_anova_2_factores",
    "abrir_modulo_ejercicios_anova",
]
