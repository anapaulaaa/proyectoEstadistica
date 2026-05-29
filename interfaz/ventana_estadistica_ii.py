"""Ventana principal de Estadistica II (lanzador de temas)."""

import tkinter as tk

from config_interfaz import *
from interfaz.estadistica_ii import (
    abrir_modulo_tamano_muestra,
    abrir_modulo_estimacion_puntual,
    abrir_modulo_intervalos_confianza,
    abrir_modulo_muestreo,
    abrir_modulo_anova_menu,
)


class VentanaEstadisticaII:
    """Vista principal de Estadistica II."""

    def __init__(self, root, usuario, callback_volver, callback_cerrar_sesion):
        self.root = root
        self.usuario = usuario
        self.callback_volver = callback_volver
        self.callback_cerrar_sesion = callback_cerrar_sesion

        self.crear_interfaz()

    def crear_interfaz(self):
        self.root.configure(bg=BG_LIGHT)
        self.root.title(f"{NOMBRE_PROYECTO} - Estadistica II")

        barra = tk.Frame(self.root, bg=COLOR_PRIMARY, height=75)
        barra.pack(fill="x", side="top")

        tk.Label(
            barra,
            text="Estadistica II",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT,
        ).pack(side="left", padx=20, pady=18)

        tk.Button(
            barra,
            text="Cerrar Sesion",
            command=self.callback_cerrar_sesion,
            bg=COLOR_DANGER,
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(side="right", padx=20, pady=18)

        contenedor = tk.Frame(self.root, bg=BG_LIGHT)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, bg=BG_LIGHT, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        cont = tk.Frame(canvas, bg=BG_LIGHT)
        cont_window = canvas.create_window((0, 0), window=cont, anchor="nw")

        def _actualizar_scroll(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _ajustar_ancho(event):
            canvas.itemconfigure(cont_window, width=event.width)

        cont.bind("<Configure>", _actualizar_scroll)
        canvas.bind("<Configure>", _ajustar_ancho)

        def _mover_rueda(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _mover_rueda)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))


        tk.Label(
            cont,
            text=f"Usuario: {self.usuario}",
            font=("Helvetica", 11),
            bg=BG_LIGHT,
            fg=TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 20))

        panel_resumen = tk.Frame(cont, bg="#E8F5E9", relief="solid", borderwidth=1)
        panel_resumen.pack(fill="x", padx=20, pady=(0, 18))

        tk.Label(
            panel_resumen,
            text="Preparado para la evaluación",
            font=("Helvetica", 16, "bold"),
            bg="#E8F5E9",
            fg="#1B5E20",
        ).pack(anchor="w", padx=16, pady=(14, 4))

        tk.Label(
            panel_resumen,
            text=(
                "Verifica aquí los apartados que normalmente se califican y entra directo al tema que necesitas practicar."
            ),
            font=("Helvetica", 10),
            bg="#E8F5E9",
            fg="#2E7D32",
            wraplength=1150,
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 10))

        checklist = tk.Frame(panel_resumen, bg="#E8F5E9")
        checklist.pack(fill="x", padx=16, pady=(0, 14))
        items = [
            "Intervalos de confianza para media, proporción y varianza",
            "Intervalos de confianza para diferencia de medias",
            "ANOVA de 1 factor para la demostración en clase",
            "ANOVA de 2 factores con y sin replicación para repasar conceptos",
        ]
        for texto in items:
            fila = tk.Frame(checklist, bg="#E8F5E9")
            fila.pack(anchor="w", fill="x", pady=2)
            tk.Label(fila, text="•", bg="#E8F5E9", fg="#1B5E20", font=("Helvetica", 12, "bold")).pack(side="left")
            tk.Label(fila, text=texto, bg="#E8F5E9", fg="#1B5E20", font=("Helvetica", 10), wraplength=1120, justify="left").pack(side="left", padx=(6, 0))

        tk.Label(
            cont,
            text="Temas de Estadistica II",
            font=("Helvetica", 22, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY,
        ).pack(pady=(0, 10))

        frame_botones = tk.Frame(cont, bg=BG_LIGHT)
        frame_botones.pack(fill="both", expand=True)
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        self._crear_card_tema(
            frame_botones,
            "📐 Tamano de Muestra",
            "Calculo de n y ajuste por perdidas.",
            abrir_modulo_tamano_muestra,
            "#E3F2FD",
            "#0D47A1",
            "#1565C0",
        )

        self._crear_card_tema(
            frame_botones,
            "🎯 Estimacion Puntual",
            "Estimacion de p y q en muestras o poblacion conocida.",
            abrir_modulo_estimacion_puntual,
            "#E8F5E9",
            "#1B5E20",
            "#2E7D32",
        )

        self._crear_card_tema(
            frame_botones,
            "📏 Intervalos de Confianza",
            "Incluye medias, proporciones, varianza y diferencias de medias.",
            abrir_modulo_intervalos_confianza,
            "#FFF8E1",
            "#F57F17",
            "#E65100",
        )

        self._crear_card_tema(
            frame_botones,
            "🧩 Seleccion y Tipos de Muestreo",
            "Incluye: probabilistico, no probabilistico, errores y referencias.",
            abrir_modulo_muestreo,
            "#E8F5E9",
            "#1B5E20",
            "#2E7D32",
        )

        self._crear_card_tema(
            frame_botones,
            "📊 ANOVA",
            "Abre el menú de ANOVA para elegir 1 factor, 2 factores o ejercicios.",
            abrir_modulo_anova_menu,
            "#E3F2FD",
            "#0D47A1",
            "#1565C0",
        )

        tk.Button(
            cont,
            text="← Volver al selector",
            command=self.callback_volver,
            bg=COLOR_INFO,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack(pady=(20, 0))

    def _crear_card_tema(self, parent, titulo, descripcion, comando, bg, fg_titulo, fg_desc):
        card = tk.Frame(parent, bg=bg, relief="solid", borderwidth=2)
        card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            card,
            text=titulo,
            font=("Helvetica", 16, "bold"),
            bg=bg,
            fg=fg_titulo,
        ).pack(pady=(18, 8))

        tk.Label(
            card,
            text=descripcion,
            font=("Helvetica", 11),
            bg=bg,
            fg=fg_desc,
            justify="center",
            wraplength=1000,
        ).pack(pady=(0, 12))

        tk.Button(
            card,
            text="Abrir modulo",
            command=lambda: comando(self.root),
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
