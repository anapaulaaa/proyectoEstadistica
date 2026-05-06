"""Ventana dedicada a calculadoras de intervalos de confianza."""

import math
import re
import tkinter as tk
from statistics import mean, stdev
from tkinter import ttk

from scipy import stats

from config_interfaz import *


def _centrar_ventana(ventana, proporcion_w=0.9, proporcion_h=0.88):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    window_width = int(screen_width * proporcion_w)
    window_height = int(screen_height * proporcion_h)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")


def _normalizar_confianza(nivel_confianza):
    valor = float(str(nivel_confianza).strip().replace("%", ""))
    if valor <= 0:
        raise ValueError("El nivel de confianza debe ser mayor que 0.")
    if valor < 1:
        valor *= 100
    if valor >= 100:
        raise ValueError("El nivel de confianza debe ser menor que 100%.")
    return valor / 100


def _parse_float(texto):
    texto = str(texto).strip().replace(",", ".")
    if not texto:
        return None
    return float(texto)


def _fmt_numero(valor, decimales=4):
    return f"{valor:.{decimales}f}"


def _fmt_confianza(valor_normalizado):
    return f"{valor_normalizado * 100:.2f}%"


def _siguiente_fila_grid(frame):
    filas = []
    for widget in frame.grid_slaves():
        info = widget.grid_info()
        fila = info.get("row")
        if fila is not None:
            filas.append(int(fila))
    return (max(filas) + 1) if filas else 0


class VentanaIntervalosConfianza:
    """Crea la sección completa de intervalos de confianza."""

    def __init__(self, root):
        self.root = root
        self.indice_actual = 0
        self.precision_var = tk.StringVar(value="4")
        self.ventana = tk.Toplevel(root)
        self.ventana.title("📏 Intervalos de Confianza")
        _centrar_ventana(self.ventana, 0.96, 0.92)
        try:
            self.ventana.state("zoomed")
        except Exception:
            pass
        self.ventana.configure(bg=BG_LIGHT)
        self.ventana.minsize(1050, 700)

        encabezado = tk.Frame(self.ventana, bg=BG_LIGHT)
        encabezado.pack(fill="x", padx=18, pady=(14, 8))

        tk.Label(
            encabezado,
            text="📏 Intervalos de Confianza",
            font=("Helvetica", 18, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            encabezado,
            text="Cada calculadora recalcula al instante. Las entradas están a la izquierda y las salidas a la derecha.",
            font=("Helvetica", 10),
            bg=BG_LIGHT,
            fg=TEXT_MUTED,
        ).pack(anchor="w", pady=(4, 0))

        control = tk.Frame(self.ventana, bg=BG_LIGHT)
        control.pack(fill="x", padx=18, pady=(0, 8))
        tk.Label(control, text="Decimales de salida:", bg=BG_LIGHT, fg=TEXT_DARK, font=("Helvetica", 10, "bold")).pack(side="left")
        ttk.Combobox(control, textvariable=self.precision_var, state="readonly", width=8, values=["4", "2"]).pack(side="left", padx=8)
        tk.Label(control, text="(internamente calcula con mayor precisión)", bg=BG_LIGHT, fg=TEXT_MUTED, font=("Helvetica", 9, "italic")).pack(side="left")

        cuerpo = tk.Frame(self.ventana, bg=BG_LIGHT)
        cuerpo.pack(fill="both", expand=True, padx=12, pady=10)
        cuerpo.columnconfigure(0, weight=0)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        self.frame_menu = tk.LabelFrame(
            cuerpo,
            text="Menú de Calculadoras",
            bg="#ECEFF1",
            font=("Helvetica", 11, "bold"),
            padx=8,
            pady=8,
        )
        self.frame_menu.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        panel_derecho = tk.Frame(cuerpo, bg=BG_LIGHT)
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(panel_derecho, bg=BG_LIGHT, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(panel_derecho, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.panel_calculadora = tk.Frame(self.canvas, bg=BG_LIGHT)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.panel_calculadora, anchor="nw")

        self.panel_calculadora.bind("<Configure>", lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._ajustar_ancho_canvas)

        # Menu centralizado para facilitar agregar/quitar calculadoras.
        self.catalogo_calculadoras = [
            ("IC 1", "IC Media con σ conocida", self._crear_calculadora_1),
            ("IC 2", "IC Media σ desconocida, n ≥ 30", self._crear_calculadora_2),
            ("IC 3", "IC Media σ desconocida, n < 30", self._crear_calculadora_3),
            ("IC 4", "IC Proporción", self._crear_calculadora_4),
            ("IC 5", "IC Varianza (χ²)", self._crear_calculadora_5),
            ("IC 6", "Dif. medias varianzas conocidas", self._crear_calculadora_6),
            ("IC 7", "Dif. medias varianzas iguales", self._crear_calculadora_7),
            ("IC 8", "Dif. medias Welch", self._crear_calculadora_8),
            ("IC 9", "Dif. medias n1,n2 ≥ 30", self._crear_calculadora_9),
            ("IC 10", "Dif. medias pareadas", self._crear_calculadora_10),
        ]

        self.botones_menu = []
        for indice, (codigo, nombre, _) in enumerate(self.catalogo_calculadoras):
            boton = tk.Button(
                self.frame_menu,
                text=f"{codigo} - {nombre}",
                anchor="w",
                justify="left",
                wraplength=250,
                width=34,
                command=lambda i=indice: self._mostrar_calculadora(i),
                bg="#CFD8DC",
                fg="#102027",
                activebackground="#B0BEC5",
                activeforeground="#000000",
                relief="flat",
                cursor="hand2",
                padx=8,
                pady=7,
                font=("Helvetica", 10, "bold"),
            )
            boton.pack(fill="x", pady=3)
            self.botones_menu.append(boton)

        self.precision_var.trace_add("write", lambda *_: self._mostrar_calculadora(self.indice_actual))

        self._mostrar_calculadora(0)

    def _ajustar_ancho_canvas(self, event):
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def _mostrar_calculadora(self, indice):
        self.indice_actual = indice
        for widget in self.panel_calculadora.winfo_children():
            widget.destroy()

        for idx, boton in enumerate(self.botones_menu):
            if idx == indice:
                boton.configure(bg="#90A4AE", fg="#000000")
            else:
                boton.configure(bg="#CFD8DC", fg="#102027")

        _, _, constructor = self.catalogo_calculadoras[indice]
        constructor()
        self.canvas.yview_moveto(0)

    def _decimales_actuales(self):
        try:
            return int(self.precision_var.get())
        except Exception:
            return 4

    def _crear_pestana_base(self, titulo_tab, titulo, nota, formula_texto):
        contenedor = tk.Frame(self.panel_calculadora, bg=BG_LIGHT)
        contenedor.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(
            contenedor,
            text=titulo,
            font=("Helvetica", 16, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            contenedor,
            text=nota,
            font=("Helvetica", 10, "italic"),
            bg=BG_LIGHT,
            fg="#8A5A00",
            justify="left",
            wraplength=1100,
        ).pack(anchor="w", pady=(4, 10))

        frame_formula = tk.LabelFrame(
            contenedor,
            text="Fórmulas",
            bg="#FFF8E1",
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=8,
        )
        frame_formula.pack(fill="x", pady=(0, 10))

        tk.Label(
            frame_formula,
            text=formula_texto,
            justify="left",
            anchor="w",
            bg="#FFF8E1",
            fg="#37474F",
            font=("Consolas", 10),
            wraplength=1080,
        ).pack(fill="x")

        frame_general = tk.Frame(contenedor, bg=BG_LIGHT)
        frame_general.pack(fill="both", expand=True)
        frame_general.columnconfigure(0, weight=1)
        frame_general.columnconfigure(1, weight=1)

        frame_entradas = tk.LabelFrame(
            frame_general,
            text="Entradas",
            bg="#E8F5E9",
            font=("Helvetica", 11, "bold"),
            padx=12,
            pady=10,
        )
        frame_entradas.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        frame_salidas = tk.LabelFrame(
            frame_general,
            text="Salidas",
            bg="#E3F2FD",
            font=("Helvetica", 11, "bold"),
            padx=12,
            pady=10,
        )
        frame_salidas.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        return contenedor, frame_entradas, frame_salidas

    def _crear_campos(self, frame, campos):
        variables = {}
        for indice, campo in enumerate(campos):
            fila = indice // 2
            columna = (indice % 2) * 2
            tk.Label(
                frame,
                text=campo["etiqueta"],
                bg=frame.cget("bg"),
                font=("Helvetica", 10, "bold"),
            ).grid(row=fila, column=columna, sticky="w", pady=5, padx=(0, 6))

            variable = tk.StringVar(value=str(campo.get("default", "")))
            tk.Entry(frame, textvariable=variable, width=26).grid(
                row=fila,
                column=columna + 1,
                sticky="w",
                pady=5,
                padx=(0, 12),
            )
            variables[campo["nombre"]] = variable

        return variables

    def _crear_salidas(self, frame, salidas):
        variables = {}
        for indice, salida in enumerate(salidas):
            fila = indice // 2
            columna = (indice % 2) * 2
            tk.Label(
                frame,
                text=salida["etiqueta"],
                bg=frame.cget("bg"),
                font=("Helvetica", 10, "bold"),
            ).grid(row=fila, column=columna, sticky="w", pady=5, padx=(0, 6))

            variable = tk.StringVar(value="-")
            tk.Label(
                frame,
                textvariable=variable,
                bg="white",
                fg=COLOR_PRIMARY,
                font=("Consolas", 10, "bold"),
                anchor="w",
                relief="solid",
                borderwidth=1,
                padx=8,
                pady=4,
                width=24,
            ).grid(row=fila, column=columna + 1, sticky="we", pady=5, padx=(0, 12))
            variables[salida["nombre"]] = variable

        return variables

    def _crear_resultado_final(self, frame):
        fila_base = _siguiente_fila_grid(frame)
        caja = tk.LabelFrame(
            frame,
            text="Resultado final",
            bg="#FFF3E0",
            font=("Helvetica", 12, "bold"),
            padx=12,
            pady=10,
        )
        caja.grid(row=fila_base, column=0, columnspan=4, sticky="we", pady=(10, 6))

        fila = tk.Frame(caja, bg="#FFF3E0")
        fila.pack(fill="x")

        li_var = tk.StringVar(value="-")
        ls_var = tk.StringVar(value="-")

        tk.Label(fila, text="LI", bg="#FFF3E0", fg="#B71C1C", font=("Helvetica", 12, "bold")).pack(side="left")
        tk.Label(
            fila,
            textvariable=li_var,
            bg="#FFEBEE",
            fg="#B71C1C",
            font=("Consolas", 13, "bold"),
            relief="solid",
            borderwidth=1,
            padx=16,
            pady=6,
        ).pack(side="left", padx=(8, 18))

        tk.Label(fila, text="LS", bg="#FFF3E0", fg="#0D47A1", font=("Helvetica", 12, "bold")).pack(side="left")
        tk.Label(
            fila,
            textvariable=ls_var,
            bg="#E3F2FD",
            fg="#0D47A1",
            font=("Consolas", 13, "bold"),
            relief="solid",
            borderwidth=1,
            padx=16,
            pady=6,
        ).pack(side="left", padx=(8, 0))

        return li_var, ls_var

    def _crear_conclusion_y_estado(self, frame):
        fila_base = _siguiente_fila_grid(frame)
        conclusion_var = tk.StringVar(value="Complete las entradas para ver la conclusión automática.")
        estado_var = tk.StringVar(value="")

        tk.Label(
            frame,
            text="Conclusión",
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY,
            font=("Helvetica", 11, "bold"),
        ).grid(row=fila_base, column=0, columnspan=4, sticky="w", pady=(8, 2))
        tk.Label(
            frame,
            textvariable=conclusion_var,
            bg="#F3E5F5",
            fg="#4A148C",
            font=("Helvetica", 10, "bold"),
            justify="left",
            wraplength=1100,
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=8,
        ).grid(row=fila_base + 1, column=0, columnspan=4, sticky="we")
        tk.Label(
            frame,
            textvariable=estado_var,
            bg=BG_LIGHT,
            fg="#C62828",
            font=("Helvetica", 9, "italic"),
            justify="left",
            wraplength=1100,
        ).grid(row=fila_base + 2, column=0, columnspan=4, sticky="w", pady=(6, 0))

        return conclusion_var, estado_var

    def _bind_recalculo(self, variables, callback):
        for variable in variables:
            variable.trace_add("write", lambda *_: callback())

    def _leer_float(self, variable):
        return _parse_float(variable.get())

    def _limpiar_salida(self, salida_vars, li_var=None, ls_var=None, conclusion_var=None, estado_var=None):
        for variable in salida_vars.values():
            variable.set("-")
        if li_var is not None:
            li_var.set("-")
        if ls_var is not None:
            ls_var.set("-")
        if conclusion_var is not None:
            conclusion_var.set("Complete las entradas para ver la conclusión automática.")
        if estado_var is not None:
            estado_var.set("")

    def _crear_calculadora_estandar(self, titulo_tab, titulo, nota, formula_texto, campos, salidas, calcular_fn):
        contenedor, frame_entradas, frame_salidas = self._crear_pestana_base(titulo_tab, titulo, nota, formula_texto)
        entradas = self._crear_campos(frame_entradas, campos)
        salida_vars = self._crear_salidas(frame_salidas, salidas)
        li_var, ls_var = self._crear_resultado_final(frame_salidas)
        conclusion_var, estado_var = self._crear_conclusion_y_estado(frame_salidas)
        decimales = self._decimales_actuales()

        def recalcular():
            try:
                valores = {}
                for nombre, variable in entradas.items():
                    valor = self._leer_float(variable)
                    if valor is None:
                        self._limpiar_salida(salida_vars, li_var, ls_var, conclusion_var, estado_var)
                        return
                    valores[nombre] = valor

                resultado = calcular_fn(valores)
                for salida in salidas:
                    nombre = salida["nombre"]
                    if nombre in resultado:
                        salida_vars[nombre].set(_fmt_numero(resultado[nombre], decimales))

                li_var.set(_fmt_numero(resultado["li"], decimales))
                ls_var.set(_fmt_numero(resultado["ls"], decimales))
                conclusion_var.set(resultado["conclusion"])
                estado_var.set(resultado.get("estado", ""))
            except Exception as exc:
                self._limpiar_salida(salida_vars, li_var, ls_var, conclusion_var, estado_var)
                estado_var.set(str(exc))

        def limpiar():
            for variable in entradas.values():
                variable.set("")
            self._limpiar_salida(salida_vars, li_var, ls_var, conclusion_var, estado_var)

        self._bind_recalculo(entradas.values(), recalcular)
        botones = tk.Frame(frame_entradas, bg="#E8F5E9")
        botones.grid(row=_siguiente_fila_grid(frame_entradas), column=0, columnspan=4, sticky="w", pady=(10, 0))

        tk.Button(
            botones,
            text="📊 Calcular",
            command=recalcular,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=8,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botones,
            text="🧹 Limpiar",
            command=limpiar,
            bg=COLOR_WARNING,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=8,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="left")

        recalcular()

    def _crear_calculadora_1(self):
        self._crear_calculadora_estandar(
            "IC 1",
            "Calculadora 1 - IC Media con σ conocida",
            "Usar cuando se conoce la desviación poblacional σ.",
            "α = 1 - NC | α/2 = α / 2 | Z(α/2) = valor crítico de la normal estándar | SE = σ / √n | E = Z × SE | LI = x̄ - E | LS = x̄ + E",
            [
                {"nombre": "n", "etiqueta": "n", "default": "30"},
                {"nombre": "media", "etiqueta": "x̄", "default": "50"},
                {"nombre": "sigma", "etiqueta": "σ poblacional", "default": "10"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "alpha", "etiqueta": "α", "decimales": 4},
                {"nombre": "alpha_2", "etiqueta": "α/2", "decimales": 4},
                {"nombre": "z", "etiqueta": "Z(α/2)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            lambda v: self._calc_ic_media_sigma_conocida(v),
        )

    def _calc_ic_media_sigma_conocida(self, valores):
        n = valores["n"]
        media = valores["media"]
        sigma = valores["sigma"]
        nc = _normalizar_confianza(valores["nc"])
        if n <= 0 or sigma < 0:
            raise ValueError("n debe ser mayor que 0 y σ no puede ser negativa.")
        alpha = 1 - nc
        alpha_2 = alpha / 2
        z = stats.norm.ppf(1 - alpha_2)
        se = sigma / math.sqrt(n)
        e = z * se
        li = media - e
        ls = media + e
        return {
            "alpha": alpha,
            "alpha_2": alpha_2,
            "z": z,
            "se": se,
            "e": e,
            "li": li,
            "ls": ls,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, μ se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_2(self):
        self._crear_calculadora_estandar(
            "IC 2",
            "Calculadora 2 - IC Media, σ desconocida, n ≥ 30",
            "Si n < 30, usar la Calculadora 3.",
            "α = 1 - NC | df = n - 1 | t(α/2, df) = valor crítico t-Student | SE = s / √n | E = t × SE | LI = x̄ - E | LS = x̄ + E",
            [
                {"nombre": "n", "etiqueta": "n", "default": "30"},
                {"nombre": "media", "etiqueta": "x̄", "default": "50"},
                {"nombre": "s", "etiqueta": "s", "default": "10"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "alpha", "etiqueta": "α", "decimales": 4},
                {"nombre": "df", "etiqueta": "df", "decimales": 0},
                {"nombre": "t", "etiqueta": "t(α/2, df)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            lambda v: self._calc_ic_media_t(v, nota="Nota: Si n < 30, use la Calculadora 3.", mostrar_si_n_menor_30=True),
        )

    def _crear_calculadora_3(self):
        self._crear_calculadora_estandar(
            "IC 3",
            "Calculadora 3 - IC Media, σ desconocida, n < 30",
            "Caso exclusivo para n < 30. No usar Z.",
            "α = 1 - NC | df = n - 1 | t(α/2, df) = valor crítico t-Student | SE = s / √n | E = t × SE | LI = x̄ - E | LS = x̄ + E",
            [
                {"nombre": "n", "etiqueta": "n", "default": "12"},
                {"nombre": "media", "etiqueta": "x̄", "default": "50"},
                {"nombre": "s", "etiqueta": "s", "default": "10"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "alpha", "etiqueta": "α", "decimales": 4},
                {"nombre": "df", "etiqueta": "df", "decimales": 0},
                {"nombre": "t", "etiqueta": "t(α/2, df)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            lambda v: self._calc_ic_media_t(v, nota="Nota: Este caso es exclusivo para n < 30. No usar Z.", mostrar_siempre=True),
        )

    def _calc_ic_media_t(self, valores, nota, mostrar_siempre=False, mostrar_si_n_menor_30=False):
        n = valores["n"]
        media = valores["media"]
        s = valores["s"]
        nc = _normalizar_confianza(valores["nc"])
        if n <= 1 or s < 0:
            raise ValueError("n debe ser mayor que 1 y s no puede ser negativa.")
        if mostrar_siempre:
            estado = nota
        elif mostrar_si_n_menor_30:
            estado = nota if n < 30 else ""
        else:
            estado = nota if n >= 30 else ""
        alpha = 1 - nc
        df = n - 1
        t_crit = stats.t.ppf(1 - alpha / 2, df)
        se = s / math.sqrt(n)
        e = t_crit * se
        li = media - e
        ls = media + e
        return {
            "alpha": alpha,
            "df": df,
            "t": t_crit,
            "se": se,
            "e": e,
            "li": li,
            "ls": ls,
            "estado": estado,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, μ se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_4(self):
        self._crear_calculadora_estandar(
            "IC 4",
            "Calculadora 4 - IC Proporción",
            "La entrada Proporción muestral (p) debe estar entre 0 y 1, por ejemplo 0.35.",
            "α = 1 - NC | α/2 = α / 2 | Z(α/2) = valor crítico normal | q = 1 - p | SE = √(p × q / n) | E = Z × SE | LI = p - E | LS = p + E",
            [
                {"nombre": "n", "etiqueta": "n", "default": "100"},
                {"nombre": "p_hat", "etiqueta": "Proporción muestral (p)", "default": "0.35"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "q_hat", "etiqueta": "Complemento (q)", "decimales": 4},
                {"nombre": "alpha", "etiqueta": "α", "decimales": 4},
                {"nombre": "alpha_2", "etiqueta": "α/2", "decimales": 4},
                {"nombre": "z", "etiqueta": "Z(α/2)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            self._calc_ic_proporcion,
        )

    def _calc_ic_proporcion(self, valores):
        n = valores["n"]
        p_hat = valores["p_hat"]
        nc = _normalizar_confianza(valores["nc"])
        if n <= 0:
            raise ValueError("n debe ser mayor que 0.")
        if not 0 <= p_hat <= 1:
            raise ValueError("La proporción muestral (p) debe estar entre 0 y 1.")
        alpha = 1 - nc
        alpha_2 = alpha / 2
        q_hat = 1 - p_hat
        z = stats.norm.ppf(1 - alpha_2)
        se = math.sqrt((p_hat * q_hat) / n)
        e = z * se
        li = p_hat - e
        ls = p_hat + e
        return {
            "q_hat": q_hat,
            "alpha": alpha,
            "alpha_2": alpha_2,
            "z": z,
            "se": se,
            "e": e,
            "li": li,
            "ls": ls,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, p se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_5(self):
        self._crear_calculadora_estandar(
            "IC 5",
            "Calculadora 5 - IC Varianza (Chi-cuadrada)",
            "El límite inferior usa el chi-cuadrada mayor y el superior el menor.",
            "α = 1 - NC | α/2 = α / 2 | df = n - 1 | χ² derecha = χ²(1 - α/2, df) | χ² izquierda = χ²(α/2, df) | LI = (n - 1) × s² / χ² derecha | LS = (n - 1) × s² / χ² izquierda",
            [
                {"nombre": "n", "etiqueta": "n", "default": "20"},
                {"nombre": "s2", "etiqueta": "s²", "default": "25"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "alpha", "etiqueta": "α", "decimales": 4},
                {"nombre": "alpha_2", "etiqueta": "α/2", "decimales": 4},
                {"nombre": "df", "etiqueta": "df", "decimales": 0},
                {"nombre": "chi_right", "etiqueta": "χ² derecha", "decimales": 4},
                {"nombre": "chi_left", "etiqueta": "χ² izquierda", "decimales": 4},
            ],
            self._calc_ic_varianza,
        )

    def _calc_ic_varianza(self, valores):
        n = valores["n"]
        s2 = valores["s2"]
        nc = _normalizar_confianza(valores["nc"])
        if n <= 1 or s2 < 0:
            raise ValueError("n debe ser mayor que 1 y s² no puede ser negativa.")
        alpha = 1 - nc
        alpha_2 = alpha / 2
        df = n - 1
        chi_right = stats.chi2.ppf(1 - alpha_2, df)
        chi_left = stats.chi2.ppf(alpha_2, df)
        li = (df * s2) / chi_right
        ls = (df * s2) / chi_left
        return {
            "alpha": alpha,
            "alpha_2": alpha_2,
            "df": df,
            "chi_right": chi_right,
            "chi_left": chi_left,
            "li": li,
            "ls": ls,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, σ² se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_6(self):
        self._crear_calculadora_estandar(
            "IC 6",
            "Calculadora 6 - Diferencia de medias, varianzas conocidas",
            "Usar cuando σ1 y σ2 son conocidas.",
            "α = 1 - NC | α/2 = α / 2 | Z(α/2) = valor crítico normal | SE = √(σ1²/n1 + σ2²/n2) | Dif = x̄1 - x̄2 | E = Z × SE | LI = Dif - E | LS = Dif + E",
            [
                {"nombre": "n1", "etiqueta": "n₁", "default": "20"},
                {"nombre": "x1", "etiqueta": "x̄₁", "default": "50"},
                {"nombre": "sigma1", "etiqueta": "σ₁", "default": "10"},
                {"nombre": "n2", "etiqueta": "n₂", "default": "22"},
                {"nombre": "x2", "etiqueta": "x̄₂", "default": "45"},
                {"nombre": "sigma2", "etiqueta": "σ₂", "default": "8"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "alpha", "etiqueta": "α", "decimales": 4},
                {"nombre": "alpha_2", "etiqueta": "α/2", "decimales": 4},
                {"nombre": "z", "etiqueta": "Z(α/2)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "dif", "etiqueta": "Diferencia", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            self._calc_diff_medias_varianzas_conocidas,
        )

    def _calc_diff_medias_varianzas_conocidas(self, valores):
        if valores["n1"] <= 0 or valores["n2"] <= 0 or valores["sigma1"] < 0 or valores["sigma2"] < 0:
            raise ValueError("n1 y n2 deben ser mayores que 0; σ1 y σ2 no pueden ser negativas.")
        nc = _normalizar_confianza(valores["nc"])
        alpha = 1 - nc
        alpha_2 = alpha / 2
        z = stats.norm.ppf(1 - alpha_2)
        se = math.sqrt((valores["sigma1"] ** 2) / valores["n1"] + (valores["sigma2"] ** 2) / valores["n2"])
        dif = valores["x1"] - valores["x2"]
        e = z * se
        li = dif - e
        ls = dif + e
        return {
            "alpha": alpha,
            "alpha_2": alpha_2,
            "z": z,
            "se": se,
            "dif": dif,
            "e": e,
            "li": li,
            "ls": ls,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, μ₁ - μ₂ se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_7(self):
        self._crear_calculadora_estandar(
            "IC 7",
            "Calculadora 7 - Diferencia de medias, varianzas iguales",
            "Usar solo si el problema indica varianzas iguales o poblaciones homogéneas.",
            "df = n1 + n2 - 2 | sp² = [(n1 - 1)s1² + (n2 - 1)s2²] / (n1 + n2 - 2) | t = valor crítico t-Student | SE = √[sp² × (1/n1 + 1/n2)] | Dif = x̄1 - x̄2 | E = t × SE | LI = Dif - E | LS = Dif + E",
            [
                {"nombre": "n1", "etiqueta": "n₁", "default": "20"},
                {"nombre": "x1", "etiqueta": "x̄₁", "default": "50"},
                {"nombre": "s1", "etiqueta": "s₁", "default": "10"},
                {"nombre": "n2", "etiqueta": "n₂", "default": "22"},
                {"nombre": "x2", "etiqueta": "x̄₂", "default": "45"},
                {"nombre": "s2", "etiqueta": "s₂", "default": "8"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "df", "etiqueta": "df", "decimales": 0},
                {"nombre": "sp2", "etiqueta": "sp²", "decimales": 4},
                {"nombre": "t", "etiqueta": "t(α/2, df)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "dif", "etiqueta": "Diferencia", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            self._calc_diff_medias_varianzas_iguales,
        )

    def _calc_diff_medias_varianzas_iguales(self, valores):
        if valores["n1"] <= 1 or valores["n2"] <= 1 or valores["s1"] < 0 or valores["s2"] < 0:
            raise ValueError("n1 y n2 deben ser mayores que 1; s1 y s2 no pueden ser negativas.")
        nc = _normalizar_confianza(valores["nc"])
        df = valores["n1"] + valores["n2"] - 2
        sp2 = (((valores["n1"] - 1) * (valores["s1"] ** 2)) + ((valores["n2"] - 1) * (valores["s2"] ** 2))) / df
        t_crit = stats.t.ppf(1 - (1 - nc) / 2, df)
        se = math.sqrt(sp2 * ((1 / valores["n1"]) + (1 / valores["n2"])))
        dif = valores["x1"] - valores["x2"]
        e = t_crit * se
        li = dif - e
        ls = dif + e
        return {
            "df": df,
            "sp2": sp2,
            "t": t_crit,
            "se": se,
            "dif": dif,
            "e": e,
            "li": li,
            "ls": ls,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, μ₁ - μ₂ se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_8(self):
        self._crear_calculadora_estandar(
            "IC 8",
            "Calculadora 8 - Diferencia de medias, varianzas diferentes (Welch)",
            "Caso más realista cuando no se asumen varianzas iguales.",
            "A = s1²/n1 | B = s2²/n2 | v = (A + B)² / [A²/(n1 - 1) + B²/(n2 - 1)] | t = valor crítico t-Student | SE = √(A + B) | Dif = x̄1 - x̄2 | E = t × SE | LI = Dif - E | LS = Dif + E",
            [
                {"nombre": "n1", "etiqueta": "n₁", "default": "20"},
                {"nombre": "x1", "etiqueta": "x̄₁", "default": "50"},
                {"nombre": "s1", "etiqueta": "s₁", "default": "10"},
                {"nombre": "n2", "etiqueta": "n₂", "default": "22"},
                {"nombre": "x2", "etiqueta": "x̄₂", "default": "45"},
                {"nombre": "s2", "etiqueta": "s₂", "default": "8"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "A", "etiqueta": "A", "decimales": 4},
                {"nombre": "B", "etiqueta": "B", "decimales": 4},
                {"nombre": "v", "etiqueta": "v", "decimales": 0},
                {"nombre": "t", "etiqueta": "t(α/2, v)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            self._calc_diff_medias_welch,
        )

    def _calc_diff_medias_welch(self, valores):
        if valores["n1"] <= 1 or valores["n2"] <= 1 or valores["s1"] < 0 or valores["s2"] < 0:
            raise ValueError("n1 y n2 deben ser mayores que 1; s1 y s2 no pueden ser negativas.")
        nc = _normalizar_confianza(valores["nc"])
        A = (valores["s1"] ** 2) / valores["n1"]
        B = (valores["s2"] ** 2) / valores["n2"]
        numerador = (A + B) ** 2
        denominador = ((A ** 2) / (valores["n1"] - 1)) + ((B ** 2) / (valores["n2"] - 1))
        v = math.floor(numerador / denominador)
        if v <= 0:
            raise ValueError("Los grados de libertad de Welch no pudieron calcularse.")
        t_crit = stats.t.ppf(1 - (1 - nc) / 2, v)
        se = math.sqrt(A + B)
        dif = valores["x1"] - valores["x2"]
        e = t_crit * se
        li = dif - e
        ls = dif + e
        return {
            "A": A,
            "B": B,
            "v": v,
            "t": t_crit,
            "se": se,
            "e": e,
            "li": li,
            "ls": ls,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, μ₁ - μ₂ se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_9(self):
        self._crear_calculadora_estandar(
            "IC 9",
            "Calculadora 9 - Diferencia de medias, n1 y n2 ≥ 30 (Z)",
            "Usar solo si ambas muestras tienen n ≥ 30.",
            "α = 1 - NC | α/2 = α / 2 | Z(α/2) = valor crítico normal | SE = √(s1²/n1 + s2²/n2) | Dif = x̄1 - x̄2 | E = Z × SE | LI = Dif - E | LS = Dif + E",
            [
                {"nombre": "n1", "etiqueta": "n₁", "default": "35"},
                {"nombre": "x1", "etiqueta": "x̄₁", "default": "50"},
                {"nombre": "s1", "etiqueta": "s₁", "default": "10"},
                {"nombre": "n2", "etiqueta": "n₂", "default": "32"},
                {"nombre": "x2", "etiqueta": "x̄₂", "default": "45"},
                {"nombre": "s2", "etiqueta": "s₂", "default": "8"},
                {"nombre": "nc", "etiqueta": "NC", "default": "0.95"},
            ],
            [
                {"nombre": "alpha", "etiqueta": "α", "decimales": 4},
                {"nombre": "alpha_2", "etiqueta": "α/2", "decimales": 4},
                {"nombre": "z", "etiqueta": "Z(α/2)", "decimales": 4},
                {"nombre": "se", "etiqueta": "SE", "decimales": 4},
                {"nombre": "dif", "etiqueta": "Diferencia", "decimales": 4},
                {"nombre": "e", "etiqueta": "E", "decimales": 4},
            ],
            self._calc_diff_medias_z,
        )

    def _calc_diff_medias_z(self, valores):
        if valores["n1"] <= 0 or valores["n2"] <= 0 or valores["s1"] < 0 or valores["s2"] < 0:
            raise ValueError("n1 y n2 deben ser mayores que 0; s1 y s2 no pueden ser negativas.")
        nc = _normalizar_confianza(valores["nc"])
        if valores["n1"] < 30 or valores["n2"] < 30:
            estado = "Nota: Use esta calculadora solo si ambas muestras tienen n >= 30."
        else:
            estado = ""
        alpha = 1 - nc
        alpha_2 = alpha / 2
        z = stats.norm.ppf(1 - alpha_2)
        se = math.sqrt((valores["s1"] ** 2) / valores["n1"] + (valores["s2"] ** 2) / valores["n2"])
        dif = valores["x1"] - valores["x2"]
        e = z * se
        li = dif - e
        ls = dif + e
        return {
            "alpha": alpha,
            "alpha_2": alpha_2,
            "z": z,
            "se": se,
            "dif": dif,
            "e": e,
            "li": li,
            "ls": ls,
            "estado": estado,
            "conclusion": f"Con {_fmt_confianza(nc)} de confianza, μ₁ - μ₂ se encuentra entre {li:.2f} y {ls:.2f}.",
        }

    def _crear_calculadora_10(self):
        contenedor, frame_entradas, frame_salidas = self._crear_pestana_base(
            "IC 10",
            "Calculadora 10 - Diferencia de medias, muestras pareadas",
            "Se puede ingresar la lista de pares (x1i, x2i) o directamente d̄, sd y n.",
            "Si se ingresan pares: di = x1i - x2i, luego d̄ = promedio(di) y sd = desviación estándar de di | df = n - 1 | t = valor crítico t-Student | SE = sd / √n | E = t × SE | LI = d̄ - E | LS = d̄ + E",
        )
        decimales = self._decimales_actuales()

        modo_var = tk.StringVar(value="Pares")
        tk.Label(frame_entradas, text="Modo de entrada", bg="#E8F5E9", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        combo_modo = ttk.Combobox(frame_entradas, textvariable=modo_var, state="readonly", values=["Pares", "Resumen"], width=18)
        combo_modo.grid(row=0, column=1, sticky="w", pady=5, padx=(0, 12))

        nc_var = tk.StringVar(value="0.95")
        tk.Label(frame_entradas, text="NC", bg="#E8F5E9", font=("Helvetica", 10, "bold")).grid(row=0, column=2, sticky="w", pady=5)
        tk.Entry(frame_entradas, textvariable=nc_var, width=18).grid(row=0, column=3, sticky="w", pady=5)

        frame_pares = tk.Frame(frame_entradas, bg="#E8F5E9")
        frame_resumen = tk.Frame(frame_entradas, bg="#E8F5E9")
        frame_pares.grid(row=1, column=0, columnspan=4, sticky="we")
        frame_resumen.grid(row=1, column=0, columnspan=4, sticky="we")

        tk.Label(frame_pares, text="Pares x1i, x2i (uno por línea)", bg="#E8F5E9", font=("Helvetica", 10, "bold")).pack(anchor="w")
        text_pares = tk.Text(frame_pares, height=8, width=42, wrap="none", font=("Consolas", 10))
        text_pares.pack(fill="x", pady=(4, 8))
        text_pares.insert("1.0", "10, 8\n12, 9\n11, 10")

        dbar_var = tk.StringVar(value="")
        sd_var = tk.StringVar(value="")
        n_var = tk.StringVar(value="")

        tk.Label(frame_resumen, text="d̄", bg="#E8F5E9", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(frame_resumen, textvariable=dbar_var, width=18).grid(row=0, column=1, sticky="w", pady=5, padx=(0, 12))
        tk.Label(frame_resumen, text="sd", bg="#E8F5E9", font=("Helvetica", 10, "bold")).grid(row=0, column=2, sticky="w", pady=5)
        tk.Entry(frame_resumen, textvariable=sd_var, width=18).grid(row=0, column=3, sticky="w", pady=5)

        tk.Label(frame_resumen, text="n", bg="#E8F5E9", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(frame_resumen, textvariable=n_var, width=18).grid(row=1, column=1, sticky="w", pady=5, padx=(0, 12))
        tk.Label(frame_resumen, text="NC", bg="#E8F5E9", font=("Helvetica", 10, "bold")).grid(row=1, column=2, sticky="w", pady=5)
        tk.Entry(frame_resumen, textvariable=nc_var, width=18).grid(row=1, column=3, sticky="w", pady=5)

        ayuda_var = tk.StringVar(value="Pares: ingrese x1i y x2i por línea. Resumen: ingrese d̄, sd, n y NC directamente.")
        tk.Label(
            frame_entradas,
            textvariable=ayuda_var,
            bg="#FFF8E1",
            fg="#37474F",
            font=("Consolas", 10),
            justify="left",
            wraplength=520,
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=6,
        ).grid(row=2, column=0, columnspan=4, sticky="we", pady=(8, 0))

        salida_vars = {}
        for indice, salida in enumerate([
            {"nombre": "dbar", "etiqueta": "d̄"},
            {"nombre": "sd", "etiqueta": "sd"},
            {"nombre": "df", "etiqueta": "df"},
            {"nombre": "t", "etiqueta": "t(α/2, df)"},
            {"nombre": "se", "etiqueta": "SE"},
            {"nombre": "e", "etiqueta": "E"},
        ]):
            fila = indice // 2
            columna = (indice % 2) * 2
            tk.Label(frame_salidas, text=salida["etiqueta"], bg="#E3F2FD", font=("Helvetica", 10, "bold")).grid(row=fila, column=columna, sticky="w", pady=5, padx=(0, 6))
            variable = tk.StringVar(value="-")
            tk.Label(
                frame_salidas,
                textvariable=variable,
                bg="white",
                fg=COLOR_PRIMARY,
                font=("Consolas", 10, "bold"),
                anchor="w",
                relief="solid",
                borderwidth=1,
                padx=8,
                pady=4,
                width=24,
            ).grid(row=fila, column=columna + 1, sticky="we", pady=5, padx=(0, 12))
            salida_vars[salida["nombre"]] = variable

        li_var, ls_var = self._crear_resultado_final(frame_salidas)
        conclusion_var, estado_var = self._crear_conclusion_y_estado(frame_salidas)

        def leer_pares():
            texto = text_pares.get("1.0", "end").strip()
            if not texto:
                return None
            pares = []
            for linea in texto.splitlines():
                linea = linea.strip()
                if not linea:
                    continue
                partes = [parte for parte in re.split(r"[;,\s]+", linea) if parte]
                if len(partes) < 2:
                    raise ValueError(f"Fila inválida en pares: {linea}")
                pares.append((float(partes[0].replace(",", ".")), float(partes[1].replace(",", "."))))
            return pares

        def mostrar_modo(*_):
            if modo_var.get() == "Pares":
                frame_pares.grid()
                frame_resumen.grid_remove()
                ayuda_var.set("Pares: ingrese x1i y x2i por línea.")
            else:
                frame_pares.grid_remove()
                frame_resumen.grid()
                ayuda_var.set("Resumen: ingrese d̄, sd, n y NC directamente.")

        def limpiar_todo(mensaje_estado=""):
            self._limpiar_salida(salida_vars, li_var, ls_var, conclusion_var, estado_var)
            if mensaje_estado:
                estado_var.set(mensaje_estado)

        def recalcular(*_):
            try:
                if modo_var.get() == "Pares":
                    pares = leer_pares()
                    if not pares:
                        limpiar_todo()
                        return
                    if len(pares) < 2:
                        raise ValueError("Se requieren al menos 2 pares para calcular sd.")
                    diferencias = [x1 - x2 for x1, x2 in pares]
                    dbar = mean(diferencias)
                    sd = stdev(diferencias)
                    n = len(diferencias)
                else:
                    dbar = _parse_float(dbar_var.get())
                    sd = _parse_float(sd_var.get())
                    n = _parse_float(n_var.get())
                    if None in (dbar, sd, n):
                        limpiar_todo()
                        return
                    if n <= 1 or sd < 0:
                        raise ValueError("n debe ser mayor que 1 y sd no puede ser negativa.")

                nc = _normalizar_confianza(nc_var.get())
                alpha = 1 - nc
                df = n - 1
                t_crit = stats.t.ppf(1 - alpha / 2, df)
                se = sd / math.sqrt(n)
                e = t_crit * se
                li = dbar - e
                ls = dbar + e

                salida_vars["dbar"].set(_fmt_numero(dbar, decimales))
                salida_vars["sd"].set(_fmt_numero(sd, decimales))
                salida_vars["df"].set(_fmt_numero(df, decimales))
                salida_vars["t"].set(_fmt_numero(t_crit, decimales))
                salida_vars["se"].set(_fmt_numero(se, decimales))
                salida_vars["e"].set(_fmt_numero(e, decimales))
                li_var.set(_fmt_numero(li, decimales))
                ls_var.set(_fmt_numero(ls, decimales))
                conclusion_var.set(f"Con {_fmt_confianza(nc)} de confianza, μd se encuentra entre {li:.2f} y {ls:.2f}.")
                estado_var.set("")
            except Exception as exc:
                limpiar_todo(str(exc))

        modo_var.trace_add("write", mostrar_modo)
        nc_var.trace_add("write", recalcular)
        dbar_var.trace_add("write", recalcular)
        sd_var.trace_add("write", recalcular)
        n_var.trace_add("write", recalcular)
        text_pares.bind("<KeyRelease>", recalcular)
        combo_modo.bind("<<ComboboxSelected>>", recalcular)

        def limpiar():
            text_pares.delete("1.0", "end")
            dbar_var.set("")
            sd_var.set("")
            n_var.set("")
            nc_var.set("0.95")
            limpiar_todo()

        botones = tk.Frame(frame_entradas, bg="#E8F5E9")
        botones.grid(row=3, column=0, columnspan=4, sticky="w", pady=(10, 0))

        tk.Button(
            botones,
            text="📊 Calcular",
            command=recalcular,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=8,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botones,
            text="🧹 Limpiar",
            command=limpiar,
            bg=COLOR_WARNING,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=8,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="left")

        mostrar_modo()
        recalcular()


def abrir_modulo_intervalos_confianza(root):
    """Abre la nueva sección completa de intervalos de confianza."""
    VentanaIntervalosConfianza(root)
