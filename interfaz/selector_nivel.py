"""Pantalla de seleccion de nivel: Estadistica I o Estadistica II."""

import tkinter as tk

from config_interfaz import *


class SelectorNivel:
    """Pantalla intermedia para elegir modulo de trabajo."""

    def __init__(self, root, usuario, callback_estadistica_1, callback_estadistica_2, callback_cerrar_sesion):
        self.root = root
        self.usuario = usuario
        self.callback_estadistica_1 = callback_estadistica_1
        self.callback_estadistica_2 = callback_estadistica_2
        self.callback_cerrar_sesion = callback_cerrar_sesion

        self.crear_interfaz()

    def crear_interfaz(self):
        self.root.configure(bg=BG_LIGHT)
        self.root.title(f"{NOMBRE_PROYECTO} - Seleccion de Modulo")

        barra = tk.Frame(self.root, bg=COLOR_PRIMARY, height=75)
        barra.pack(fill="x", side="top")

        tk.Label(
            barra,
            text=f"{ICONO_ESTADISTICA} {NOMBRE_PROYECTO}",
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

        frame = tk.Frame(self.root, bg=BG_LIGHT)
        frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            frame,
            text=f"Bienvenido/a, {self.usuario.upper()}",
            font=("Helvetica", 24, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY,
        ).pack(pady=(10, 10))

        tk.Label(
            frame,
            text="Selecciona el modulo con el que deseas trabajar",
            font=("Helvetica", 13),
            bg=BG_LIGHT,
            fg=TEXT_MUTED,
        ).pack(pady=(0, 25))

        botones_frame = tk.Frame(frame, bg=BG_LIGHT)
        botones_frame.pack(expand=True)

        card_1 = tk.Frame(botones_frame, bg="#E3F2FD", relief="solid", borderwidth=2)
        card_1.pack(side="left", padx=20, pady=10, ipadx=25, ipady=25)

        tk.Label(
            card_1,
            text="Estadistica I",
            font=("Helvetica", 18, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1",
        ).pack(pady=(10, 8))

        tk.Label(
            card_1,
            text="Descriptiva e inferencial base\n(temario actual)",
            font=("Helvetica", 11),
            bg="#E3F2FD",
            fg="#1E3A5F",
            justify="center",
        ).pack(pady=(0, 15))

        tk.Button(
            card_1,
            text="Entrar a Estadistica I",
            command=self.callback_estadistica_1,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack()

        card_2 = tk.Frame(botones_frame, bg="#F3E5F5", relief="solid", borderwidth=2)
        card_2.pack(side="left", padx=20, pady=10, ipadx=25, ipady=25)

        tk.Label(
            card_2,
            text="Estadistica II",
            font=("Helvetica", 18, "bold"),
            bg="#F3E5F5",
            fg="#4A148C",
        ).pack(pady=(10, 8))

        tk.Label(
            card_2,
            text="Nueva unidad del proyecto\n(estructura inicial)",
            font=("Helvetica", 11),
            bg="#F3E5F5",
            fg="#4A2A62",
            justify="center",
        ).pack(pady=(0, 15))

        tk.Button(
            card_2,
            text="Entrar a Estadistica II",
            command=self.callback_estadistica_2,
            bg=COLOR_SECONDARY,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            activebackground="#FFEB3B",
            activeforeground="#000000",
        ).pack()
