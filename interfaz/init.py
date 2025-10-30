"""
Módulo de Interfaz Gráfica
Contiene todos los componentes de la GUI de StatPro
"""

from .interfaz_grafica import App, main
from .pantalla_login import PantallaLogin
from .menu_principal import MenuPrincipal

__all__ = [
    'App',
    'main',
    'PantallaLogin',
    'MenuPrincipal'
]

__version__ = '1.0'
__author__ = 'Ana Paula Vásquez, María Mendez, Ariana Morales'