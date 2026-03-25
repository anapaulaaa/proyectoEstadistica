"""
Módulo de Interfaz Gráfica
Contiene todos los componentes de la GUI de StatPro
"""

from .interfaz_grafica import App, main
from .pantalla_login import PantallaLogin
from .menu_principal import MenuPrincipal
from .componentes_analisis import VentanaAnalisis, crear_panel_instrucciones
from .selector_nivel import SelectorNivel
from .ventana_estadistica_ii import VentanaEstadisticaII

__all__ = [
    'App',
    'main',
    'PantallaLogin',
    'MenuPrincipal',
    'VentanaAnalisis',
    'crear_panel_instrucciones',
    'SelectorNivel',
    'VentanaEstadisticaII'
]

__version__ = '1.0'
__author__ = 'Ana Paula Vásquez, María Mendez, Ariana Morales'