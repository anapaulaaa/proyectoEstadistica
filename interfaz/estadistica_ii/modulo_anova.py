"""Modulos UI para ANOVA dentro de Estadistica II."""

from __future__ import annotations

import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

import numpy as np

from config_interfaz import *
from estadistica_inferencial.anova import (
    anova_dos_factores_con_replicacion,
    anova_dos_factores_sin_replicacion,
    anova_un_factor,
)


EXAMPLES_ANOVA_1 = {
    "Colores de cajas y ventas": {
        "grupos": [
            ("Rojo", [15, 18, 17, 16, 19]),
            ("Azul", [22, 24, 21, 23, 25]),
            ("Verde", [20, 19, 18, 21, 20]),
            ("Amarillo", [28, 27, 29, 30, 26]),
        ],
        "procedimiento": "Se comparan las ventas promedio entre cuatro colores de cajas para determinar si el color influye en el resultado comercial.",
    },
    "Profesores y rendimiento": {
        "grupos": [
            ("Prof. A", [78, 82, 80, 79, 81]),
            ("Prof. B", [74, 76, 73, 75, 72]),
            ("Prof. C", [88, 90, 87, 89, 91]),
        ],
        "procedimiento": "Se analizan los promedios de rendimiento para verificar si existen diferencias significativas entre docentes.",
    },
    "Algodón y resistencia": {
        "grupos": [
            ("10%", [52, 54, 53, 55, 51]),
            ("20%", [60, 61, 59, 62, 60]),
            ("30%", [67, 68, 66, 69, 67]),
            ("40%", [73, 72, 74, 71, 75]),
        ],
        "procedimiento": "Se evalúa si el porcentaje de algodón cambia la resistencia promedio del material.",
    },
    "Temperaturas y bateria": {
        "grupos": [
            ("Baja", [8.1, 8.4, 8.3, 8.2, 8.5]),
            ("Media", [7.4, 7.6, 7.5, 7.3, 7.7]),
            ("Alta", [6.8, 6.7, 6.9, 6.6, 6.8]),
        ],
        "procedimiento": "Se comparan duraciones de bateria bajo distintas temperaturas para identificar diferencias en las medias.",
    },
}


EXAMPLES_ANOVA_2_NO_REP = {
    "Algoritmos y navegadores": {
        "filas": ["Algoritmo A", "Algoritmo B", "Algoritmo C"],
        "columnas": ["Chrome", "Edge", "Firefox"],
        "matriz": [[82, 79, 85], [76, 74, 77], [88, 86, 90]],
        "procedimiento": "Se comparan los tiempos promedio entre algoritmos y navegadores para evaluar si alguno modifica el desempeño.",
    },
    "Querys y bases de datos": {
        "filas": ["Query 1", "Query 2", "Query 3"],
        "columnas": ["MySQL", "PostgreSQL", "SQL Server", "SQLite"],
        "matriz": [[4.1, 4.4, 4.2, 4.0], [5.2, 5.1, 5.0, 5.3], [6.0, 5.8, 5.9, 6.1]],
        "procedimiento": "Se evalúa si el tiempo de respuesta cambia según la query y la base de datos sin considerar replicaciones.",
    },
    "Servidores y querys": {
        "filas": ["Servidor 1", "Servidor 2", "Servidor 3"],
        "columnas": ["Query A", "Query B", "Query C"],
        "matriz": [[120, 115, 118], [132, 128, 130], [125, 123, 127]],
        "procedimiento": "Se observa si existen diferencias por servidor y por tipo de consulta.",
    },
    "Conferencias y semestres": {
        "filas": ["Semestre 1", "Semestre 2", "Semestre 3"],
        "columnas": ["Conferencia A", "Conferencia B", "Conferencia C"],
        "matriz": [[78, 80, 79], [82, 83, 81], [85, 84, 86]],
        "procedimiento": "Se comparan evaluaciones por semestre y tipo de conferencia para detectar efecto de filas o columnas.",
    },
}


EXAMPLES_ANOVA_2_REP = {
    "Querys y bases de datos": {
        "filas": ["Query 1", "Query 2", "Query 3"],
        "columnas": ["MySQL", "PostgreSQL", "SQL Server"],
        "cubo": [
            [[4.1, 4.0], [4.4, 4.5], [4.2, 4.1]],
            [[5.2, 5.1], [5.1, 5.0], [5.0, 5.2]],
            [[6.0, 6.1], [5.8, 5.9], [5.9, 6.0]],
        ],
        "procedimiento": "Se comparan varias observaciones por celda para evaluar factor A, factor B e interaccion.",
    },
    "Servidores y querys": {
        "filas": ["Servidor 1", "Servidor 2", "Servidor 3"],
        "columnas": ["Query A", "Query B", "Query C"],
        "cubo": [
            [[120, 121], [115, 116], [118, 119]],
            [[132, 133], [128, 129], [130, 131]],
            [[125, 126], [123, 124], [127, 128]],
        ],
        "procedimiento": "Se analiza el efecto combinado de servidores y consultas con replicaciones por celda.",
    },
    "Conferencias y semestres": {
        "filas": ["Semestre 1", "Semestre 2", "Semestre 3"],
        "columnas": ["Conferencia A", "Conferencia B", "Conferencia C"],
        "cubo": [
            [[78, 79], [80, 81], [79, 80]],
            [[82, 83], [83, 84], [81, 82]],
            [[85, 86], [84, 85], [86, 87]],
        ],
        "procedimiento": "Se estudia si existen diferencias significativas por semestre, por conferencia y por su interaccion.",
    },
    "Algoritmos y navegadores": {
        "filas": ["Algoritmo A", "Algoritmo B", "Algoritmo C"],
        "columnas": ["Chrome", "Edge", "Firefox"],
        "cubo": [
            [[82, 83], [79, 80], [85, 84]],
            [[76, 77], [74, 75], [77, 78]],
            [[88, 89], [86, 87], [90, 91]],
        ],
        "procedimiento": "Se compara el rendimiento por algoritmo y navegador usando varias observaciones por celda.",
    },
}


EXERCISES_ANOVA = [
    {
        "clave": "EJ01",
        "tipo": "1 factor",
        "titulo": "EJ01 - Colores de cajas y ventas",
        "datos": EXAMPLES_ANOVA_1["Colores de cajas y ventas"],
        "procedimiento": "Hipotesis: H0 = las medias de ventas son iguales para todos los colores. H1 = al menos un color cambia la media de ventas.",
    },
    {
        "clave": "EJ02",
        "tipo": "1 factor",
        "titulo": "EJ02 - Profesores y rendimiento",
        "datos": EXAMPLES_ANOVA_1["Profesores y rendimiento"],
        "procedimiento": "Se contrasta si el docente influye en el rendimiento promedio de los estudiantes.",
    },
    {
        "clave": "EJ03",
        "tipo": "2 factores sin replicacion",
        "titulo": "EJ03 - Algoritmos y navegadores",
        "datos": EXAMPLES_ANOVA_2_NO_REP["Algoritmos y navegadores"],
        "procedimiento": "Se evalua el efecto de filas y columnas con una observacion por celda.",
    },
    {
        "clave": "EJ04",
        "tipo": "2 factores con replicacion",
        "titulo": "EJ04 - Querys y bases de datos",
        "datos": EXAMPLES_ANOVA_2_REP["Querys y bases de datos"],
        "procedimiento": "Se revisan los efectos principales y la interaccion usando varias observaciones por celda.",
    },
]


def _centrar_ventana(ventana, proporcion_w=0.95, proporcion_h=0.92):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    window_width = int(screen_width * proporcion_w)
    window_height = int(screen_height * proporcion_h)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")


def _configurar_ventana(ventana, titulo):
    ventana.title(titulo)
    ventana.configure(bg=BG_LIGHT)
    _centrar_ventana(ventana)
    try:
        ventana.state("zoomed")
    except Exception:
        pass


def _volver_a_menu_anova(root, ventana):
    ventana.destroy()
    abrir_modulo_anova_menu(root)


def _crear_barra_navegacion(ventana, titulo, volver_callback=None, volver_texto="← Volver"):
    barra = tk.Frame(ventana, bg=COLOR_PRIMARY, height=64)
    barra.pack(fill="x", side="top")

    frame_izq = tk.Frame(barra, bg=COLOR_PRIMARY)
    frame_izq.pack(side="left", padx=14, pady=10)

    if volver_callback is not None:
        tk.Button(
            frame_izq,
            text=volver_texto,
            command=volver_callback,
            bg=COLOR_INFO,
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="left", padx=(0, 10))

    tk.Label(
        frame_izq,
        text=titulo,
        font=("Helvetica", 15, "bold"),
        bg=COLOR_PRIMARY,
        fg=TEXT_LIGHT,
    ).pack(side="left")

    tk.Button(
        barra,
        text="Cerrar",
        command=ventana.destroy,
        bg=COLOR_DANGER,
        fg="#000000",
        font=("Helvetica", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=6,
        activebackground="#FFEB3B",
        activeforeground="#000000",
    ).pack(side="right", padx=14, pady=10)


def _crear_scroll_frame(parent, bg=BG_LIGHT):
    contenedor = tk.Frame(parent, bg=bg)
    contenedor.pack(fill="both", expand=True)
    contenedor.columnconfigure(0, weight=1)
    contenedor.rowconfigure(0, weight=1)

    canvas = tk.Canvas(contenedor, bg=bg, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar_y = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    scrollbar_x = ttk.Scrollbar(contenedor, orient="horizontal", command=canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    frame = tk.Frame(canvas, bg=bg)
    window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

    def _actualizar_scroll(_event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", _actualizar_scroll)
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=max(event.width, frame.winfo_reqwidth())))
    return contenedor, canvas, frame


def _crear_titulo(parent, titulo, subtitulo):
    tk.Label(parent, text=titulo, font=("Helvetica", 18, "bold"), bg=BG_LIGHT, fg=COLOR_PRIMARY).pack(anchor="w", pady=(2, 4))
    tk.Label(parent, text=subtitulo, font=("Helvetica", 10), bg=BG_LIGHT, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 8))


def _crear_panel_seccion(parent, titulo, subtitulo, bg, fg_titulo, fg_subtitulo):
    panel = tk.LabelFrame(parent, text=titulo, bg=bg, font=("Helvetica", 11, "bold"), fg=fg_titulo, padx=10, pady=10)
    panel.pack(fill="x", pady=(0, 10))
    tk.Label(panel, text=subtitulo, bg=bg, fg=fg_subtitulo, font=("Helvetica", 9, "italic"), anchor="w", justify="left", wraplength=1200).pack(anchor="w", pady=(0, 8))
    return panel


def _crear_tarjetas_metricas(parent, tarjetas):
    contenedor = tk.Frame(parent, bg=BG_LIGHT)
    contenedor.pack(fill="x", pady=(0, 10))

    for tarjeta in tarjetas:
        card = tk.Frame(contenedor, bg=tarjeta["bg"], relief="solid", borderwidth=1)
        card.pack(side="left", fill="both", expand=True, padx=6)
        tk.Label(card, text=tarjeta["titulo"], bg=tarjeta["bg"], fg=tarjeta["fg_titulo"], font=("Helvetica", 10, "bold")).pack(pady=(10, 4))
        tk.Label(card, text=tarjeta["valor"], bg=tarjeta["bg"], fg=tarjeta["fg_valor"], font=("Helvetica", 14, "bold")).pack(pady=(0, 4))
        tk.Label(card, text=tarjeta["detalle"], bg=tarjeta["bg"], fg=tarjeta["fg_detalle"], font=("Helvetica", 9)).pack(pady=(0, 10))


def _parsear_lista_numeros(texto):
    valores = []
    for parte in re.split(r"[\s,;\n]+", str(texto).strip()):
        if parte:
            valores.append(float(parte.replace(",", ".")))
    return valores


def _limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def _formatear_numero(valor):
    if valor is None:
        return ""
    if isinstance(valor, (float, np.floating)):
        if np.isnan(valor):
            return ""
        if np.isinf(valor):
            return "∞"
        return f"{valor:.6f}".rstrip("0").rstrip(".")
    return str(valor)


def _crear_estilo_treeview():
    style = ttk.Style()
    try:
        style.theme_use("default")
    except Exception:
        pass
    style.configure(
        "Anova.Treeview",
        font=("Helvetica", 10),
        rowheight=26,
        background=BG_WHITE,
        fieldbackground=BG_WHITE,
        foreground=TEXT_DARK,
        bordercolor="#CFD8DC",
        lightcolor="#CFD8DC",
        darkcolor="#CFD8DC",
    )
    style.configure(
        "Anova.Treeview.Heading",
        font=("Helvetica", 10, "bold"),
        background=COLOR_PRIMARY,
        foreground=TEXT_LIGHT,
        relief="flat",
    )
    style.map("Anova.Treeview", background=[("selected", "#DDEEFF")], foreground=[("selected", TEXT_DARK)])


def _crear_tabla_dataframe(parent, dataframe, titulo=None, altura=10):
    contenedor = tk.Frame(parent, bg=BG_LIGHT)
    contenedor.pack(fill="both", expand=True, pady=6)

    if titulo:
        tk.Label(contenedor, text=titulo, font=("Helvetica", 11, "bold"), bg=BG_LIGHT, fg=COLOR_PRIMARY).pack(anchor="w", pady=(0, 4))

    marco = tk.Frame(contenedor, bg=BG_WHITE, relief="solid", borderwidth=1)
    marco.pack(fill="both", expand=True)

    columnas = list(dataframe.columns)
    tree = ttk.Treeview(marco, columns=columnas, show="headings", style="Anova.Treeview", height=altura)
    vsb = ttk.Scrollbar(marco, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(marco, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    for columna in columnas:
        tree.heading(columna, text=str(columna))
        tree.column(columna, width=max(110, len(str(columna)) * 10), anchor="center")

    for _, fila in dataframe.iterrows():
        valores = [_formatear_numero(valor) for valor in fila.tolist()]
        tree.insert("", "end", values=valores)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    marco.rowconfigure(0, weight=1)
    marco.columnconfigure(0, weight=1)
    return tree


def _texto_dataframe(dataframe):
    if dataframe is None:
        return "Sin datos para mostrar."
    if hasattr(dataframe, "empty") and dataframe.empty:
        return "Sin datos para mostrar."
    return dataframe.to_string(index=False)


class _BaseAnovaView:
    def __init__(self, parent):
        self.parent = parent
        self.resultado = None
        self.frame = tk.Frame(parent, bg=BG_LIGHT)
        self.frame.pack(fill="both", expand=True)

    def _crear_selector_alpha(self, parent):
        tk.Label(parent, text="Alpha:", bg=BG_LIGHT, font=("Helvetica", 10, "bold")).pack(side="left")
        self.alpha_var = tk.StringVar(value="0.05")
        ttk.Combobox(parent, textvariable=self.alpha_var, values=["0.10", "0.05", "0.01"], state="readonly", width=10).pack(side="left", padx=8)

    def _render_dataframe(self, contenedor, dataframe, titulo=None):
        _crear_tabla_dataframe(contenedor, dataframe, titulo=titulo)

    def _reset_resultados(self):
        self.resultado = None
        for widget in getattr(self, "frame_resultados", []).winfo_children() if hasattr(self, "frame_resultados") else []:
            widget.destroy()


class VentanaAnova1Factor(_BaseAnovaView):
    def __init__(self, root):
        ventana = tk.Toplevel(root)
        self.ventana = ventana
        _configurar_ventana(ventana, "ANOVA de 1 Factor")
        _crear_barra_navegacion(
            ventana,
            "ANOVA de 1 Factor",
            volver_callback=lambda: _volver_a_menu_anova(root, ventana),
            volver_texto="← Menú ANOVA",
        )
        super().__init__(ventana)
        self.ejemplos = list(EXAMPLES_ANOVA_1.keys())
        self.nombre_vars = []
        self.valor_entries = []
        self._construir()

    def _construir(self):
        cont = self.frame
        _crear_titulo(cont, "ANOVA de 1 Factor", "Ingreso dinamico de grupos, resumen estadistico y tabla ANOVA estilo Excel.")

        panel_control = _crear_panel_seccion(
            cont,
            "Controles",
            "Carga un ejemplo o ingresa datos manuales antes de calcular.",
            "#E8F5E9",
            COLOR_PRIMARY,
            "#1B5E20",
        )

        fila1 = tk.Frame(panel_control, bg=BG_WHITE)
        fila1.pack(fill="x", pady=4)
        tk.Label(fila1, text="Ejemplo:", bg=BG_WHITE).pack(side="left")
        self.ejemplo_var = tk.StringVar(value=self.ejemplos[0])
        ttk.Combobox(fila1, textvariable=self.ejemplo_var, values=self.ejemplos, state="readonly", width=32).pack(side="left", padx=8)
        tk.Button(fila1, text="Cargar ejemplo", command=self.cargar_ejemplo, bg=COLOR_INFO, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)
        tk.Button(fila1, text="Limpiar", command=self.limpiar_datos, bg=COLOR_WARNING, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)

        fila2 = tk.Frame(panel_control, bg=BG_WHITE)
        fila2.pack(fill="x", pady=4)
        tk.Label(fila2, text="Numero de grupos:", bg=BG_WHITE).pack(side="left")
        self.grupos_var = tk.IntVar(value=4)
        tk.Spinbox(fila2, from_=2, to=12, width=6, textvariable=self.grupos_var).pack(side="left", padx=(6, 18))
        tk.Label(fila2, text="Observaciones por grupo:", bg=BG_WHITE).pack(side="left")
        self.obs_var = tk.IntVar(value=5)
        tk.Spinbox(fila2, from_=2, to=20, width=6, textvariable=self.obs_var).pack(side="left", padx=(6, 18))
        self._crear_selector_alpha(fila2)
        tk.Button(fila2, text="Generar tabla", command=self.generar_tabla, bg=COLOR_SECONDARY, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=8)
        tk.Button(fila2, text="Calcular ANOVA", command=self.calcular, bg=COLOR_SUCCESS, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)

        self.frame_entrada = _crear_panel_seccion(
            cont,
            "Datos de entrada",
            "Cada columna representa un grupo y cada fila una observacion.",
            "#FFF8E1",
            COLOR_PRIMARY,
            "#8A6D00",
        )
        self._crear_matriz_entrada()

        self.notebook = ttk.Notebook(cont)
        self.notebook.pack(fill="both", expand=True)
        self.tab_datos = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.tab_resumen = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.tab_anova = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.tab_interpretacion = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.notebook.add(self.tab_datos, text="Tabla de datos")
        self.notebook.add(self.tab_resumen, text="Resumen estadistico")
        self.notebook.add(self.tab_anova, text="Analisis de varianza")
        self.notebook.add(self.tab_interpretacion, text="Interpretacion")

        self.text_interpretacion = scrolledtext.ScrolledText(self.tab_interpretacion, height=18, font=("Consolas", 10), bg=BG_WHITE)
        self.text_interpretacion.pack(fill="both", expand=True, padx=8, pady=8)

        self.frame_datos_tab = tk.Frame(self.tab_datos, bg=BG_LIGHT)
        self.frame_datos_tab.pack(fill="both", expand=True, padx=8, pady=8)

        self.frame_resumen_tab = tk.Frame(self.tab_resumen, bg=BG_LIGHT)
        self.frame_resumen_tab.pack(fill="both", expand=True, padx=8, pady=8)

        self.frame_anova_tab = tk.Frame(self.tab_anova, bg=BG_LIGHT)
        self.frame_anova_tab.pack(fill="both", expand=True, padx=8, pady=8)

        self.frame_metricas = tk.Frame(self.tab_interpretacion, bg=BG_LIGHT)
        self.frame_metricas.pack(fill="x", padx=8, pady=(8, 0))

        self.generar_tabla()
        self.cargar_ejemplo()

    def _crear_matriz_entrada(self):
        _limpiar_frame(self.frame_entrada)
        grupos = int(self.grupos_var.get())
        observaciones = int(self.obs_var.get())
        self.nombre_vars = [tk.StringVar(value=f"Grupo {i + 1}") for i in range(grupos)]
        self.valor_entries = []

        encabezado = tk.Frame(self.frame_entrada, bg=BG_WHITE)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="Obs.", bg=BG_WHITE, font=("Helvetica", 10, "bold"), width=10).grid(row=0, column=0, padx=4, pady=4)
        for indice, nombre_var in enumerate(self.nombre_vars, start=1):
            entrada_nombre = tk.Entry(encabezado, textvariable=nombre_var, width=18, justify="center")
            entrada_nombre.grid(row=0, column=indice, padx=4, pady=4)

        grid_frame = tk.Frame(self.frame_entrada, bg=BG_WHITE)
        grid_frame.pack(fill="x", pady=(8, 0))

        for fila in range(observaciones):
            tk.Label(grid_frame, text=f"{fila + 1}", bg=BG_WHITE, width=10).grid(row=fila, column=0, padx=4, pady=3)
            fila_entries = []
            for columna in range(grupos):
                entry = tk.Entry(grid_frame, width=18, justify="center")
                entry.grid(row=fila, column=columna + 1, padx=4, pady=3)
                fila_entries.append(entry)
            self.valor_entries.append(fila_entries)

    def generar_tabla(self):
        self._crear_matriz_entrada()

    def limpiar_datos(self):
        for nombre in self.nombre_vars:
            nombre.set("")
        for fila in self.valor_entries:
            for entry in fila:
                entry.delete(0, tk.END)
        for widget in self.frame_datos_tab.winfo_children():
            widget.destroy()
        for widget in self.frame_resumen_tab.winfo_children():
            widget.destroy()
        for widget in self.frame_anova_tab.winfo_children():
            widget.destroy()
        self.text_interpretacion.delete("1.0", tk.END)

    def cargar_ejemplo(self):
        ejemplo = EXAMPLES_ANOVA_1[self.ejemplo_var.get()]
        grupos = ejemplo["grupos"]
        self.grupos_var.set(len(grupos))
        self.obs_var.set(max(len(grupo[1]) for grupo in grupos))
        self._crear_matriz_entrada()
        for indice, (nombre, valores) in enumerate(grupos):
            self.nombre_vars[indice].set(nombre)
            for fila, valor in enumerate(valores):
                self.valor_entries[fila][indice].delete(0, tk.END)
                self.valor_entries[fila][indice].insert(0, str(valor))

    def _leer_datos(self):
        grupos = []
        nombres = []
        for indice, nombre_var in enumerate(self.nombre_vars):
            nombre = nombre_var.get().strip() or f"Grupo {indice + 1}"
            valores = []
            for fila in self.valor_entries:
                texto = fila[indice].get().strip()
                if texto:
                    valores.append(float(texto.replace(",", ".")))
            if not valores:
                raise ValueError(f"El grupo '{nombre}' no tiene datos.")
            if len(valores) < 2:
                raise ValueError(f"El grupo '{nombre}' requiere al menos 2 observaciones.")
            nombres.append(nombre)
            grupos.append(valores)
        return nombres, grupos

    def calcular(self):
        try:
            nombres, grupos = self._leer_datos()
            alpha = float(self.alpha_var.get())
            self.resultado = anova_un_factor(grupos, nombres, alpha)
        except Exception as error:
            messagebox.showerror("Error en ANOVA", str(error))
            return

        for widget in self.frame_datos_tab.winfo_children():
            widget.destroy()
        for widget in self.frame_resumen_tab.winfo_children():
            widget.destroy()
        for widget in self.frame_anova_tab.winfo_children():
            widget.destroy()

        _crear_tabla_dataframe(self.frame_datos_tab, self.resultado["datos_largos"], titulo="Datos observados")
        _crear_tabla_dataframe(self.frame_resumen_tab, self.resultado["resumen"], titulo="Resumen por grupo")
        _crear_tabla_dataframe(self.frame_anova_tab, self.resultado["anova"], titulo="Tabla ANOVA")

        _limpiar_frame(self.frame_metricas)
        _crear_tarjetas_metricas(
            self.frame_metricas,
            [
                {
                    "titulo": "F calculada",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["f_calculada"]),
                    "detalle": "Estadistico central",
                    "bg": "#E3F2FD",
                    "fg_titulo": "#0D47A1",
                    "fg_valor": COLOR_PRIMARY,
                    "fg_detalle": "#1E3A5F",
                },
                {
                    "titulo": "F critica",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["f_critica"]),
                    "detalle": "Referencia de rechazo",
                    "bg": "#FFF8E1",
                    "fg_titulo": "#8A6D00",
                    "fg_valor": "#8A6D00",
                    "fg_detalle": "#6F5F20",
                },
                {
                    "titulo": "p-value",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["p_valor"]),
                    "detalle": "Probabilidad asociada",
                    "bg": "#FCE4EC",
                    "fg_titulo": "#AD1457",
                    "fg_valor": "#AD1457",
                    "fg_detalle": "#7A1740",
                },
                {
                    "titulo": "Decision",
                    "valor": "Rechaza H0" if "rechaza" in self.resultado["decision"].lower() else "No rechaza H0",
                    "detalle": "Conclusion resumida",
                    "bg": "#E8F5E9",
                    "fg_titulo": "#1B5E20",
                    "fg_valor": "#1B5E20",
                    "fg_detalle": "#2E7D32",
                },
            ],
        )

        self.text_interpretacion.delete("1.0", tk.END)
        self.text_interpretacion.insert(tk.END, self.resultado["interpretacion"])
        self.notebook.select(self.tab_anova)


class _AnovaDosFactoresTab:
    def __init__(self, parent, titulo, subtitulo, con_replicacion=False):
        self.parent = parent
        self.con_replicacion = con_replicacion
        self.frame = tk.Frame(parent, bg=BG_LIGHT)
        self.frame.pack(fill="both", expand=True)
        self.referencias = {}
        self._construir(titulo, subtitulo)

    def _construir(self, titulo, subtitulo):
        _crear_titulo(self.frame, titulo, subtitulo)

        panel_control = _crear_panel_seccion(
            self.frame,
            "Controles",
            "Selecciona el ejemplo y define filas, columnas y replicaciones si corresponde.",
            "#E8F5E9",
            COLOR_PRIMARY,
            "#1B5E20",
        )

        fila1 = tk.Frame(panel_control, bg=BG_WHITE)
        fila1.pack(fill="x", pady=4)
        tk.Label(fila1, text="Ejemplo:", bg=BG_WHITE).pack(side="left")
        if self.con_replicacion:
            self.ejemplo_var = tk.StringVar(value=list(EXAMPLES_ANOVA_2_REP.keys())[0])
            self.catalogo = EXAMPLES_ANOVA_2_REP
        else:
            self.ejemplo_var = tk.StringVar(value=list(EXAMPLES_ANOVA_2_NO_REP.keys())[0])
            self.catalogo = EXAMPLES_ANOVA_2_NO_REP
        ttk.Combobox(fila1, textvariable=self.ejemplo_var, values=list(self.catalogo.keys()), state="readonly", width=32).pack(side="left", padx=8)
        tk.Button(fila1, text="Cargar ejemplo", command=self.cargar_ejemplo, bg=COLOR_INFO, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)
        tk.Button(fila1, text="Limpiar", command=self.limpiar_datos, bg=COLOR_WARNING, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)

        fila2 = tk.Frame(panel_control, bg=BG_WHITE)
        fila2.pack(fill="x", pady=4)
        tk.Label(fila2, text="Filas:", bg=BG_WHITE).pack(side="left")
        self.filas_var = tk.IntVar(value=3)
        tk.Spinbox(fila2, from_=2, to=10, width=6, textvariable=self.filas_var).pack(side="left", padx=(6, 18))
        tk.Label(fila2, text="Columnas:", bg=BG_WHITE).pack(side="left")
        self.columnas_var = tk.IntVar(value=3)
        tk.Spinbox(fila2, from_=2, to=10, width=6, textvariable=self.columnas_var).pack(side="left", padx=(6, 18))
        if self.con_replicacion:
            tk.Label(fila2, text="Replicaciones por celda:", bg=BG_WHITE).pack(side="left")
            self.replicaciones_var = tk.IntVar(value=2)
            tk.Spinbox(fila2, from_=2, to=6, width=6, textvariable=self.replicaciones_var).pack(side="left", padx=(6, 18))
        self.alpha_var = tk.StringVar(value="0.05")
        tk.Label(fila2, text="Alpha:", bg=BG_WHITE).pack(side="left")
        ttk.Combobox(fila2, textvariable=self.alpha_var, values=["0.10", "0.05", "0.01"], state="readonly", width=10).pack(side="left", padx=8)
        tk.Button(fila2, text="Generar tabla", command=self.generar_tabla, bg=COLOR_SECONDARY, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=8)
        tk.Button(fila2, text="Calcular ANOVA", command=self.calcular, bg=COLOR_SUCCESS, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)

        self.frame_entrada = _crear_panel_seccion(
            self.frame,
            "Datos de entrada",
            "En sin replicacion, cada celda acepta un valor. En con replicacion, escribe valores separados por coma.",
            "#FFF8E1",
            COLOR_PRIMARY,
            "#8A6D00",
        )
        self._crear_matriz_entrada()

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True)
        self.tab_resumen = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.tab_anova = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.tab_interpretacion = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.notebook.add(self.tab_resumen, text="Resumen estadistico")
        self.notebook.add(self.tab_anova, text="Analisis de varianza")
        self.notebook.add(self.tab_interpretacion, text="Interpretacion")

        self.frame_resumen_tab = tk.Frame(self.tab_resumen, bg=BG_LIGHT)
        self.frame_resumen_tab.pack(fill="both", expand=True, padx=8, pady=8)
        self.frame_anova_tab = tk.Frame(self.tab_anova, bg=BG_LIGHT)
        self.frame_anova_tab.pack(fill="both", expand=True, padx=8, pady=8)
        self.frame_metricas = tk.Frame(self.tab_interpretacion, bg=BG_LIGHT)
        self.frame_metricas.pack(fill="x", padx=8, pady=(8, 0))
        self.text_interpretacion = scrolledtext.ScrolledText(self.tab_interpretacion, height=16, font=("Consolas", 10), bg=BG_WHITE)
        self.text_interpretacion.pack(fill="both", expand=True, padx=8, pady=8)

        self.cargar_ejemplo()

    def _crear_matriz_entrada(self):
        _limpiar_frame(self.frame_entrada)
        filas = int(self.filas_var.get())
        columnas = int(self.columnas_var.get())
        self.nombre_filas_vars = [tk.StringVar(value=f"Fila {i + 1}") for i in range(filas)]
        self.nombre_columnas_vars = [tk.StringVar(value=f"Columna {j + 1}") for j in range(columnas)]
        self.valor_entries = []

        top = tk.Frame(self.frame_entrada, bg=BG_WHITE)
        top.pack(fill="x")
        tk.Label(top, text="", bg=BG_WHITE, width=14).grid(row=0, column=0, padx=3, pady=3)
        for j, var in enumerate(self.nombre_columnas_vars, start=1):
            tk.Entry(top, textvariable=var, width=18, justify="center").grid(row=0, column=j, padx=3, pady=3)

        grid = tk.Frame(self.frame_entrada, bg=BG_WHITE)
        grid.pack(fill="x", pady=(8, 0))
        for i, fila_var in enumerate(self.nombre_filas_vars):
            tk.Entry(grid, textvariable=fila_var, width=16, justify="center").grid(row=i, column=0, padx=3, pady=3)
            fila_entries = []
            for j in range(columnas):
                if self.con_replicacion:
                    entry = tk.Entry(grid, width=18, justify="center")
                else:
                    entry = tk.Entry(grid, width=18, justify="center")
                entry.grid(row=i, column=j + 1, padx=3, pady=3)
                fila_entries.append(entry)
            self.valor_entries.append(fila_entries)

    def generar_tabla(self):
        self._crear_matriz_entrada()

    def limpiar_datos(self):
        for var in getattr(self, "nombre_filas_vars", []):
            var.set("")
        for var in getattr(self, "nombre_columnas_vars", []):
            var.set("")
        for fila in getattr(self, "valor_entries", []):
            for entry in fila:
                entry.delete(0, tk.END)
        for widget in self.frame_resumen_tab.winfo_children():
            widget.destroy()
        for widget in self.frame_anova_tab.winfo_children():
            widget.destroy()
        self.text_interpretacion.delete("1.0", tk.END)

    def cargar_ejemplo(self):
        ejemplo = self.catalogo[self.ejemplo_var.get()]
        self.filas_var.set(len(ejemplo["filas"]))
        self.columnas_var.set(len(ejemplo["columnas"]))
        if self.con_replicacion:
            self.replicaciones_var.set(len(ejemplo["cubo"][0][0]))
        self._crear_matriz_entrada()
        for i, nombre in enumerate(ejemplo["filas"]):
            self.nombre_filas_vars[i].set(nombre)
        for j, nombre in enumerate(ejemplo["columnas"]):
            self.nombre_columnas_vars[j].set(nombre)
        if self.con_replicacion:
            for i, fila in enumerate(ejemplo["cubo"]):
                for j, celda in enumerate(fila):
                    self.valor_entries[i][j].insert(0, ", ".join(str(valor) for valor in celda))
        else:
            for i, fila in enumerate(ejemplo["matriz"]):
                for j, valor in enumerate(fila):
                    self.valor_entries[i][j].insert(0, str(valor))

    def _leer_datos_sin_replicacion(self):
        matriz = []
        for i in range(len(self.nombre_filas_vars)):
            fila = []
            for j in range(len(self.nombre_columnas_vars)):
                texto = self.valor_entries[i][j].get().strip()
                if not texto:
                    raise ValueError("No deje celdas vacias en la matriz de ANOVA.")
                fila.append(float(texto.replace(",", ".")))
            matriz.append(fila)
        return matriz

    def _leer_datos_con_replicacion(self):
        cubo = []
        for i in range(len(self.nombre_filas_vars)):
            filas = []
            for j in range(len(self.nombre_columnas_vars)):
                texto = self.valor_entries[i][j].get().strip()
                valores = _parsear_lista_numeros(texto)
                if len(valores) < 2:
                    raise ValueError("Cada celda debe contener al menos dos replicaciones separadas por coma o espacio.")
                filas.append(valores)
            cubo.append(filas)

        replicaciones = {len(celda) for fila in cubo for celda in fila}
        if len(replicaciones) != 1:
            raise ValueError("Todas las celdas deben tener la misma cantidad de replicaciones.")
        return cubo

    def calcular(self):
        try:
            alpha = float(self.alpha_var.get())
            nombres_filas = [var.get().strip() or f"Fila {i + 1}" for i, var in enumerate(self.nombre_filas_vars)]
            nombres_columnas = [var.get().strip() or f"Columna {j + 1}" for j, var in enumerate(self.nombre_columnas_vars)]
            if self.con_replicacion:
                cubo = self._leer_datos_con_replicacion()
                self.resultado = anova_dos_factores_con_replicacion(cubo, nombres_filas, nombres_columnas, alpha=alpha)
            else:
                matriz = self._leer_datos_sin_replicacion()
                self.resultado = anova_dos_factores_sin_replicacion(matriz, nombres_filas, nombres_columnas, alpha=alpha)
        except Exception as error:
            messagebox.showerror("Error en ANOVA", str(error))
            return

        for widget in self.frame_resumen_tab.winfo_children():
            widget.destroy()
        for widget in self.frame_anova_tab.winfo_children():
            widget.destroy()

        if self.con_replicacion:
            _crear_tabla_dataframe(self.frame_resumen_tab, self.resultado["resumen"], titulo="Resumen por filas")
        else:
            resumen_filas = self.resultado["resumen_filas"]
            resumen_columnas = self.resultado["resumen_columnas"]
            _crear_tabla_dataframe(self.frame_resumen_tab, resumen_filas, titulo="Resumen por filas")
            _crear_tabla_dataframe(self.frame_resumen_tab, resumen_columnas, titulo="Resumen por columnas")

        _crear_tabla_dataframe(self.frame_anova_tab, self.resultado["anova"], titulo="Tabla ANOVA")
        _limpiar_frame(self.frame_metricas)
        if self.con_replicacion:
            tarjetas = [
                {
                    "titulo": "F Factor A",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["f_factor_a"]),
                    "detalle": "Efecto principal de A",
                    "bg": "#E3F2FD",
                    "fg_titulo": "#0D47A1",
                    "fg_valor": COLOR_PRIMARY,
                    "fg_detalle": "#1E3A5F",
                },
                {
                    "titulo": "F Factor B",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["f_factor_b"]),
                    "detalle": "Efecto principal de B",
                    "bg": "#FFF8E1",
                    "fg_titulo": "#8A6D00",
                    "fg_valor": "#8A6D00",
                    "fg_detalle": "#6F5F20",
                },
                {
                    "titulo": "F Interaccion",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["f_interaccion"]),
                    "detalle": "Efecto combinado A x B",
                    "bg": "#FCE4EC",
                    "fg_titulo": "#AD1457",
                    "fg_valor": "#AD1457",
                    "fg_detalle": "#7A1740",
                },
                {
                    "titulo": "Decision",
                    "valor": "Ver interpretacion",
                    "detalle": "Conclusiones abajo",
                    "bg": "#E8F5E9",
                    "fg_titulo": "#1B5E20",
                    "fg_valor": "#1B5E20",
                    "fg_detalle": "#2E7D32",
                },
            ]
        else:
            tarjetas = [
                {
                    "titulo": "F Filas",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["f_filas"]),
                    "detalle": "Efecto de filas",
                    "bg": "#E3F2FD",
                    "fg_titulo": "#0D47A1",
                    "fg_valor": COLOR_PRIMARY,
                    "fg_detalle": "#1E3A5F",
                },
                {
                    "titulo": "F Columnas",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["f_columnas"]),
                    "detalle": "Efecto de columnas",
                    "bg": "#FFF8E1",
                    "fg_titulo": "#8A6D00",
                    "fg_valor": "#8A6D00",
                    "fg_detalle": "#6F5F20",
                },
                {
                    "titulo": "Error",
                    "valor": _formatear_numero(self.resultado["estadisticos"]["cm_error"]),
                    "detalle": "Variacion residual",
                    "bg": "#FCE4EC",
                    "fg_titulo": "#AD1457",
                    "fg_valor": "#AD1457",
                    "fg_detalle": "#7A1740",
                },
                {
                    "titulo": "Decision",
                    "valor": "Ver interpretacion",
                    "detalle": "Conclusiones abajo",
                    "bg": "#E8F5E9",
                    "fg_titulo": "#1B5E20",
                    "fg_valor": "#1B5E20",
                    "fg_detalle": "#2E7D32",
                },
            ]
        _crear_tarjetas_metricas(self.frame_metricas, tarjetas)
        self.text_interpretacion.delete("1.0", tk.END)
        self.text_interpretacion.insert(tk.END, self.resultado["interpretacion"])
        self.notebook.select(self.tab_anova)


class VentanaAnova2Factores:
    def __init__(self, root):
        ventana = tk.Toplevel(root)
        self.ventana = ventana
        _configurar_ventana(ventana, "ANOVA de 2 Factores")
        _crear_barra_navegacion(
            ventana,
            "ANOVA de 2 Factores",
            volver_callback=lambda: _volver_a_menu_anova(root, ventana),
            volver_texto="← Menú ANOVA",
        )

        cont = tk.Frame(ventana, bg=BG_LIGHT)
        cont.pack(fill="both", expand=True, padx=10, pady=10)

        _crear_titulo(cont, "ANOVA de 2 Factores", "Incluye la variante sin replicacion y la variante con varias observaciones por celda.")

        notebook = ttk.Notebook(cont)
        notebook.pack(fill="both", expand=True)
        tab_sin = tk.Frame(notebook, bg=BG_LIGHT)
        tab_con = tk.Frame(notebook, bg=BG_LIGHT)
        notebook.add(tab_sin, text="Sin replicacion")
        notebook.add(tab_con, text="Con replicacion")

        self.vista_sin = _AnovaDosFactoresTab(
            tab_sin,
            "ANOVA de 2 Factores sin replicacion",
            "Cada celda tiene una sola observacion. El error se estima con el residuo de filas y columnas.",
            con_replicacion=False,
        )
        self.vista_con = _AnovaDosFactoresTab(
            tab_con,
            "ANOVA de 2 Factores con replicacion",
            "Cada celda contiene varias observaciones. Se calculan factor A, factor B, interaccion y error.",
            con_replicacion=True,
        )


class VentanaEjerciciosAnova:
    def __init__(self, root):
        ventana = tk.Toplevel(root)
        self.ventana = ventana
        _configurar_ventana(ventana, "Ejercicios ANOVA")
        _crear_barra_navegacion(
            ventana,
            "Ejercicios ANOVA",
            volver_callback=lambda: _volver_a_menu_anova(root, ventana),
            volver_texto="← Menú ANOVA",
        )

        cont = tk.Frame(ventana, bg=BG_LIGHT)
        cont.pack(fill="both", expand=True, padx=10, pady=10)

        _crear_titulo(cont, "Ejercicios ANOVA", "Casos precargados para resolver, comparar datos originales, procedimiento y resultado final.")

        self.notebook = ttk.Notebook(cont)
        self.notebook.pack(fill="both", expand=True)

        self.tab_1 = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.tab_2 = tk.Frame(self.notebook, bg=BG_LIGHT)
        self.notebook.add(self.tab_1, text="Ejercicios 1 factor")
        self.notebook.add(self.tab_2, text="Ejercicios 2 factores")

        self._crear_tab_ejercicios_1_factor()
        self._crear_tab_ejercicios_2_factores()

    def _crear_area_resultados(self, parent, incluir_resumen=True):
        marco = tk.Frame(parent, bg=BG_LIGHT)
        marco.pack(fill="both", expand=True)
        if incluir_resumen:
            frame_resumen = tk.Frame(marco, bg=BG_LIGHT)
            frame_resumen.pack(fill="both", expand=True)
        else:
            frame_resumen = None
        frame_anova = tk.Frame(marco, bg=BG_LIGHT)
        frame_anova.pack(fill="both", expand=True, pady=(8, 0))
        texto = scrolledtext.ScrolledText(marco, height=10, font=("Consolas", 10), bg=BG_WHITE)
        texto.pack(fill="both", expand=True, pady=(8, 0))
        return frame_resumen, frame_anova, texto

    def _crear_tab_ejercicios_1_factor(self):
        frame = tk.Frame(self.tab_1, bg=BG_LIGHT)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        control = _crear_panel_seccion(
            frame,
            "Selector de ejercicio",
            "Elige el ejercicio precargado y luego presiona Resolver.",
            "#E8F5E9",
            COLOR_PRIMARY,
            "#1B5E20",
        )
        self.ej_1_var = tk.StringVar(value=EXERCISES_ANOVA[0]["titulo"])
        opciones = [ej["titulo"] for ej in EXERCISES_ANOVA if ej["tipo"] == "1 factor"]
        ttk.Combobox(control, textvariable=self.ej_1_var, values=opciones, state="readonly", width=42).pack(side="left", padx=(0, 8))
        tk.Button(control, text="Cargar ejemplo", command=self.cargar_ejercicio_1, bg=COLOR_INFO, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)
        tk.Button(control, text="Resolver", command=self.resolver_ejercicio_1, bg=COLOR_SUCCESS, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)

        self.texto_datos_1 = scrolledtext.ScrolledText(frame, height=10, font=("Consolas", 10), bg=BG_WHITE)
        self.texto_datos_1.pack(fill="x", pady=(0, 8))
        self.texto_datos_1.insert(tk.END, "Seleccione un ejercicio y pulse Cargar ejemplo.")

        self.frame_resumen_1 = tk.Frame(frame, bg=BG_LIGHT)
        self.frame_resumen_1.pack(fill="both", expand=True)
        self.frame_anova_1 = tk.Frame(frame, bg=BG_LIGHT)
        self.frame_anova_1.pack(fill="both", expand=True, pady=(8, 0))
        self.frame_metricas_1 = tk.Frame(frame, bg=BG_LIGHT)
        self.frame_metricas_1.pack(fill="x", pady=(8, 0))
        self.texto_resultado_1 = scrolledtext.ScrolledText(frame, height=9, font=("Consolas", 10), bg=BG_WHITE)
        self.texto_resultado_1.pack(fill="both", expand=True, pady=(8, 0))

        self.ejercicio_1_actual = None
        self.cargar_ejercicio_1()

    def _crear_tab_ejercicios_2_factores(self):
        frame = tk.Frame(self.tab_2, bg=BG_LIGHT)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        control = _crear_panel_seccion(
            frame,
            "Selector de ejercicio",
            "Elige el ejercicio precargado y luego presiona Resolver.",
            "#E8F5E9",
            COLOR_PRIMARY,
            "#1B5E20",
        )
        self.ej_2_var = tk.StringVar(value=EXERCISES_ANOVA[2]["titulo"])
        opciones = [ej["titulo"] for ej in EXERCISES_ANOVA if ej["tipo"] != "1 factor"]
        ttk.Combobox(control, textvariable=self.ej_2_var, values=opciones, state="readonly", width=42).pack(side="left", padx=(0, 8))
        tk.Button(control, text="Cargar ejemplo", command=self.cargar_ejercicio_2, bg=COLOR_INFO, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)
        tk.Button(control, text="Resolver", command=self.resolver_ejercicio_2, bg=COLOR_SUCCESS, fg="#000000", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=6).pack(side="left", padx=4)

        self.texto_datos_2 = scrolledtext.ScrolledText(frame, height=10, font=("Consolas", 10), bg=BG_WHITE)
        self.texto_datos_2.pack(fill="x", pady=(0, 8))
        self.texto_datos_2.insert(tk.END, "Seleccione un ejercicio y pulse Cargar ejemplo.")

        self.frame_resumen_2 = tk.Frame(frame, bg=BG_LIGHT)
        self.frame_resumen_2.pack(fill="both", expand=True)
        self.frame_anova_2 = tk.Frame(frame, bg=BG_LIGHT)
        self.frame_anova_2.pack(fill="both", expand=True, pady=(8, 0))
        self.frame_metricas_2 = tk.Frame(frame, bg=BG_LIGHT)
        self.frame_metricas_2.pack(fill="x", pady=(8, 0))
        self.texto_resultado_2 = scrolledtext.ScrolledText(frame, height=9, font=("Consolas", 10), bg=BG_WHITE)
        self.texto_resultado_2.pack(fill="both", expand=True, pady=(8, 0))

        self.ejercicio_2_actual = None
        self.cargar_ejercicio_2()

    def _buscar_ejercicio(self, titulo):
        for ejercicio in EXERCISES_ANOVA:
            if ejercicio["titulo"] == titulo:
                return ejercicio
        raise ValueError("Ejercicio no encontrado.")

    def cargar_ejercicio_1(self):
        self.ejercicio_1_actual = self._buscar_ejercicio(self.ej_1_var.get())
        ejercicio = self.ejercicio_1_actual
        grupos = ejercicio["datos"]["grupos"]
        lineas = [f"{ejercicio['titulo']}", "", f"Procedimiento: {ejercicio['procedimiento']}", "", "Datos originales:"]
        for nombre, valores in grupos:
            lineas.append(f"- {nombre}: {', '.join(str(v) for v in valores)}")
        self.texto_datos_1.delete("1.0", tk.END)
        self.texto_datos_1.insert(tk.END, "\n".join(lineas))

    def resolver_ejercicio_1(self):
        self.cargar_ejercicio_1()
        ejercicio = self.ejercicio_1_actual
        grupos = [valores for _, valores in ejercicio["datos"]["grupos"]]
        nombres = [nombre for nombre, _ in ejercicio["datos"]["grupos"]]
        resultado = anova_un_factor(grupos, nombres)

        for widget in self.frame_resumen_1.winfo_children():
            widget.destroy()
        for widget in self.frame_anova_1.winfo_children():
            widget.destroy()
        _crear_tabla_dataframe(self.frame_resumen_1, resultado["resumen"], titulo="Resumen estadistico")
        _crear_tabla_dataframe(self.frame_anova_1, resultado["anova"], titulo="Tabla ANOVA")
        _limpiar_frame(self.frame_metricas_1)
        _crear_tarjetas_metricas(
            self.frame_metricas_1,
            [
                {
                    "titulo": "F calculada",
                    "valor": _formatear_numero(resultado["estadisticos"]["f_calculada"]),
                    "detalle": "Estadistico central",
                    "bg": "#E3F2FD",
                    "fg_titulo": "#0D47A1",
                    "fg_valor": COLOR_PRIMARY,
                    "fg_detalle": "#1E3A5F",
                },
                {
                    "titulo": "F critica",
                    "valor": _formatear_numero(resultado["estadisticos"]["f_critica"]),
                    "detalle": "Referencia de rechazo",
                    "bg": "#FFF8E1",
                    "fg_titulo": "#8A6D00",
                    "fg_valor": "#8A6D00",
                    "fg_detalle": "#6F5F20",
                },
                {
                    "titulo": "p-value",
                    "valor": _formatear_numero(resultado["estadisticos"]["p_valor"]),
                    "detalle": "Probabilidad asociada",
                    "bg": "#FCE4EC",
                    "fg_titulo": "#AD1457",
                    "fg_valor": "#AD1457",
                    "fg_detalle": "#7A1740",
                },
            ],
        )
        self.texto_resultado_1.delete("1.0", tk.END)
        self.texto_resultado_1.insert(tk.END, f"{resultado['conclusion']}\n\n{resultado['interpretacion']}")

    def cargar_ejercicio_2(self):
        self.ejercicio_2_actual = self._buscar_ejercicio(self.ej_2_var.get())
        ejercicio = self.ejercicio_2_actual
        datos = ejercicio["datos"]
        lineas = [f"{ejercicio['titulo']}", "", f"Procedimiento: {ejercicio['procedimiento']}", "", "Datos originales:"]
        if "matriz" in datos:
            matriz = np.array(datos["matriz"], dtype=float)
            for nombre_fila, fila in zip(datos["filas"], matriz):
                valores = ", ".join(str(valor) for valor in fila)
                lineas.append(f"- {nombre_fila}: {valores}")
        else:
            for i, fila in enumerate(datos["cubo"], start=1):
                lineas.append(f"Fila {i}: {fila}")
        self.texto_datos_2.delete("1.0", tk.END)
        self.texto_datos_2.insert(tk.END, "\n".join(lineas))

    def resolver_ejercicio_2(self):
        self.cargar_ejercicio_2()
        ejercicio = self.ejercicio_2_actual
        datos = ejercicio["datos"]

        if "matriz" in datos:
            resultado = anova_dos_factores_sin_replicacion(datos["matriz"], datos["filas"], datos["columnas"])
            resumenes = [resultado["resumen_filas"], resultado["resumen_columnas"]]
            titulo_resumen = ["Resumen por filas", "Resumen por columnas"]
        else:
            resultado = anova_dos_factores_con_replicacion(datos["cubo"], datos["filas"], datos["columnas"])
            resumenes = [resultado["resumen"]]
            titulo_resumen = ["Resumen"]

        for widget in self.frame_resumen_2.winfo_children():
            widget.destroy()
        for widget in self.frame_anova_2.winfo_children():
            widget.destroy()

        for tabla, titulo in zip(resumenes, titulo_resumen):
            _crear_tabla_dataframe(self.frame_resumen_2, tabla, titulo=titulo)
        _crear_tabla_dataframe(self.frame_anova_2, resultado["anova"], titulo="Tabla ANOVA")
        _limpiar_frame(self.frame_metricas_2)
        tarjetas = [
            {
                "titulo": "Factor A",
                "valor": _formatear_numero(resultado["estadisticos"]["f_factor_a"]),
                "detalle": "Efecto principal A",
                "bg": "#E3F2FD",
                "fg_titulo": "#0D47A1",
                "fg_valor": COLOR_PRIMARY,
                "fg_detalle": "#1E3A5F",
            },
            {
                "titulo": "Factor B",
                "valor": _formatear_numero(resultado["estadisticos"]["f_factor_b"]),
                "detalle": "Efecto principal B",
                "bg": "#FFF8E1",
                "fg_titulo": "#8A6D00",
                "fg_valor": "#8A6D00",
                "fg_detalle": "#6F5F20",
            },
            {
                "titulo": "Interaccion",
                "valor": _formatear_numero(resultado["estadisticos"]["f_interaccion"]),
                "detalle": "Efecto combinado",
                "bg": "#FCE4EC",
                "fg_titulo": "#AD1457",
                "fg_valor": "#AD1457",
                "fg_detalle": "#7A1740",
            },
        ]
        _crear_tarjetas_metricas(self.frame_metricas_2, tarjetas)
        self.texto_resultado_2.delete("1.0", tk.END)
        self.texto_resultado_2.insert(tk.END, f"{resultado['conclusion']}\n\n{resultado['interpretacion']}")


def abrir_modulo_anova_1_factor(root):
    VentanaAnova1Factor(root)


def abrir_modulo_anova_2_factores(root):
    VentanaAnova2Factores(root)


def abrir_modulo_ejercicios_anova(root):
    VentanaEjerciciosAnova(root)


class VentanaMenuAnova:
    def __init__(self, root):
        self.root = root
        self.ventana = tk.Toplevel(root)
        _configurar_ventana(self.ventana, "Menu ANOVA")
        self._construir()

    def _construir(self):
        barra = tk.Frame(self.ventana, bg=COLOR_PRIMARY, height=64)
        barra.pack(fill="x", side="top")

        tk.Button(
            barra,
            text="← Estadistica II",
            command=self.ventana.destroy,
            bg=COLOR_INFO,
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="left", padx=14, pady=10)

        tk.Label(
            barra,
            text="ANOVA",
            font=("Helvetica", 15, "bold"),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT,
        ).pack(side="left", padx=6)

        tk.Button(
            barra,
            text="Cerrar",
            command=self.ventana.destroy,
            bg=COLOR_DANGER,
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="right", padx=14, pady=10)

        cont = tk.Frame(self.ventana, bg=BG_LIGHT)
        cont.pack(fill="both", expand=True, padx=20, pady=18)

        _crear_titulo(cont, "ANOVA", "Selecciona el tipo de analisis que deseas abrir.")

        frame_cards = tk.Frame(cont, bg=BG_LIGHT)
        frame_cards.pack(fill="both", expand=True)

        self._crear_card(
            frame_cards,
            "📊 ANOVA de 1 Factor",
            "Comparacion de medias entre varios grupos con tabla ANOVA y conclusion academica.",
            lambda: abrir_modulo_anova_1_factor(self.root),
            "#E3F2FD",
            "#0D47A1",
            "#1565C0",
        )

        self._crear_card(
            frame_cards,
            "📊 ANOVA de 2 Factores",
            "Incluye variante sin replicacion y con varias observaciones por celda.",
            lambda: abrir_modulo_anova_2_factores(self.root),
            "#FFF8E1",
            "#F57F17",
            "#E65100",
        )

        self._crear_card(
            frame_cards,
            "🧪 Ejercicios ANOVA",
            "Casos precargados con procedimiento, resultados y tabla completa.",
            lambda: abrir_modulo_ejercicios_anova(self.root),
            "#FCE4EC",
            "#880E4F",
            "#AD1457",
        )

    def _crear_card(self, parent, titulo, descripcion, comando, bg, fg_titulo, fg_desc):
        card = tk.Frame(parent, bg=bg, relief="solid", borderwidth=2)
        card.pack(fill="x", padx=20, pady=10)

        tk.Label(card, text=titulo, font=("Helvetica", 16, "bold"), bg=bg, fg=fg_titulo).pack(pady=(18, 8))
        tk.Label(card, text=descripcion, font=("Helvetica", 11), bg=bg, fg=fg_desc, justify="center", wraplength=1000).pack(pady=(0, 12))
        tk.Button(
            card,
            text="Abrir modulo",
            command=comando,
            bg=COLOR_SECONDARY,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(pady=(0, 18))


def abrir_modulo_anova_menu(root):
    VentanaMenuAnova(root)
