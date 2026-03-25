"""Modulo UI: temas de muestreo para Estadistica II."""

import tkinter as tk
from tkinter import ttk, scrolledtext

from config_interfaz import *


def _crear_bloque_texto(parent, titulo, contenido):
    frame = tk.LabelFrame(
        parent,
        text=titulo,
        padx=12,
        pady=12,
        bg=BG_WHITE,
        font=("Helvetica", 11, "bold"),
    )
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    area = scrolledtext.ScrolledText(frame, height=22, width=110, font=("Consolas", 10), bg=BG_WHITE)
    area.pack(fill="both", expand=True)
    area.insert(tk.END, contenido)
    area.config(state="disabled")


def abrir_modulo_muestreo(root):
    """Abre el modulo teorico-practico de muestreo."""
    ventana = tk.Toplevel(root)
    ventana.title("🧩 Seleccion y Tipos de Muestreo")

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.9)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
    ventana.configure(bg=BG_LIGHT)

    tk.Label(
        ventana,
        text="🧩 SELECCION Y TIPOS DE MUESTREO",
        font=("Helvetica", 16, "bold"),
        bg=BG_LIGHT,
        fg=COLOR_PRIMARY,
    ).pack(pady=12)

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    tab_general = tk.Frame(notebook, bg=BG_WHITE)
    tab_prob = tk.Frame(notebook, bg=BG_WHITE)
    tab_no_prob = tk.Frame(notebook, bg=BG_WHITE)
    tab_errores = tk.Frame(notebook, bg=BG_WHITE)

    notebook.add(tab_general, text="Marco General")
    notebook.add(tab_prob, text="Muestreo Probabilistico")
    notebook.add(tab_no_prob, text="Muestreo No Probabilistico")
    notebook.add(tab_errores, text="Errores y Referencias")

    texto_general = """
1. CALCULO DEL TAMANO DE MUESTRA
   - Define cuantas unidades necesitas observar para estimar parametros con precision.
   - Depende de: nivel de confianza, margen de error, variabilidad y tamano poblacional.

2. ESTIMACION DE PROPORCIONES
   - Se usa cuando la variable es dicotomica (si/no, exito/fracaso).
   - Permite estimar p_hat y construir intervalos de confianza.

3. ESTIMACION DE MEDIAS
   - Se usa con variables cuantitativas (edad, peso, ingreso, etc.).
   - Requiere media muestral, desviacion estandar y n.

4. NIVELES DE CONFIANZA
   - Expresan el grado de seguridad del intervalo.
   - A mayor confianza, mayor amplitud del intervalo.

5. CONSIDERACIONES EN EL TAMANO DE MUESTRA
   - Objetivo del estudio.
   - Recursos disponibles (tiempo, presupuesto, personal).
   - Homogeneidad/heterogeneidad de la poblacion.
   - Riesgo de no respuesta y perdidas.

6. SELECCION DE LA MUESTRA
   - Es el procedimiento para elegir elementos de la poblacion.
   - Debe ser coherente con el tipo de muestreo elegido.
"""

    texto_prob = """
MUESTREO PROBABILISTICO
Todos los elementos tienen probabilidad conocida y mayor que cero de ser seleccionados.

1. MUESTREO ALEATORIO SIMPLE
   - Seleccion completamente al azar.
   - Requiere marco muestral completo.
   - Ventaja: facil analisis estadistico e inferencia.

2. MUESTREO SISTEMATICO
   - Se elige cada k-esimo elemento despues de un inicio aleatorio.
   - k = N / n aproximadamente.
   - Rapido y practico, pero cuidado con patrones periodicos.

3. MUESTREO ESTRATIFICADO
   - La poblacion se divide en estratos homogeneos (sexo, edad, region, etc.).
   - Luego se muestrea dentro de cada estrato.
   - Mejora precision y representatividad de subgrupos.

4. MUESTREO POR CONGLOMERADOS
   - Se seleccionan grupos naturales (escuelas, barrios, empresas) en lugar de individuos directos.
   - Reduce costos logisticos.
   - Suele tener mayor error muestral que el estratificado.
"""

    texto_no_prob = """
MUESTREO NO PROBABILISTICO
La probabilidad de inclusion no es conocida; se usa mucho en estudios exploratorios.

1. MUESTREO POR CONVENIENCIA
   - Se eligen casos faciles de acceder.
   - Rapido y economico.
   - Limite: baja generalizacion.

2. MUESTREO POR JUICIO (INTENCIONAL)
   - El investigador selecciona casos segun criterio experto.
   - Util para estudios cualitativos o de especialistas.

3. MUESTREO POR CUOTAS
   - Se fijan cuotas por categorias (ej. 50% hombres, 50% mujeres).
   - No aleatorio dentro de cada cuota.

4. MUESTREO BOLA DE NIEVE
   - Participantes iniciales recomiendan nuevos participantes.
   - Util en poblaciones dificiles de localizar.
"""

    texto_errores = """
ERRORES EN EL MUESTREO

1. ERROR MUESTRAL
   - Diferencia natural entre estadistico muestral y parametro poblacional.
   - Disminuye al aumentar n y mejorar el diseno muestral.

2. ERROR DE COBERTURA
   - El marco muestral no representa bien a la poblacion objetivo.

3. ERROR DE NO RESPUESTA
   - Parte de la muestra seleccionada no responde.
   - Puede generar sesgo si la no respuesta no es aleatoria.

4. ERROR DE MEDICION
   - Instrumento mal disenado, preguntas ambiguas o sesgo del encuestador.

5. ERROR DE PROCESAMIENTO
   - Errores al digitar, codificar, limpiar o analizar datos.

REFERENCIAS BIBLIOGRAFICAS SUGERIDAS
1. Cochran, W. G. (1977). Sampling Techniques. 3rd ed. Wiley.
2. Lohr, S. L. (2019). Sampling: Design and Analysis. 2nd ed. Chapman & Hall/CRC.
3. Levy, P. S., & Lemeshow, S. (2013). Sampling of Populations. 4th ed. Wiley.
4. Hernandez Sampieri, R., Fernandez Collado, C., & Baptista, P. Metodologia de la investigacion.
"""

    _crear_bloque_texto(tab_general, "Fundamentos", texto_general)
    _crear_bloque_texto(tab_prob, "Tipos Probabilisticos", texto_prob)
    _crear_bloque_texto(tab_no_prob, "Tipos No Probabilisticos", texto_no_prob)
    _crear_bloque_texto(tab_errores, "Errores y Bibliografia", texto_errores)

    def ir_a_calculadora():
        from interfaz.estadistica_ii.modulo_estimacion import abrir_modulo_estimacion_tamano_muestra

        ventana.destroy()
        abrir_modulo_estimacion_tamano_muestra(root)

    frame_nav = tk.Frame(ventana, bg=BG_LIGHT)
    frame_nav.pack(pady=10)

    tk.Button(
        frame_nav,
        text="📊 Ir a Calculadora",
        command=ir_a_calculadora,
        bg=COLOR_INFO,
        fg="#000000",
        font=("Helvetica", 11, "bold"),
        cursor="hand2",
        padx=20,
        pady=8,
        activebackground="#FFEB3B",
        activeforeground="#000000",
    ).pack(side="left", padx=5)

    tk.Button(
        frame_nav,
        text="⬅️ Regresar al Menu",
        command=ventana.destroy,
        bg="#9C27B0",
        fg="#000000",
        font=("Helvetica", 11, "bold"),
        cursor="hand2",
        padx=20,
        pady=8,
        activebackground="#FFEB3B",
        activeforeground="#000000",
    ).pack(side="left", padx=5)
