"""Ventana principal de Estadistica II (lanzador de temas)."""

import tkinter as tk

from config_interfaz import *
from interfaz.estadistica_ii import (
    abrir_modulo_estimacion_tamano_muestra,
    abrir_modulo_muestreo,
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

        cont = tk.Frame(self.root, bg=BG_LIGHT)
        cont.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            cont,
            text=f"Usuario: {self.usuario}",
            font=("Helvetica", 11),
            bg=BG_LIGHT,
            fg=TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 20))

        tk.Label(
            cont,
            text="Temas de Estadistica II",
            font=("Helvetica", 22, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY,
        ).pack(pady=(0, 10))

        frame_botones = tk.Frame(cont, bg=BG_LIGHT)
        frame_botones.pack(fill="both", expand=True)

        self._crear_card_tema(
            frame_botones,
            "📊 Estimacion y Tamano de Muestra",
            "Incluye: tamano de muestra, estimacion puntual e intervalos de confianza.",
            abrir_modulo_estimacion_tamano_muestra,
            "#F3E5F5",
            "#4A148C",
            "#4A2A62",
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

        tk.Button(
            cont,
            text="Volver al selector",
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
        card.pack(fill="x", padx=80, pady=10)

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
