"""Modulo UI: estimacion y tamano de muestra en ventanas separadas."""

import tkinter as tk
from tkinter import ttk, messagebox

from config_interfaz import *
from estadistica_inferencial.estimacion_tamano_muestra import EstimacionTamanoMuestra


def _centrar_ventana(ventana, proporcion_w=0.8, proporcion_h=0.8):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    window_width = int(screen_width * proporcion_w)
    window_height = int(screen_height * proporcion_h)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")


def abrir_modulo_estimacion_tamano_muestra(root):
    """Menu principal del modulo de estimacion y tamano de muestra."""
    ventana = tk.Toplevel(root)
    ventana.title("📊 Estimacion y Tamano de Muestra")
    _centrar_ventana(ventana, 0.72, 0.65)
    ventana.configure(bg=BG_LIGHT)

    tk.Label(
        ventana,
        text="📊 ESTIMACION Y TAMANO DE MUESTRA",
        font=("Helvetica", 16, "bold"),
        bg=BG_LIGHT,
        fg=COLOR_PRIMARY,
    ).pack(pady=(20, 10))

    tk.Label(
        ventana,
        text="Selecciona la ventana de calculo",
        font=("Helvetica", 11),
        bg=BG_LIGHT,
        fg=TEXT_MUTED,
    ).pack(pady=(0, 20))

    panel = tk.Frame(ventana, bg=BG_LIGHT)
    panel.pack(fill="both", expand=True, padx=40, pady=10)

    botones = [
        ("📐 Tamano de Muestra", lambda: _abrir_ventana_tamano_muestra(root), "#E3F2FD", "#0D47A1"),
        ("🎯 Estimacion Puntual", lambda: _abrir_ventana_estimacion_puntual(root), "#E8F5E9", "#1B5E20"),
        ("📏 Intervalos de Confianza", lambda: _abrir_ventana_intervalos(root), "#FFF8E1", "#F57F17"),
    ]

    for texto, comando, bg_card, fg_card in botones:
        card = tk.Frame(panel, bg=bg_card, relief="solid", borderwidth=2)
        card.pack(fill="x", pady=8)
        tk.Button(
            card,
            text=texto,
            command=comando,
            bg=bg_card,
            fg=fg_card,
            activebackground="#FFEB3B",
            activeforeground="#000000",
            relief="flat",
            cursor="hand2",
            font=("Helvetica", 13, "bold"),
            padx=16,
            pady=14,
        ).pack(fill="x")

    def ir_a_muestreo():
        from interfaz.estadistica_ii.modulo_muestreo import abrir_modulo_muestreo

        ventana.destroy()
        abrir_modulo_muestreo(root)

    frame_nav = tk.Frame(ventana, bg=BG_LIGHT)
    frame_nav.pack(pady=15)

    tk.Button(
        frame_nav,
        text="🧩 Ir a Muestreo",
        command=ir_a_muestreo,
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


def _abrir_ventana_tamano_muestra(root):
    estimador = EstimacionTamanoMuestra()

    ventana = tk.Toplevel(root)
    ventana.title("📐 Tamano de Muestra")
    _centrar_ventana(ventana, 0.78, 0.72)
    ventana.configure(bg=BG_LIGHT)

    frame = tk.LabelFrame(
        ventana,
        text="Calculo de Tamano de Muestra",
        bg=BG_WHITE,
        font=("Helvetica", 11, "bold"),
        padx=12,
        pady=12,
    )
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tipo_var = tk.StringVar(value="Proporciones")
    caso_var = tk.StringVar(value="Poblacion desconocida")
    conf_var = tk.StringVar(value="95")
    p_var = tk.StringVar(value="0.5")
    s_var = tk.StringVar(value="10")
    d_var = tk.StringVar(value="0.05")
    n_pob_var = tk.StringVar(value="")
    ajuste_var = tk.BooleanVar(value=False)
    pe_var = tk.StringVar(value="")

    tk.Label(frame, text="Tipo:", bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    ttk.Combobox(
        frame,
        textvariable=tipo_var,
        state="readonly",
        values=["Proporciones", "Medias"],
        width=24,
    ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Caso:", bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=0, column=2, sticky="w", pady=5)
    ttk.Combobox(
        frame,
        textvariable=caso_var,
        state="readonly",
        values=["Poblacion desconocida", "Poblacion conocida"],
        width=24,
    ).grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Nivel de confianza (%):", bg=BG_WHITE).grid(row=1, column=0, sticky="w", pady=5)
    tk.Entry(frame, textvariable=conf_var, width=28).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Margen de error (d):", bg=BG_WHITE).grid(row=1, column=2, sticky="w", pady=5)
    tk.Entry(frame, textvariable=d_var, width=28).grid(row=1, column=3, padx=5, pady=5, sticky="w")

    label_p = tk.Label(frame, text="p (proporcion esperada):", bg=BG_WHITE)
    label_p.grid(row=2, column=0, sticky="w", pady=5)
    entry_p = tk.Entry(frame, textvariable=p_var, width=28)
    entry_p.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    label_s = tk.Label(frame, text="s (desviacion estandar):", bg=BG_WHITE)
    label_s.grid(row=3, column=0, sticky="w", pady=5)
    entry_s = tk.Entry(frame, textvariable=s_var, width=28)
    entry_s.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    label_n = tk.Label(frame, text="N (tamano poblacional):", bg=BG_WHITE)
    label_n.grid(row=2, column=2, sticky="w", pady=5)
    entry_n = tk.Entry(frame, textvariable=n_pob_var, width=28)
    entry_n.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    chk_ajuste = tk.Checkbutton(
        frame,
        text="Aplicar ajuste por perdidas",
        variable=ajuste_var,
        bg=BG_WHITE,
        activebackground=BG_WHITE,
    )
    chk_ajuste.grid(row=4, column=0, sticky="w", pady=5)

    tk.Label(frame, text="pe (% o proporcion):", bg=BG_WHITE).grid(row=4, column=2, sticky="w", pady=5)
    entry_pe = tk.Entry(frame, textvariable=pe_var, width=28, state="disabled")
    entry_pe.grid(row=4, column=3, padx=5, pady=5, sticky="w")

    lbl_tipo = tk.Label(
        frame,
        text="Proporciones: muestral (N desconocida) o poblacional finita (N conocida).",
        bg=BG_WHITE,
        fg=TEXT_MUTED,
        font=("Helvetica", 9, "italic"),
    )
    lbl_tipo.grid(row=5, column=0, columnspan=4, sticky="w", pady=(2, 8))

    formula_tm_var = tk.StringVar()
    frame_formula_tm = tk.LabelFrame(
        frame,
        text="Formula aplicada",
        bg="#F9FBE7",
        font=("Helvetica", 10, "bold"),
        padx=10,
        pady=8,
    )
    frame_formula_tm.grid(row=6, column=0, columnspan=4, sticky="we", pady=(0, 8))
    tk.Label(
        frame_formula_tm,
        textvariable=formula_tm_var,
        justify="left",
        anchor="w",
        bg="#F9FBE7",
        fg="#37474F",
        font=("Consolas", 10),
    ).pack(fill="x")

    resultado_var = tk.StringVar(value="n: -    |    nc: -")
    tk.Label(
        frame,
        textvariable=resultado_var,
        bg=BG_WHITE,
        fg=COLOR_PRIMARY,
        font=("Helvetica", 12, "bold"),
    ).grid(row=7, column=0, columnspan=4, sticky="w", pady=10)

    def actualizar_campos(*_):
        if tipo_var.get() == "Proporciones":
            label_p.grid()
            entry_p.grid()
            label_s.grid_remove()
            entry_s.grid_remove()
            lbl_tipo.config(text="Proporciones: muestral (N desconocida) o poblacional finita (N conocida).")
        else:
            label_p.grid_remove()
            entry_p.grid_remove()
            label_s.grid()
            entry_s.grid()
            lbl_tipo.config(text="Medias: usa s y puede aplicar correccion por poblacion finita si N es conocida.")

        if caso_var.get() == "Poblacion conocida":
            label_n.grid()
            entry_n.grid()
        else:
            label_n.grid_remove()
            entry_n.grid_remove()

        if ajuste_var.get():
            entry_pe.config(state="normal")
        else:
            entry_pe.config(state="disabled")
            pe_var.set("")

        if tipo_var.get() == "Proporciones" and caso_var.get() == "Poblacion desconocida":
            formula_tm_var.set("n = (Z^2 * p * q) / d^2")
        elif tipo_var.get() == "Proporciones" and caso_var.get() == "Poblacion conocida":
            formula_tm_var.set("n = [N * Z^2 * p * q] / [d^2 * (N - 1) + Z^2 * p * q]")
        elif tipo_var.get() == "Medias" and caso_var.get() == "Poblacion desconocida":
            formula_tm_var.set("n = (Z^2 * s^2) / d^2")
        else:
            formula_tm_var.set("n = [N * Z^2 * s^2] / [d^2 * (N - 1) + Z^2 * s^2]")

    def calcular():
        try:
            z = estimador.obtener_z(conf_var.get())
            d = float(d_var.get())
            if d <= 0:
                raise ValueError("d debe ser mayor que cero")

            n_calculado = None

            if tipo_var.get() == "Proporciones":
                p = float(p_var.get())
                if caso_var.get() == "Poblacion conocida":
                    n_pob = float(n_pob_var.get())
                    n_calculado = estimador.tamano_muestra_proporcion_conocida(n_pob, z, p, d)
                else:
                    n_calculado = estimador.tamano_muestra_proporcion_desconocida(z, p, d)
            else:
                s = float(s_var.get())
                if caso_var.get() == "Poblacion conocida":
                    n_pob = float(n_pob_var.get())
                    n_calculado = estimador.tamano_muestra_media_conocida(n_pob, z, s, d)
                else:
                    n_calculado = estimador.tamano_muestra_media_desconocida(z, s, d)

            n_redondeado = estimador.redondear_tamano_muestra(n_calculado)

            if ajuste_var.get():
                pe = float(pe_var.get())
                nc = estimador.ajuste_perdidas(n_redondeado, pe)
                nc = estimador.redondear_tamano_muestra(nc)
                resultado_var.set(f"n: {n_redondeado}    |    nc: {nc}")
            else:
                resultado_var.set(f"n: {n_redondeado}    |    nc: -")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular tamano de muestra:\n{e}")

    tipo_var.trace_add("write", actualizar_campos)
    caso_var.trace_add("write", actualizar_campos)
    ajuste_var.trace_add("write", actualizar_campos)

    tk.Button(
        frame,
        text="📊 Calcular",
        command=calcular,
        bg=COLOR_SUCCESS,
        fg="#000000",
        font=("Helvetica", 11, "bold"),
        cursor="hand2",
        padx=20,
        pady=8,
        activebackground="#FFEB3B",
        activeforeground="#000000",
    ).grid(row=8, column=0, columnspan=4, pady=12)

    actualizar_campos()


def _abrir_ventana_estimacion_puntual(root):
    estimador = EstimacionTamanoMuestra()

    ventana = tk.Toplevel(root)
    ventana.title("🎯 Estimacion Puntual")
    _centrar_ventana(ventana, 0.62, 0.56)
    ventana.configure(bg=BG_LIGHT)

    frame = tk.LabelFrame(
        ventana,
        text="Estimacion de Proporciones",
        bg=BG_WHITE,
        font=("Helvetica", 11, "bold"),
        padx=12,
        pady=12,
    )
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    modo_var = tk.StringVar(value="Proporcion muestral (p_hat = x/n)")
    x_var = tk.StringVar(value="50")
    n_var = tk.StringVar(value="100")
    p_pob_var = tk.StringVar(value="0.5")

    tk.Label(frame, text="Tipo de proporcion:", bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    ttk.Combobox(
        frame,
        textvariable=modo_var,
        state="readonly",
        width=34,
        values=[
            "Proporcion muestral (p_hat = x/n)",
            "Proporcion poblacional (p conocida)",
        ],
    ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    label_x = tk.Label(frame, text="x (exitos):", bg=BG_WHITE)
    label_x.grid(row=1, column=0, sticky="w", pady=5)
    entry_x = tk.Entry(frame, textvariable=x_var, width=36)
    entry_x.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    label_n = tk.Label(frame, text="n (muestra):", bg=BG_WHITE)
    label_n.grid(row=2, column=0, sticky="w", pady=5)
    entry_n = tk.Entry(frame, textvariable=n_var, width=36)
    entry_n.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    label_p_pob = tk.Label(frame, text="p poblacional conocida:", bg=BG_WHITE)
    label_p_pob.grid(row=3, column=0, sticky="w", pady=5)
    entry_p_pob = tk.Entry(frame, textvariable=p_pob_var, width=36)
    entry_p_pob.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    formula_ep_var = tk.StringVar()
    frame_formula_ep = tk.LabelFrame(
        frame,
        text="Formula aplicada",
        bg="#F9FBE7",
        font=("Helvetica", 10, "bold"),
        padx=10,
        pady=8,
    )
    frame_formula_ep.grid(row=4, column=0, columnspan=2, sticky="we", pady=(0, 8))
    tk.Label(
        frame_formula_ep,
        textvariable=formula_ep_var,
        justify="left",
        anchor="w",
        bg="#F9FBE7",
        fg="#37474F",
        font=("Consolas", 10),
    ).pack(fill="x")

    resultado_var = tk.StringVar(value="p: -    |    q: -")
    tk.Label(
        frame,
        textvariable=resultado_var,
        bg=BG_WHITE,
        fg=COLOR_PRIMARY,
        font=("Helvetica", 12, "bold"),
    ).grid(row=5, column=0, columnspan=2, sticky="w", pady=10)

    ayuda_var = tk.StringVar(value="Muestral: estima p_hat a partir de x y n.")
    tk.Label(frame, textvariable=ayuda_var, bg=BG_WHITE, fg=TEXT_MUTED, font=("Helvetica", 9, "italic")).grid(
        row=6, column=0, columnspan=2, sticky="w", pady=(0, 8)
    )

    def actualizar_campos(*_):
        es_muestral = modo_var.get().startswith("Proporcion muestral")
        if es_muestral:
            label_x.grid()
            entry_x.grid()
            label_n.grid()
            entry_n.grid()
            label_p_pob.grid_remove()
            entry_p_pob.grid_remove()
            ayuda_var.set("Muestral: estima p_hat a partir de x y n.")
            formula_ep_var.set("p_hat = x / n\nq_hat = 1 - p_hat")
        else:
            label_x.grid_remove()
            entry_x.grid_remove()
            label_n.grid_remove()
            entry_n.grid_remove()
            label_p_pob.grid()
            entry_p_pob.grid()
            ayuda_var.set("Poblacional: usa p conocida del parametro poblacional.")
            formula_ep_var.set("p = dato poblacional conocido\nq = 1 - p")

    def calcular():
        try:
            if modo_var.get().startswith("Proporcion muestral"):
                x = float(x_var.get())
                n = float(n_var.get())
                p = estimador.estimacion_puntual_proporcion(x, n)
            else:
                p = float(p_pob_var.get())
                if p < 0 or p > 1:
                    raise ValueError("p debe estar entre 0 y 1")

            q = estimador.calcular_q(p)
            resultado_var.set(f"p: {p:.6f}    |    q: {q:.6f}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular la proporcion:\n{e}")

    modo_var.trace_add("write", actualizar_campos)

    tk.Button(
        frame,
        text="📊 Calcular",
        command=calcular,
        bg=COLOR_SUCCESS,
        fg="#000000",
        font=("Helvetica", 11, "bold"),
        cursor="hand2",
        padx=20,
        pady=8,
        activebackground="#FFEB3B",
        activeforeground="#000000",
    ).grid(row=7, column=0, columnspan=2, pady=12)

    actualizar_campos()


def _abrir_ventana_intervalos(root):
    estimador = EstimacionTamanoMuestra()

    ventana = tk.Toplevel(root)
    ventana.title("📏 Intervalos de Confianza")
    _centrar_ventana(ventana, 0.72, 0.62)
    ventana.configure(bg=BG_LIGHT)

    frame = tk.LabelFrame(
        ventana,
        text="Intervalos de Confianza",
        bg=BG_WHITE,
        font=("Helvetica", 11, "bold"),
        padx=12,
        pady=12,
    )
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tipo_var = tk.StringVar(value="Proporciones muestrales")
    metodo_var = tk.StringVar(value="Z normal")
    conf_var = tk.StringVar(value="95")
    valor_critico_manual_var = tk.StringVar(value="")
    mostrar_pct_var = tk.BooleanVar(value=False)
    p_hat_var = tk.StringVar(value="0.5")
    n_var = tk.StringVar(value="100")
    media_var = tk.StringVar(value="70")
    s_var = tk.StringVar(value="10")

    tk.Label(frame, text="Tipo:", bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    ttk.Combobox(
        frame,
        textvariable=tipo_var,
        state="readonly",
        values=["Proporciones muestrales", "Medias"],
        width=28,
    ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Metodo valor critico:", bg=BG_WHITE).grid(row=1, column=0, sticky="w", pady=5)
    combo_metodo = ttk.Combobox(
        frame,
        textvariable=metodo_var,
        state="readonly",
        values=["Z normal", "t Student", "Manual"],
        width=28,
    )
    combo_metodo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    label_manual = tk.Label(frame, text="Valor critico manual:", bg=BG_WHITE)
    label_manual.grid(row=1, column=2, sticky="w", pady=5)
    entry_manual = tk.Entry(frame, textvariable=valor_critico_manual_var, width=30, state="disabled")
    entry_manual.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Checkbutton(
        frame,
        text="Mostrar LI/LS en porcentaje",
        variable=mostrar_pct_var,
        bg=BG_WHITE,
        activebackground=BG_WHITE,
    ).grid(row=9, column=0, columnspan=4, sticky="w", pady=(0, 6))

    tk.Label(frame, text="Nivel de confianza (%):", bg=BG_WHITE).grid(row=0, column=2, sticky="w", pady=5)
    tk.Entry(frame, textvariable=conf_var, width=30).grid(row=0, column=3, padx=5, pady=5, sticky="w")

    label_p_hat = tk.Label(frame, text="p_hat:", bg=BG_WHITE)
    label_p_hat.grid(row=2, column=0, sticky="w", pady=5)
    entry_p_hat = tk.Entry(frame, textvariable=p_hat_var, width=32)
    entry_p_hat.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="n:", bg=BG_WHITE).grid(row=2, column=2, sticky="w", pady=5)
    tk.Entry(frame, textvariable=n_var, width=30).grid(row=2, column=3, padx=5, pady=5, sticky="w")

    label_media = tk.Label(frame, text="Media (x_bar):", bg=BG_WHITE)
    label_media.grid(row=3, column=0, sticky="w", pady=5)
    entry_media = tk.Entry(frame, textvariable=media_var, width=32)
    entry_media.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    label_s = tk.Label(frame, text="s:", bg=BG_WHITE)
    label_s.grid(row=3, column=2, sticky="w", pady=5)
    entry_s = tk.Entry(frame, textvariable=s_var, width=30)
    entry_s.grid(row=3, column=3, padx=5, pady=5, sticky="w")

    label_z = tk.Label(frame, text="Z = 1.96", bg=BG_WHITE, fg=COLOR_PRIMARY, font=("Helvetica", 10, "bold"))
    label_z.grid(row=4, column=0, columnspan=4, sticky="w", pady=5)

    formula_ic_var = tk.StringVar()
    frame_formula_ic = tk.LabelFrame(
        frame,
        text="Formula aplicada",
        bg="#F9FBE7",
        font=("Helvetica", 10, "bold"),
        padx=10,
        pady=8,
    )
    frame_formula_ic.grid(row=5, column=0, columnspan=4, sticky="we", pady=(0, 8))
    tk.Label(
        frame_formula_ic,
        textvariable=formula_ic_var,
        justify="left",
        anchor="w",
        bg="#F9FBE7",
        fg="#37474F",
        font=("Consolas", 10),
    ).pack(fill="x")

    resultado_var = tk.StringVar(value="LI: -    |    LS: -")
    tk.Label(
        frame,
        textvariable=resultado_var,
        bg=BG_WHITE,
        fg=COLOR_PRIMARY,
        font=("Helvetica", 12, "bold"),
    ).grid(row=6, column=0, columnspan=4, sticky="w", pady=10)

    ayuda_var = tk.StringVar(value="Proporciones muestrales: el intervalo se calcula con p_hat.")
    tk.Label(frame, textvariable=ayuda_var, bg=BG_WHITE, fg=TEXT_MUTED, font=("Helvetica", 9, "italic")).grid(
        row=7, column=0, columnspan=4, sticky="w", pady=(0, 8)
    )

    def actualizar_criterio(*_):
        try:
            metodo = metodo_var.get()
            n_val = float(n_var.get())

            if metodo == "Manual":
                entry_manual.config(state="normal")
                label_manual.config(state="normal")
                valor = float(valor_critico_manual_var.get())
                if valor <= 0:
                    raise ValueError
                label_z.config(text=f"Valor critico manual = {valor:.6f}")
            elif metodo == "t Student":
                entry_manual.config(state="disabled")
                label_manual.config(state="disabled")
                gl = int(n_val - 1)
                t_crit = estimador.obtener_t_critico(conf_var.get(), gl)
                label_z.config(text=f"t (gl={gl}) = {t_crit:.6f}")
            else:
                entry_manual.config(state="disabled")
                label_manual.config(state="disabled")
                z = estimador.obtener_z(conf_var.get())
                label_z.config(text=f"Z = {z:.6f}")
        except Exception:
            if metodo_var.get() == "Manual":
                label_z.config(text="Valor critico manual = -")
            elif metodo_var.get() == "t Student":
                label_z.config(text="t = -")
            else:
                label_z.config(text="Z = -")

    def _obtener_valor_critico():
        metodo = metodo_var.get()
        if metodo == "Manual":
            valor = float(valor_critico_manual_var.get())
            if valor <= 0:
                raise ValueError("El valor critico manual debe ser mayor que cero")
            return valor
        if metodo == "t Student":
            n_val = float(n_var.get())
            gl = int(n_val - 1)
            return estimador.obtener_t_critico(conf_var.get(), gl)
        return estimador.obtener_z(conf_var.get())

    def actualizar_campos(*_):
        es_prop = tipo_var.get() == "Proporciones muestrales"
        if es_prop:
            label_p_hat.grid()
            entry_p_hat.grid()
            label_media.grid_remove()
            entry_media.grid_remove()
            label_s.grid_remove()
            entry_s.grid_remove()
            ayuda_var.set("Proporciones muestrales: el intervalo se calcula con p_hat.")
            formula_ic_var.set("IC_p = p_hat +/- Vc * sqrt[p_hat * (1 - p_hat) / n]\nVc: Z, t o valor manual")
        else:
            label_p_hat.grid_remove()
            entry_p_hat.grid_remove()
            label_media.grid()
            entry_media.grid()
            label_s.grid()
            entry_s.grid()
            ayuda_var.set("Medias: el intervalo se calcula con x_bar y s.")
            formula_ic_var.set("IC_mu = x_bar +/- Vc * (s / sqrt(n))\nVc: Z, t o valor manual")

    def calcular():
        try:
            valor_critico = _obtener_valor_critico()
            n = float(n_var.get())

            if tipo_var.get() == "Proporciones muestrales":
                p_hat = float(p_hat_var.get())
                li, ls = estimador.intervalo_confianza_proporcion(p_hat, n, valor_critico)
            else:
                media = float(media_var.get())
                s = float(s_var.get())
                li, ls = estimador.intervalo_confianza_media(media, s, n, valor_critico)

            if mostrar_pct_var.get():
                resultado_var.set(f"LI: {li * 100:.4f}%    |    LS: {ls * 100:.4f}%")
            else:
                resultado_var.set(f"LI: {li:.6f}    |    LS: {ls:.6f}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular el intervalo:\n{e}")

    tipo_var.trace_add("write", actualizar_campos)
    conf_var.trace_add("write", actualizar_criterio)
    n_var.trace_add("write", actualizar_criterio)
    metodo_var.trace_add("write", actualizar_criterio)
    valor_critico_manual_var.trace_add("write", actualizar_criterio)
    combo_metodo.bind("<<ComboboxSelected>>", actualizar_criterio)

    tk.Button(
        frame,
        text="📊 Calcular",
        command=calcular,
        bg=COLOR_SUCCESS,
        fg="#000000",
        font=("Helvetica", 11, "bold"),
        cursor="hand2",
        padx=20,
        pady=8,
        activebackground="#FFEB3B",
        activeforeground="#000000",
    ).grid(row=8, column=0, columnspan=4, pady=12)

    actualizar_campos()
    actualizar_criterio()
