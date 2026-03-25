"""Modulo UI: temas de muestreo para Estadistica II."""

import random
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

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

    frame_selector = tk.LabelFrame(
        ventana,
        text="Selector de elementos",
        padx=10,
        pady=10,
        bg=BG_WHITE,
        font=("Helvetica", 11, "bold"),
    )
    frame_selector.pack(fill="x", padx=10, pady=(0, 8))

    tk.Label(frame_selector, text="Elementos (separados por coma):", bg=BG_WHITE).grid(row=0, column=0, sticky="w", pady=4)
    elementos_var = tk.StringVar(value="A,B,C,D,E,F,G,H,I,J")
    tk.Entry(frame_selector, textvariable=elementos_var, width=70).grid(
        row=0, column=1, columnspan=3, padx=6, pady=4, sticky="we"
    )

    tk.Label(frame_selector, text="Tamano de muestra (n):", bg=BG_WHITE).grid(row=1, column=0, sticky="w", pady=4)
    n_var = tk.StringVar(value="4")
    tk.Entry(frame_selector, textvariable=n_var, width=20).grid(row=1, column=1, padx=6, pady=4, sticky="w")

    tk.Label(frame_selector, text="Metodo:", bg=BG_WHITE).grid(row=1, column=2, sticky="e", pady=4)
    metodo_var = tk.StringVar(value="Aleatorio simple")
    ttk.Combobox(
        frame_selector,
        textvariable=metodo_var,
        state="readonly",
        values=["Aleatorio simple", "Sistematico"],
        width=24,
    ).grid(row=1, column=3, padx=6, pady=4, sticky="w")

    tk.Label(frame_selector, text="Semilla (opcional):", bg=BG_WHITE).grid(row=2, column=0, sticky="w", pady=4)
    semilla_var = tk.StringVar(value="")
    tk.Entry(frame_selector, textvariable=semilla_var, width=20).grid(row=2, column=1, padx=6, pady=4, sticky="w")

    resultado_var = tk.StringVar(value="Muestra seleccionada: -")
    tk.Label(
        frame_selector,
        textvariable=resultado_var,
        bg=BG_WHITE,
        fg=COLOR_PRIMARY,
        font=("Helvetica", 10, "bold"),
    ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 4))

    def seleccionar_elementos():
        try:
            elementos = [e.strip() for e in elementos_var.get().split(",") if e.strip()]
            if not elementos:
                raise ValueError("Ingrese al menos un elemento.")

            n = int(float(n_var.get()))
            if n <= 0:
                raise ValueError("n debe ser mayor que cero.")
            if n > len(elementos):
                raise ValueError("n no puede ser mayor que el numero de elementos.")

            if semilla_var.get().strip():
                random.seed(int(float(semilla_var.get())))

            metodo = metodo_var.get()
            if metodo == "Aleatorio simple":
                muestra = random.sample(elementos, n)
                detalle = "Muestreo aleatorio simple"
            else:
                n_total = len(elementos)
                paso = max(1, n_total // n)
                inicio = random.randint(0, paso - 1)

                indices = []
                idx = inicio
                while idx < n_total and len(indices) < n:
                    indices.append(idx)
                    idx += paso

                if len(indices) < n:
                    faltan = n - len(indices)
                    restantes = [i for i in range(n_total) if i not in indices]
                    indices.extend(restantes[:faltan])

                muestra = [elementos[i] for i in indices]
                detalle = f"Muestreo sistematico (k={paso}, inicio={inicio + 1})"

            resultado_var.set(f"Muestra seleccionada: {muestra}")
            messagebox.showinfo("Seleccion completada", detalle)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo seleccionar la muestra:\n{e}")

    tk.Button(
        frame_selector,
        text="Seleccionar elementos",
        command=seleccionar_elementos,
        bg=COLOR_SUCCESS,
        fg="#000000",
        font=("Helvetica", 10, "bold"),
        cursor="hand2",
        padx=12,
        pady=6,
        activebackground="#FFEB3B",
        activeforeground="#000000",
    ).grid(row=2, column=3, padx=6, pady=4, sticky="e")

    frame_selector.grid_columnconfigure(1, weight=1)
    frame_selector.grid_columnconfigure(3, weight=1)

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
