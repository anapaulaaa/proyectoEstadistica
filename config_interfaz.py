"""
Configuración de colores, estilos y constantes para la interfaz gráfica
"""

# ============== INFORMACIÓN DEL PROYECTO ==============
NOMBRE_PROYECTO = "StatPro - Analizador Estadístico"
VERSION = "1.0"
AUTOR = "Ana Paula Vásquez, María Mendez, Ariana Morales"
UNIVERSIDAD = "UMG Huehuetenango"
CARRERA = "Ingeniería en Sistemas - 4to Ciclo"

# ============== COLORES PRINCIPALES ==============
COLOR_PRIMARY = "#2C3E50"      # Azul oscuro elegante
COLOR_SECONDARY = "#3498DB"    # Azul claro
COLOR_SUCCESS = "#27AE60"      # Verde
COLOR_WARNING = "#F39C12"      # Naranja
COLOR_DANGER = "#E74C3C"       # Rojo
COLOR_INFO = "#16A085"         # Turquesa

# ============== COLORES DE FONDO ==============
BG_DARK = "#1A1A2E"           # Fondo oscuro principal
BG_MEDIUM = "#16213E"         # Fondo medio
BG_LIGHT = "#F8F9FA"          # Fondo claro
BG_WHITE = "#FFFFFF"          # Blanco puro

# ============== COLORES DE TEXTO ==============
TEXT_DARK = "#2C3E50"         # Texto oscuro
TEXT_LIGHT = "#ECF0F1"        # Texto claro
TEXT_MUTED = "#95A5A6"        # Texto secundario

# ============== COLORES PARA GRÁFICOS ==============
COLORES_GRAFICOS = [
    "#3498DB",  # Azul
    "#E74C3C",  # Rojo
    "#2ECC71",  # Verde
    "#F39C12",  # Naranja
    "#9B59B6",  # Púrpura
    "#1ABC9C",  # Turquesa
    "#34495E",  # Gris oscuro
    "#E67E22",  # Naranja oscuro
]

# ============== FUENTES ==============
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_SUBTITLE = ("Helvetica", 16, "bold")
FONT_NORMAL = ("Helvetica", 11)
FONT_SMALL = ("Helvetica", 9)
FONT_BUTTON = ("Helvetica", 10, "bold")

# ============== DIMENSIONES ==============
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 2
ENTRY_WIDTH = 30

# ============== ESTILOS PARA BOTONES ==============
STYLE_BTN_PRIMARY = {
    "bg": COLOR_PRIMARY,
    "fg": TEXT_LIGHT,
    "font": FONT_BUTTON,
    "width": BUTTON_WIDTH,
    "height": BUTTON_HEIGHT,
    "relief": "flat",
    "cursor": "hand2"
}

STYLE_BTN_SUCCESS = {
    "bg": COLOR_SUCCESS,
    "fg": TEXT_LIGHT,
    "font": FONT_BUTTON,
    "width": BUTTON_WIDTH,
    "height": BUTTON_HEIGHT,
    "relief": "flat",
    "cursor": "hand2"
}

STYLE_BTN_DANGER = {
    "bg": COLOR_DANGER,
    "fg": TEXT_LIGHT,
    "font": FONT_BUTTON,
    "width": BUTTON_WIDTH,
    "height": BUTTON_HEIGHT,
    "relief": "flat",
    "cursor": "hand2"
}

STYLE_BTN_INFO = {
    "bg": COLOR_INFO,
    "fg": TEXT_LIGHT,
    "font": FONT_BUTTON,
    "width": BUTTON_WIDTH,
    "height": BUTTON_HEIGHT,
    "relief": "flat",
    "cursor": "hand2"
}

# ============== ESTILOS PARA LABELS ==============
STYLE_LABEL_TITLE = {
    "font": FONT_TITLE,
    "fg": COLOR_PRIMARY,
    "bg": BG_LIGHT
}

STYLE_LABEL_SUBTITLE = {
    "font": FONT_SUBTITLE,
    "fg": COLOR_SECONDARY,
    "bg": BG_LIGHT
}

STYLE_LABEL_NORMAL = {
    "font": FONT_NORMAL,
    "fg": TEXT_DARK,
    "bg": BG_LIGHT
}

# ============== CONFIGURACIÓN DE MATPLOTLIB ==============
MATPLOTLIB_STYLE = {
    'figure.facecolor': BG_WHITE,
    'axes.facecolor': BG_LIGHT,
    'axes.edgecolor': COLOR_PRIMARY,
    'axes.labelcolor': TEXT_DARK,
    'xtick.color': TEXT_DARK,
    'ytick.color': TEXT_DARK,
    'grid.color': TEXT_MUTED,
    'grid.alpha': 0.3,
    'lines.linewidth': 2,
    'font.size': 10,
}

# ============== USUARIOS PREDEFINIDOS (para login) ==============
USUARIOS = {
    "admin": "admin123",
    "ana": "estadistica2024",
    "profesor": "umg2024",
    "invitado": "guest"
}

# ============== MENSAJES ==============
MSG_BIENVENIDA = f"""
¡Bienvenido a {NOMBRE_PROYECTO}!

Sistema integral de análisis estadístico
desarrollado como proyecto final del curso
de Estadística I

Autor: {AUTOR}
{CARRERA}
{UNIVERSIDAD}
"""

MSG_LOGIN_EXITOSO = "¡Inicio de sesión exitoso!"
MSG_LOGIN_FALLIDO = "Usuario o contraseña incorrectos"
MSG_ARCHIVO_CARGADO = "Archivo cargado correctamente"
MSG_ERROR_ARCHIVO = "Error al cargar el archivo"
MSG_CALCULOS_COMPLETADOS = "Cálculos completados exitosamente"

# ============== ÍCONOS Y SÍMBOLOS ==============
ICONO_ESTADISTICA = "📊"
ICONO_PROBABILIDAD = "🎲"
ICONO_GRAFICO = "📈"
ICONO_CALCULADORA = "🧮"
ICONO_ARCHIVO = "📁"
ICONO_EXPORTAR = "💾"
ICONO_INFO = "ℹ️"
ICONO_EXITO = "✅"
ICONO_ERROR = "❌"
ICONO_ALERTA = "⚠️"

# ============== TÍTULOS DE SECCIONES ==============
TITULO_DESCRIPTIVA = f"{ICONO_ESTADISTICA} Estadística Descriptiva"
TITULO_INFERENCIAL = f"{ICONO_PROBABILIDAD} Estadística Inferencial"
TITULO_TENDENCIA = "Medidas de Tendencia Central"
TITULO_POSICION = "Medidas de Posición"
TITULO_DISPERSION = "Medidas de Dispersión"
TITULO_FORMA = "Medidas de Forma"
TITULO_PROBABILIDAD = "Probabilidades"
TITULO_DISTRIBUCIONES = "Distribuciones de Probabilidad"
TITULO_REGRESION = "Regresión y Correlación"
TITULO_BAYES = "Teorema de Bayes"