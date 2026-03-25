"""Submodulos de interfaz para temas de Estadistica II."""

from .modulo_estimacion import abrir_modulo_estimacion_tamano_muestra
from .modulo_estimacion import abrir_modulo_tamano_muestra
from .modulo_estimacion import abrir_modulo_estimacion_puntual
from .modulo_estimacion import abrir_modulo_intervalos_confianza
from .modulo_muestreo import abrir_modulo_muestreo

__all__ = [
    "abrir_modulo_estimacion_tamano_muestra",
    "abrir_modulo_tamano_muestra",
    "abrir_modulo_estimacion_puntual",
    "abrir_modulo_intervalos_confianza",
    "abrir_modulo_muestreo",
]
