"""Mixin con ventanas de estadistica inferencial para MenuPrincipal."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from math import comb

from config_interfaz import *
from estadistica_inferencial.probabilidades import ProbabilidadesElementales
from estadistica_inferencial.distribuciones import DistribucionBernoulli, DistribucionBinomial
from estadistica_inferencial.distribucion_normal import DistribucionNormal
from estadistica_inferencial.distribucion_poisson import DistribucionPoisson
from estadistica_inferencial.bayes import TeoremaBayes
from estadistica_inferencial.regresion_correlacion import CorrelacionLineal, RegresionLinealSimple, RegresionNoLineal
from estadistica_inferencial.diagramas_arbol import DiagramaArbol
from estadistica_inferencial.chi_cuadrado import PruebaChiCuadrado


class MenuInferencialMixin:
    def abrir_probabilidades(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("🎲 Cálculo de Probabilidades Elementales")
        
        # Obtener dimensiones de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        
        # Configurar ventana
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        ventana.configure(bg=BG_LIGHT)
        
        # ===== CREAR CANVAS PRINCIPAL CON SCROLL =====
        # Frame contenedor principal
        main_container = tk.Frame(ventana, bg=BG_LIGHT)
        main_container.pack(fill='both', expand=True)
        
        # Canvas para scroll
        main_canvas = tk.Canvas(main_container, bg=BG_LIGHT, highlightthickness=0)
        main_canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=main_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(main_canvas, bg=BG_LIGHT)
        
        # Crear ventana en el canvas
        canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        
        # Función para actualizar el scroll region
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox('all'))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        
        # Hacer que el frame scrollable se expanda al ancho del canvas
        def configure_canvas_width(event):
            main_canvas.itemconfig(canvas_window, width=event.width)
        
        main_canvas.bind('<Configure>', configure_canvas_width)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para diferentes sistemas operativos
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac
        main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        prob = ProbabilidadesElementales()
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  🎲 CÁLCULO DE PROBABILIDADES ELEMENTALES                            ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 PASO 1: Define el Espacio Muestral
   → Ingresa todos los resultados posibles separados por comas
   → Ejemplo: 1, 2, 3, 4, 5, 6 (para un dado)
   
🔹 PASO 2: Define Eventos
   → Nombre del evento (ej: "Par")
   → Elementos del evento (ej: 2, 4, 6)
   → Click en "Definir Evento"
   
🔹 PASO 3: Calcula Operaciones
   → Unión de eventos (A ∪ B)
   → Intersección de eventos (A ∩ B)
   → Complemento de un evento (A')

💡 TIP: Puedes definir varios eventos y combinarlos
        """
        
        frame_inst = tk.Frame(scrollable_frame, bg="#E8EAF6")
        frame_inst.pack(fill='x', padx=10, pady=(10, 0))
        
        tk.Label(
            frame_inst,
            text=instrucciones_text,
            bg="#E8EAF6",
            fg="#283593",
            font=("Consolas", 9),
            justify='left',
            anchor='w'
        ).pack(padx=15, pady=15)
        
        # Frame superior para inputs
        frame_input = tk.LabelFrame(scrollable_frame, text="Definir Espacio Muestral y Eventos", 
                                     padx=10, pady=10, bg=BG_LIGHT)
        frame_input.pack(fill='x', padx=10, pady=10)
        
        # Espacio muestral
        tk.Label(frame_input, text="Espacio Muestral (sep. por coma):", bg=BG_LIGHT).grid(row=0, column=0, sticky='w')
        entry_espacio = tk.Entry(frame_input, width=60)
        entry_espacio.grid(row=0, column=1, padx=5)
        
        def def_espacio():
            elementos = [x.strip() for x in entry_espacio.get().split(',')]
            prob.definir_espacio_muestral(elementos)
            messagebox.showinfo("Éxito", f"Espacio muestral: {elementos}")
        
        tk.Button(frame_input, text="Definir", command=def_espacio, bg=COLOR_SUCCESS, fg="#000000", font=("Helvetica", 10, "bold"), activebackground="#FFEB3B", activeforeground="#000000").grid(row=0, column=2, padx=5)
        
        # Definir evento
        tk.Label(frame_input, text="Nombre Evento:", bg=BG_LIGHT).grid(row=1, column=0, sticky='w', pady=5)
        entry_nombre = tk.Entry(frame_input, width=20)
        entry_nombre.grid(row=1, column=1, sticky='w', padx=5)
        
        tk.Label(frame_input, text="Elementos (sep. por coma):", bg=BG_LIGHT).grid(row=2, column=0, sticky='w')
        entry_elementos = tk.Entry(frame_input, width=60)
        entry_elementos.grid(row=2, column=1, padx=5)
        
        def def_evento():
            nombre = entry_nombre.get()
            elementos = [x.strip() for x in entry_elementos.get().split(',')]
            try:
                prob.definir_evento(nombre, elementos)
                messagebox.showinfo("Éxito", f"Evento '{nombre}' definido")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(frame_input, text="Definir Evento", command=def_evento, bg=COLOR_INFO, fg="#000000", font=("Helvetica", 10, "bold"), activebackground="#FFEB3B", activeforeground="#000000").grid(row=2, column=2, padx=5)
        
        # Área de resultados
        text_prob = scrolledtext.ScrolledText(scrollable_frame, height=25, width=120)
        text_prob.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botones de cálculo
        frame_calc = tk.Frame(scrollable_frame, bg=BG_LIGHT)
        frame_calc.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_calc, text="Evento A:", bg=BG_LIGHT).grid(row=0, column=0)
        entry_a = tk.Entry(frame_calc, width=15)
        entry_a.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_calc, text="Evento B:", bg=BG_LIGHT).grid(row=0, column=2)
        entry_b = tk.Entry(frame_calc, width=15)
        entry_b.grid(row=0, column=3, padx=5)
        
        def calc_simple():
            try:
                res = prob.probabilidad_simple(entry_a.get())
                text_prob.insert(tk.END, f"\nP({entry_a.get()}) = {res}\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def calc_union():
            try:
                a, b = entry_a.get(), entry_b.get()
                if prob.eventos_excluyentes(a, b):
                    res = prob.probabilidad_union_excluyentes(a, b)
                else:
                    res = prob.probabilidad_union_no_excluyentes(a, b)
                text_prob.insert(tk.END, f"\nP({a} ∪ {b}) = {res}\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(frame_calc, text="P(A)", command=calc_simple, bg=COLOR_PRIMARY, fg="#000000", font=("Helvetica", 10, "bold"), activebackground="#FFEB3B", activeforeground="#000000").grid(row=1, column=0, pady=5)
        tk.Button(frame_calc, text="P(A ∪ B)", command=calc_union, bg=COLOR_SECONDARY, fg="#000000", font=("Helvetica", 10, "bold"), activebackground="#FFEB3B", activeforeground="#000000").grid(row=1, column=1, pady=5)
    
    def abrir_bayes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("🔄 Teorema de Bayes")
        
        # Obtener dimensiones de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        
        # Configurar ventana
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.8)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # ===== CREAR CANVAS PRINCIPAL CON SCROLL =====
        # Frame contenedor principal
        main_container = tk.Frame(ventana, bg=BG_LIGHT)
        main_container.pack(fill='both', expand=True)
        
        # Canvas para scroll
        main_canvas = tk.Canvas(main_container, bg=BG_LIGHT, highlightthickness=0)
        main_canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=main_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(main_canvas, bg=BG_LIGHT)
        
        # Crear ventana en el canvas
        canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        
        # Función para actualizar el scroll region
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox('all'))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        
        # Hacer que el frame scrollable se expanda al ancho del canvas
        def configure_canvas_width(event):
            main_canvas.itemconfig(canvas_window, width=event.width)
        
        main_canvas.bind('<Configure>', configure_canvas_width)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para diferentes sistemas operativos
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac
        main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        tk.Label(scrollable_frame, text="📊 Teorema de Bayes", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  🔄 TEOREMA DE BAYES - PROBABILIDAD CONDICIONAL                      ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 DEFINICIÓN:
   P(A|B) = [P(B|A) × P(A)] / P(B)
   
🔹 DATOS REQUERIDOS:
   → P(A): Probabilidad a priori del evento A
   → P(B|A): Probabilidad de B dado que ocurrió A
   → P(B|¬A): Probabilidad de B dado que NO ocurrió A
   
🔹 RESULTADO:
   → P(A|B): Probabilidad de A dado que ocurrió B
   → P(B): Probabilidad total de B

💡 EJEMPLO: Test médico
   A = "Tiene la enfermedad"
   B = "Test positivo"
   P(A|B) = "¿Qué probabilidad de tener la enfermedad si el test es positivo?"
        """
        
        frame_inst = tk.Frame(scrollable_frame, bg="#FFF3E0")
        frame_inst.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            frame_inst,
            text=instrucciones_text,
            bg="#FFF3E0",
            fg="#E65100",
            font=("Consolas", 9),
            justify='left',
            anchor='w'
        ).pack(padx=15, pady=15)
        
        frame = tk.Frame(scrollable_frame)
        frame.pack(padx=20, pady=10)
        
        tk.Label(frame, text="P(A):").grid(row=0, column=0)
        entry_pa = tk.Entry(frame)
        entry_pa.grid(row=0, column=1)
        
        tk.Label(frame, text="P(B|A):").grid(row=1, column=0)
        entry_pba = tk.Entry(frame)
        entry_pba.grid(row=1, column=1)
        
        tk.Label(frame, text="P(B|¬A):").grid(row=2, column=0)
        entry_pbna = tk.Entry(frame)
        entry_pbna.grid(row=2, column=1)
        
        text_result = scrolledtext.ScrolledText(scrollable_frame, height=20, width=80)
        text_result.pack(padx=20, pady=10)
        
        def calcular():
            try:
                pa = float(entry_pa.get())
                pba = float(entry_pba.get())
                pbna = float(entry_pbna.get())
                
                pb = (pba * pa) + (pbna * (1 - pa))
                pab = (pba * pa) / pb
                
                result = f"{'='*60}\nTEOREMA DE BAYES\n{'='*60}\n\n"
                result += f"P(A) = {pa}\n"
                result += f"P(B|A) = {pba}\n"
                result += f"P(B|¬A) = {pbna}\n\n"
                result += f"P(B) = {pb:.4f}\n"
                result += f"P(A|B) = {pab:.4f} ({pab*100:.2f}%)\n"
                
                text_result.delete("1.0", tk.END)
                text_result.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(scrollable_frame, text="Calcular", command=calcular, bg=COLOR_SUCCESS, 
                 fg="#000000", font=FONT_BUTTON, activebackground="#FFEB3B", activeforeground="#000000").pack(pady=10)
    
    def abrir_distribuciones(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("📊 Distribuciones de Probabilidad")
        
        # Obtener dimensiones de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        
        # Configurar ventana
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # ===== CREAR CANVAS PRINCIPAL CON SCROLL =====
        # Frame contenedor principal
        main_container = tk.Frame(ventana, bg=BG_LIGHT)
        main_container.pack(fill='both', expand=True)
        
        # Canvas para scroll
        main_canvas = tk.Canvas(main_container, bg=BG_LIGHT, highlightthickness=0)
        main_canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=main_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(main_canvas, bg=BG_LIGHT)
        
        # Crear ventana en el canvas
        canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        
        # Función para actualizar el scroll region
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox('all'))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        
        # Hacer que el frame scrollable se expanda al ancho del canvas
        def configure_canvas_width(event):
            main_canvas.itemconfig(canvas_window, width=event.width)
        
        main_canvas.bind('<Configure>', configure_canvas_width)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para diferentes sistemas operativos
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac
        main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        tk.Label(scrollable_frame, text="📊 Distribuciones de Probabilidad", 
                font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📊 DISTRIBUCIONES DE PROBABILIDAD                                   ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 DISTRIBUCIONES DISPONIBLES:
   → BINOMIAL: Número de éxitos en n ensayos independientes
   → NORMAL: Variables continuas con forma de campana
   → POISSON: Número de eventos en un intervalo fijo

🔹 CÓMO USAR:
   → Selecciona una pestaña según el tipo de distribución
   → Ingresa los parámetros requeridos
   → Presiona "Calcular" para obtener probabilidades
   → Presiona "Graficar" para ver visualizaciones

💡 APLICACIONES:
   • Binomial: Control de calidad, encuestas
   • Normal: Alturas, pesos, calificaciones
   • Poisson: Llamadas telefónicas, accidentes, defectos
        """
        
        frame_inst = tk.Frame(scrollable_frame, bg="#F3E5F5")
        frame_inst.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            frame_inst,
            text=instrucciones_text,
            bg="#F3E5F5",
            fg="#6A1B9A",
            font=("Consolas", 9),
            justify='left',
            anchor='w'
        ).pack(padx=15, pady=15)
        
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab Binomial
        tab_binom = tk.Frame(notebook)
        notebook.add(tab_binom, text="Binomial")
        
        tk.Label(tab_binom, text="Distribución Binomial", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        frame_binom = tk.Frame(tab_binom)
        frame_binom.pack(pady=10)
        
        tk.Label(frame_binom, text="n (ensayos):").grid(row=0, column=0)
        entry_n = tk.Entry(frame_binom)
        entry_n.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_binom, text="p (éxito):").grid(row=1, column=0)
        entry_p = tk.Entry(frame_binom)
        entry_p.grid(row=1, column=1, padx=5)
        
        tk.Label(frame_binom, text="k (éxitos):").grid(row=2, column=0)
        entry_k = tk.Entry(frame_binom)
        entry_k.grid(row=2, column=1, padx=5)
        
        text_binom = scrolledtext.ScrolledText(tab_binom, height=20, width=100)
        text_binom.pack(padx=10, pady=10)
        
        def calc_binomial():
            try:
                n = int(entry_n.get())
                p = float(entry_p.get())
                k = int(entry_k.get())
                
                binom = DistribucionBinomial(n, p)
                resultado = binom.probabilidad(k)
                stats = binom.estadisticas()
                
                text = f"{'='*60}\nDISTRIBUCIÓN BINOMIAL\n{'='*60}\n\n"
                text += f"Parámetros: n={n}, p={p}\n\n"
                text += f"PROBABILIDAD:\n"
                text += f"P(X = {k}) = {resultado['probabilidad']:.6f}\n"
                text += f"Porcentaje: {resultado['porcentaje']}%\n"
                text += f"\nFórmula: {resultado['formula']}\n\n"
                text += f"ESTADÍSTICAS:\n"
                text += f"Media: {stats['media']:.4f}\n"
                text += f"Varianza: {stats['varianza']:.4f}\n"
                text += f"Desv. Estándar: {stats['desviacion_estandar']:.4f}\n"
                text += f"Moda: {stats['moda']}\n"
                
                text_binom.delete("1.0", tk.END)
                text_binom.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def graficar_binomial():
            try:
                n = int(entry_n.get())
                p = float(entry_p.get())
                
                binom = DistribucionBinomial(n, p)
                fig = binom.graficar(figsize=(14, 8))
                
                # Mostrar en ventana nueva
                ventana_graf = tk.Toplevel(ventana)
                ventana_graf.title("Gráficas - Distribución Binomial")
                ventana_graf.geometry("1200x700")
                
                canvas = FigureCanvasTkAgg(fig, master=ventana_graf)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
                toolbar = NavigationToolbar2Tk(canvas, ventana_graf)
                toolbar.update()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        frame_botones_binom = tk.Frame(tab_binom)
        frame_botones_binom.pack(pady=5)
        
        tk.Button(frame_botones_binom, text="📊 Calcular", command=calc_binomial, 
                 bg=COLOR_PRIMARY, fg="#000000", font=FONT_BUTTON, activebackground="#FFEB3B", activeforeground="#000000").pack(side='left', padx=5)
        
        tk.Button(frame_botones_binom, text="📈 Ver Gráficas", command=graficar_binomial,
                 bg=COLOR_SUCCESS, fg="#000000", font=FONT_BUTTON, activebackground="#FFEB3B", activeforeground="#000000").pack(side='left', padx=5)
        
        # Tab Normal
        tab_normal = tk.Frame(notebook)
        notebook.add(tab_normal, text="Normal")
        
        tk.Label(tab_normal, text="Distribución Normal", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        frame_normal = tk.Frame(tab_normal)
        frame_normal.pack(pady=10)
        
        tk.Label(frame_normal, text="μ (media):").grid(row=0, column=0)
        entry_mu = tk.Entry(frame_normal)
        entry_mu.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_normal, text="σ (desv):").grid(row=1, column=0)
        entry_sigma = tk.Entry(frame_normal)
        entry_sigma.grid(row=1, column=1, padx=5)
        
        tk.Label(frame_normal, text="x:").grid(row=2, column=0)
        entry_x = tk.Entry(frame_normal)
        entry_x.grid(row=2, column=1, padx=5)
        
        text_normal = scrolledtext.ScrolledText(tab_normal, height=20, width=100)
        text_normal.pack(padx=10, pady=10)
        
        def calc_normal():
            try:
                mu = float(entry_mu.get())
                sigma = float(entry_sigma.get())
                x = float(entry_x.get())
                
                normal = DistribucionNormal(mu, sigma)
                prob_menor = normal.probabilidad_menor(x)
                prob_mayor = normal.probabilidad_mayor(x)
                stats = normal.estadisticas()
                
                text = f"{'='*60}\nDISTRIBUCIÓN NORMAL\n{'='*60}\n\n"
                text += f"Parámetros: μ={mu}, σ={sigma}\n\n"
                text += f"PROBABILIDADES:\n"
                text += f"P(X < {x}) = {prob_menor['probabilidad']:.6f} ({prob_menor['porcentaje']}%)\n"
                text += f"P(X > {x}) = {prob_mayor['probabilidad']:.6f} ({prob_mayor['porcentaje']}%)\n\n"
                text += f"ESTADÍSTICAS:\n"
                text += f"Media: {stats['media']}\n"
                text += f"Mediana: {stats['mediana']}\n"
                text += f"Desv. Estándar: {stats['desviacion_estandar']}\n"
                text += f"Varianza: {stats['varianza']}\n"
                
                text_normal.delete("1.0", tk.END)
                text_normal.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def graficar_normal():
            try:
                mu = float(entry_mu.get())
                sigma = float(entry_sigma.get())
                
                normal = DistribucionNormal(mu, sigma)
                
                # Crear figura con 3 subgráficas
                fig, axes = plt.subplots(1, 3, figsize=(16, 5))
                fig.suptitle(f'Distribución Normal: μ={mu}, σ={sigma}', 
                           fontsize=16, fontweight='bold')
                
                # Gráfica 1: Densidad básica
                normal.graficar_densidad(ax=axes[0])
                
                # Gráfica 2: Con área sombreada (si hay x)
                if entry_x.get():
                    x_val = float(entry_x.get())
                    normal.graficar_densidad(ax=axes[1], 
                                           mostrar_areas={'a': x_val})
                    axes[1].set_title(f'Área P(X ≤ {x_val})')
                else:
                    normal.graficar_densidad(ax=axes[1])
                
                # Gráfica 3: Regla empírica
                normal.graficar_regla_empirica(ax=axes[2])
                
                plt.tight_layout()
                
                # Mostrar en ventana nueva
                ventana_graf = tk.Toplevel(ventana)
                ventana_graf.title("Gráficas - Distribución Normal")
                ventana_graf.geometry("1400x600")
                
                canvas = FigureCanvasTkAgg(fig, master=ventana_graf)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
                toolbar = NavigationToolbar2Tk(canvas, ventana_graf)
                toolbar.update()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        frame_botones_normal = tk.Frame(tab_normal)
        frame_botones_normal.pack(pady=5)
        
        tk.Button(frame_botones_normal, text="📊 Calcular", command=calc_normal, 
                 bg=COLOR_SECONDARY, fg="#000000", font=FONT_BUTTON, activebackground="#FFEB3B", activeforeground="#000000").pack(side='left', padx=5)
        
        tk.Button(frame_botones_normal, text="📈 Ver Gráficas", command=graficar_normal,
                 bg=COLOR_SUCCESS, fg="#000000", font=FONT_BUTTON, activebackground="#FFEB3B", activeforeground="#000000").pack(side='left', padx=5)
        
        # Tab Poisson
        tab_poisson = tk.Frame(notebook)
        notebook.add(tab_poisson, text="Poisson")
        
        tk.Label(tab_poisson, text="Distribución de Poisson", font=("Helvetica", 14, "bold")).pack(pady=10)

        frame_poisson = tk.Frame(tab_poisson)
        frame_poisson.pack(pady=10)
        
        tk.Label(frame_poisson, text="λ (lambda):").grid(row=0, column=0)
        entry_lambda = tk.Entry(frame_poisson)
        entry_lambda.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_poisson, text="k (eventos):").grid(row=1, column=0)
        entry_k_poisson = tk.Entry(frame_poisson)
        entry_k_poisson.grid(row=1, column=1, padx=5)
        
        text_poisson = scrolledtext.ScrolledText(tab_poisson, height=20, width=100)
        text_poisson.pack(padx=10, pady=10)
        
        def calc_poisson():
            try:
                lambd = float(entry_lambda.get())
                k = int(entry_k_poisson.get())
                
                poisson = DistribucionPoisson(lambd)
                resultado = poisson.probabilidad(k)
                stats = poisson.estadisticas()
                
                text = f"{'='*60}\nDISTRIBUCIÓN DE POISSON\n{'='*60}\n\n"
                text += f"Parámetro: λ={lambd}\n\n"
                text += f"PROBABILIDAD:\n"
                text += f"P(X = {k}) = {resultado['probabilidad']:.6f}\n"
                text += f"Porcentaje: {resultado['porcentaje']}%\n"
                text += f"\nFórmula: {resultado['formula']}\n\n"
                text += f"ESTADÍSTICAS:\n"
                text += f"Media: {stats['media']:.4f}\n"
                text += f"Varianza: {stats['varianza']:.4f}\n"
                text += f"Desv. Estándar: {stats['desviacion_estandar']:.4f}\n"
                
                text_poisson.delete("1.0", tk.END)
                text_poisson.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def graficar_poisson():
            try:
                lambd = float(entry_lambda.get())
                
                poisson = DistribucionPoisson(lambd)
                
                # Crear figura con 2 subgráficas
                fig, axes = plt.subplots(1, 2, figsize=(14, 6))
                fig.suptitle(f'Distribución de Poisson: λ={lambd}', 
                           fontsize=16, fontweight='bold')
                
                # Gráfica 1: Probabilidades
                poisson.graficar_probabilidades(ax=axes[0])
                
                # Gráfica 2: Acumulada
                poisson.graficar_acumulada(ax=axes[1])
                
                plt.tight_layout()
                
                # Mostrar en ventana nueva
                ventana_graf = tk.Toplevel(ventana)
                ventana_graf.title("Gráficas - Distribución de Poisson")
                ventana_graf.geometry("1200x600")
                
                canvas = FigureCanvasTkAgg(fig, master=ventana_graf)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
                toolbar = NavigationToolbar2Tk(canvas, ventana_graf)
                toolbar.update()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        frame_botones_poisson = tk.Frame(tab_poisson)
        frame_botones_poisson.pack(pady=5)
        
        tk.Button(frame_botones_poisson, text="📊 Calcular", command=calc_poisson, 
                 bg=COLOR_INFO, fg="#000000", font=FONT_BUTTON, activebackground="#FFEB3B", activeforeground="#000000").pack(side='left', padx=5)
        
        tk.Button(frame_botones_poisson, text="📈 Ver Gráficas", command=graficar_poisson,
                 bg=COLOR_SUCCESS, fg="#000000", font=FONT_BUTTON, activebackground="#FFEB3B", activeforeground="#000000").pack(side='left', padx=5)
    
    def abrir_regresion(self):
        """Regresión y Correlación Simple"""
        ventana = VentanaAnalisis(self.root, "📈 Correlación y Regresión Simple")
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📈 CORRELACIÓN Y REGRESIÓN LINEAL SIMPLE                            ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 PASO 1: Carga tus datos
   → Click en "📁 Cargar CSV" (debe tener al menos 2 columnas numéricas)
   
🔹 PASO 2: Analiza los datos
   → Click en "▶️ ANALIZAR REGRESIÓN"
   → Selecciona Variable X (independiente)
   → Selecciona Variable Y (dependiente)
   
📊 QUÉ VERÁS:
   ✓ Coeficiente de Correlación de Pearson (r)
   ✓ Coeficiente de Determinación (R²)
   ✓ Ecuación de Regresión Lineal (y = a + bx)
   ✓ Comparación con modelos no lineales
   ✓ Gráficos de dispersión con línea de tendencia

📈 INTERPRETACIÓN:
   • r cercano a +1 → Correlación positiva fuerte
   • r cercano a -1 → Correlación negativa fuerte
   • r cercano a 0 → Sin correlación lineal
   • R² indica % de variabilidad explicada por el modelo

💡 TIP: Usa datos de "datos_regresion_estudio.csv" para probar
        """
        
        crear_panel_instrucciones(
            ventana.text_frame,
            "INSTRUCCIONES DE USO",
            instrucciones_text,
            color_bg="#FFF3E0",
            color_fg="#E65100",
            color_texto="#BF360C"
        )
        
        def analizar_regresion():
            """Función para analizar regresión después de cargar datos"""
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "❌ Primero debe cargar un archivo CSV")
                return
            
            # Seleccionar columnas
            columnas = list(ventana.datos.columns)
            
            # Filtrar solo columnas numéricas
            columnas_numericas = []
            for col in columnas:
                try:
                    pd.to_numeric(ventana.datos[col], errors='raise')
                    columnas_numericas.append(col)
                except:
                    pass
            
            if len(columnas_numericas) < 2:
                messagebox.showerror("Error", 
                    "❌ Se necesitan al menos 2 columnas numéricas para regresión.\n\n"
                    f"Columnas disponibles: {', '.join(columnas)}\n"
                    f"Columnas numéricas: {', '.join(columnas_numericas) if columnas_numericas else 'Ninguna'}")
                return
            
            ventana_seleccion = tk.Toplevel(ventana)
            ventana_seleccion.title("Seleccionar Variables")
            ventana_seleccion.geometry("500x400")
            
            # Centrar ventana
            ventana_seleccion.update_idletasks()
            x = (ventana_seleccion.winfo_screenwidth() // 2) - (500 // 2)
            y = (ventana_seleccion.winfo_screenheight() // 2) - (400 // 2)
            ventana_seleccion.geometry(f"500x400+{x}+{y}")
            
            tk.Label(
                ventana_seleccion, 
                text="🎯 Selecciona las Variables",
                font=("Helvetica", 14, "bold"),
                fg=COLOR_PRIMARY
            ).pack(pady=15)
            
            frame_vars = tk.Frame(ventana_seleccion)
            frame_vars.pack(pady=10)
            
            tk.Label(frame_vars, text="Variable X (independiente):", 
                    font=("Helvetica", 11, "bold")).grid(row=0, column=0, sticky='w', pady=10, padx=10)
            combo_x = ttk.Combobox(frame_vars, values=columnas_numericas, width=25, font=("Helvetica", 10))
            combo_x.grid(row=0, column=1, pady=10, padx=10)
            if columnas_numericas:
                combo_x.set(columnas_numericas[0])
            
            tk.Label(frame_vars, text="Variable Y (dependiente):", 
                    font=("Helvetica", 11, "bold")).grid(row=1, column=0, sticky='w', pady=10, padx=10)
            combo_y = ttk.Combobox(frame_vars, values=columnas_numericas, width=25, font=("Helvetica", 10))
            combo_y.grid(row=1, column=1, pady=10, padx=10)
            if len(columnas_numericas) > 1:
                combo_y.set(columnas_numericas[1])
            
            # Información
            info_text = "📊 La variable X es la que usas para predecir\n" \
                       "📈 La variable Y es la que quieres predecir\n" \
                       "Ejemplo: X=Horas de Estudio, Y=Calificación"
            tk.Label(
                ventana_seleccion,
                text=info_text,
                font=("Helvetica", 9),
                fg="#1976D2",
                justify='left'
            ).pack(pady=10)
            
            def calcular_regresion():
                try:
                    col_x = combo_x.get()
                    col_y = combo_y.get()
                    
                    if not col_x or not col_y:
                        messagebox.showwarning("Advertencia", "❌ Seleccione ambas variables")
                        return
                    
                    if col_x == col_y:
                        messagebox.showwarning("Advertencia", "❌ Las variables X e Y deben ser diferentes")
                        return
                    
                    x = ventana.datos[col_x].dropna()
                    y = ventana.datos[col_y].dropna()
                    
                    # Asegurar que tenemos pares completos
                    indices_comunes = x.index.intersection(y.index)
                    x = x.loc[indices_comunes]
                    y = y.loc[indices_comunes]
                    
                    if len(x) < 2:
                        messagebox.showerror("Error", "❌ Se necesitan al menos 2 pares de datos válidos")
                        return
                    
                    # Correlación
                    corr = CorrelacionLineal(x, y)
                    resultado_corr = corr.coeficiente_correlacion_pearson()
                    
                    # Regresión Lineal
                    reg_lineal = RegresionLinealSimple(x, y)
                    ecuacion = reg_lineal.ecuacion()
                    resumen = reg_lineal.resumen_estadistico()
                    
                    # Regresión No Lineal
                    reg_no_lineal = RegresionNoLineal(x, y)
                    comparacion = reg_no_lineal.comparar_modelos()
                    
                    # ============= FORMATEAR RESULTADOS CON ESTILO =============
                    texto = ""
                    
                    texto += "╔" + "═" * 98 + "╗\n"
                    texto += "║" + " " * 25 + "📈 ANÁLISIS DE CORRELACIÓN Y REGRESIÓN" + " " * 35 + "║\n"
                    texto += "╚" + "═" * 98 + "╝\n\n"
                    
                    texto += f"📊 Variables analizadas:\n"
                    texto += f"   • Variable X (independiente): {col_x}\n"
                    texto += f"   • Variable Y (dependiente):   {col_y}\n"
                    texto += f"   • Número de observaciones:    {len(x)}\n\n"
                    
                    texto += "╔" + "═" * 98 + "╗\n"
                    texto += "║" + " " * 38 + "📊 CORRELACIÓN" + " " * 45 + "║\n"
                    texto += "╚" + "═" * 98 + "╝\n\n"
                    
                    texto += f"  🔢 Coeficiente de Pearson (r):     {resultado_corr['r']:.6f}\n"
                    texto += f"  📈 R² (coef. determinación):       {resultado_corr['r_cuadrado']:.6f}\n"
                    texto += f"  📊 Interpretación:                 {resultado_corr['interpretacion']}\n"
                    texto += f"  ✅ Significativo:                  {'Sí' if resultado_corr['significativo'] else 'No'} "
                    texto += f"(p-valor = {resultado_corr['p_valor']:.6f})\n\n"
                    
                    texto += "  💡 INTERPRETACIÓN DE r:\n"
                    r_abs = abs(resultado_corr['r'])
                    if r_abs >= 0.9:
                        texto += f"     → Correlación MUY FUERTE ({'positiva' if resultado_corr['r'] > 0 else 'negativa'})\n"
                    elif r_abs >= 0.7:
                        texto += f"     → Correlación FUERTE ({'positiva' if resultado_corr['r'] > 0 else 'negativa'})\n"
                    elif r_abs >= 0.5:
                        texto += f"     → Correlación MODERADA ({'positiva' if resultado_corr['r'] > 0 else 'negativa'})\n"
                    elif r_abs >= 0.3:
                        texto += f"     → Correlación DÉBIL ({'positiva' if resultado_corr['r'] > 0 else 'negativa'})\n"
                    else:
                        texto += f"     → Correlación MUY DÉBIL o nula\n"
                    
                    texto += "\n╔" + "═" * 98 + "╗\n"
                    texto += "║" + " " * 30 + "📈 REGRESIÓN LINEAL SIMPLE" + " " * 41 + "║\n"
                    texto += "╚" + "═" * 98 + "╝\n\n"
                    
                    texto += f"  📐 Ecuación de regresión:          {ecuacion['ecuacion']}\n"
                    texto += f"  📍 Intercepto (a):                 {ecuacion['a_intercepto']:.6f}\n"
                    texto += f"  📏 Pendiente (b):                  {ecuacion['b_pendiente']:.6f}\n"
                    texto += f"  📊 R² (determinación):             {resumen['r2_determinacion']:.6f} ({resumen['r2_porcentaje']})\n"
                    texto += f"  📉 RMSE (error cuadrático):        {resumen['rmse']:.6f}\n\n"
                    
                    texto += f"  💡 {resumen['interpretacion_r2']}\n\n"
                    
                    texto += "  🎯 INTERPRETACIÓN DE LA ECUACIÓN:\n"
                    texto += f"     • Intercepto (a = {ecuacion['a_intercepto']:.4f}): Valor de Y cuando X = 0\n"
                    if ecuacion['b_pendiente'] > 0:
                        texto += f"     • Pendiente (b = {ecuacion['b_pendiente']:.4f}): Por cada unidad que aumenta X,\n"
                        texto += f"       Y aumenta en {ecuacion['b_pendiente']:.4f} unidades\n"
                    else:
                        texto += f"     • Pendiente (b = {ecuacion['b_pendiente']:.4f}): Por cada unidad que aumenta X,\n"
                        texto += f"       Y disminuye en {abs(ecuacion['b_pendiente']):.4f} unidades\n"
                    
                    texto += "\n╔" + "═" * 98 + "╗\n"
                    texto += "║" + " " * 32 + "🔍 COMPARACIÓN DE MODELOS" + " " * 40 + "║\n"
                    texto += "╚" + "═" * 98 + "╝\n\n"
                    
                    texto += f"  🏆 Mejor modelo:                   {comparacion['mejor_modelo']}\n"
                    texto += f"  📈 R² del mejor modelo:            {comparacion['mejor_r2']:.6f}\n"
                    texto += f"  📐 Ecuación:                       {comparacion['mejor_ecuacion']}\n\n"
                    texto += f"  💡 {comparacion['recomendacion']}\n\n"
                    
                    texto += "  📊 TODOS LOS MODELOS COMPARADOS:\n"
                    for nombre, datos in comparacion['modelos'].items():
                        texto += f"     • {nombre:<25} R² = {datos['r2']:.6f}\n"
                    
                    ventana.mostrar_texto(texto)
                    
                    # ============= MOSTRAR GRÁFICOS DE MANERA ORDENADA =============
                    try:
                        # Cerrar ventana de selección
                        ventana_seleccion.destroy()
                        
                        # 1. Gráfico de Correlación (dispersión simple)
                        fig_corr = corr.graficar_correlacion()
                        
                        # Mostrar en ventana nueva
                        ventana_graf_corr = tk.Toplevel(ventana)
                        ventana_graf_corr.title("📊 Gráfico de Correlación")
                        ventana_graf_corr.geometry("900x700")
                        
                        canvas_corr = FigureCanvasTkAgg(fig_corr, master=ventana_graf_corr)
                        canvas_corr.draw()
                        canvas_corr.get_tk_widget().pack(fill='both', expand=True)
                        
                        toolbar_corr = NavigationToolbar2Tk(canvas_corr, ventana_graf_corr)
                        toolbar_corr.update()
                        
                        # 2. Gráfico de Regresión Lineal Simple
                        fig_reg = reg_lineal.graficar()
                        
                        ventana_graf_reg = tk.Toplevel(ventana)
                        ventana_graf_reg.title("📈 Regresión Lineal Simple")
                        ventana_graf_reg.geometry("900x700")
                        
                        canvas_reg = FigureCanvasTkAgg(fig_reg, master=ventana_graf_reg)
                        canvas_reg.draw()
                        canvas_reg.get_tk_widget().pack(fill='both', expand=True)
                        
                        toolbar_reg = NavigationToolbar2Tk(canvas_reg, ventana_graf_reg)
                        toolbar_reg.update()
                        
                        # 3. Comparación COMPLETA de 4 modelos (en la ventana principal)
                        fig_comp = reg_no_lineal.graficar_comparacion()
                        ventana.mostrar_grafico(fig_comp)
                        
                        # 3. Comparación COMPLETA de 4 modelos (en la ventana principal)
                        fig_comp = reg_no_lineal.graficar_comparacion()
                        ventana.mostrar_grafico(fig_comp)
                        
                        # Mensaje informativo
                        messagebox.showinfo(
                            "📊 Análisis Completo",
                            "✅ Se han generado 3 gráficos:\n\n"
                            "1️⃣ CORRELACIÓN\n"
                            "   • Diagrama de dispersión\n"
                            "   • Coeficiente de Pearson (r)\n\n"
                            "2️⃣ REGRESIÓN LINEAL\n"
                            "   • Dispersión con línea de ajuste\n"
                            "   • Ecuación: y = a + bx\n\n"
                            "3️⃣ COMPARACIÓN DE MODELOS\n"
                            "   • 4 modelos de regresión\n"
                            "   • Comparación de R²\n"
                            "   • Resumen de ecuaciones"
                        )
                        
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        messagebox.showerror("Error", f"❌ Error al generar gráficos:\n\n{str(e)}")
                    
                    ventana_seleccion.destroy()
                    
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    messagebox.showerror("Error", f"❌ Error en el análisis:\n\n{str(e)}")
            
            # Botones
            frame_botones = tk.Frame(ventana_seleccion)
            frame_botones.pack(pady=20)
            
            tk.Button(
                frame_botones, 
                text="📊 Calcular Regresión", 
                command=calcular_regresion,
                bg="#4CAF50",
                fg="#000000",
                font=("Helvetica", 12, "bold"),
                width=20,
                height=2,
                cursor="hand2",
                relief="raised",
                borderwidth=3,
                activebackground="#66BB6A",
                activeforeground="#000000"
            ).pack(side='left', padx=5)
            
            tk.Button(
                frame_botones,
                text="❌ Cancelar",
                command=ventana_seleccion.destroy,
                bg="#E53935",
                fg="#000000",
                font=("Helvetica", 12, "bold"),
                width=15,
                height=2,
                cursor="hand2",
                relief="raised",
                borderwidth=3,
                activebackground="#FFEB3B",
                activeforeground="#000000"
            ).pack(side='left', padx=5)
        
        # Botón principal de análisis
        btn_analizar = tk.Button(
            ventana.btn_frame,
            text="▶️ ANALIZAR REGRESIÓN",
            command=analizar_regresion,
            bg="#4CAF50",
            fg="#000000",
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
            width=25,
            height=2,
            relief="raised",
            borderwidth=3,
            activebackground="#66BB6A",
            activeforeground="#000000"
        )
        btn_analizar.pack(pady=15)
    
    def abrir_arboles(self):
        """Árboles de Probabilidad"""
        ventana = tk.Toplevel(self.root)
        ventana.title("🌳 Árboles de Decisión - Probabilidades")
        
        # Obtener dimensiones de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        
        # Configurar ventana
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # ===== CREAR CANVAS PRINCIPAL CON SCROLL =====
        # Frame contenedor principal
        main_container = tk.Frame(ventana, bg=BG_LIGHT)
        main_container.pack(fill='both', expand=True)
        
        # Canvas para scroll
        main_canvas = tk.Canvas(main_container, bg=BG_LIGHT, highlightthickness=0)
        main_canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=main_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(main_canvas, bg=BG_LIGHT)
        
        # Crear ventana en el canvas
        canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        
        # Función para actualizar el scroll region
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox('all'))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        
        # Hacer que el frame scrollable se expanda al ancho del canvas
        def configure_canvas_width(event):
            main_canvas.itemconfig(canvas_window, width=event.width)
        
        main_canvas.bind('<Configure>', configure_canvas_width)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para diferentes sistemas operativos
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac
        main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        tk.Label(
            scrollable_frame, 
            text="🌳 Generador de Árboles de Probabilidad",
            font=("Helvetica", 16, "bold")
        ).pack(pady=15)
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  🌳 ÁRBOLES DE PROBABILIDAD                                          ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 QUÉ ES:
   Representación gráfica de eventos secuenciales con sus probabilidades

🔹 CÓMO USAR:
   1. Ingresa número de niveles (ej: 3)
   2. Ingresa probabilidades separadas por coma (ej: 0.6, 0.7, 0.5)
   3. Presiona "Generar Árbol"
   4. CLICK en cualquier probabilidad para EDITARLA ✏️

🔹 INTERACTIVIDAD:
   → Haz CLICK en el texto de probabilidad (P=0.xxx)
   → Ingresa el nuevo valor (entre 0 y 1)
   → El árbol se actualizará automáticamente

💡 APLICACIONES: Procesos de decisión, eventos dependientes, análisis de riesgo
        """
        
        frame_inst = tk.Frame(scrollable_frame, bg="#E8F5E9")
        frame_inst.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            frame_inst,
            text=instrucciones_text,
            bg="#E8F5E9",
            fg="#2E7D32",
            font=("Consolas", 9),
            justify='left',
            anchor='w'
        ).pack(padx=15, pady=15)
        
        # Frame para inputs
        frame_input = tk.LabelFrame(scrollable_frame, text="Configuración del Árbol", 
                                     padx=20, pady=15, font=("Helvetica", 11, "bold"))
        frame_input.pack(padx=20, pady=10, fill='x')
        
        tk.Label(frame_input, text="Número de niveles:", 
                font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
        entry_niveles = tk.Entry(frame_input, width=10, font=("Helvetica", 10))
        entry_niveles.grid(row=0, column=1, padx=5, sticky='w')
        entry_niveles.insert(0, "3")
        
        tk.Label(frame_input, text="Probabilidades por nivel (separadas por coma):", 
                font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
        entry_probs = tk.Entry(frame_input, width=50, font=("Helvetica", 10))
        entry_probs.grid(row=1, column=1, padx=5, sticky='w')
        entry_probs.insert(0, "0.6, 0.7, 0.5")
        
        # Instrucciones más claras
        instrucciones = tk.Label(
            frame_input, 
            text="💡 Ejemplo: Si tienes 3 niveles, ingresa 3 probabilidades: 0.6, 0.7, 0.5\n"
                 "    Cada probabilidad debe estar entre 0 y 1",
            font=("Helvetica", 9), 
            fg="#1976D2",
            justify='left'
        )
        instrucciones.grid(row=2, column=0, columnspan=2, pady=5, sticky='w')
        
        # Frame para el árbol
        frame_arbol = tk.Frame(scrollable_frame, bg=BG_WHITE, relief='solid', borderwidth=1)
        frame_arbol.pack(fill='both', expand=True, padx=20, pady=10)
        
        def generar_arbol():
            try:
                # Limpiar frame
                for widget in frame_arbol.winfo_children():
                    widget.destroy()
                
                # Obtener parámetros
                niveles = int(entry_niveles.get())
                probs_str = entry_probs.get().split(',')
                probabilidades = [float(p.strip()) for p in probs_str]
                
                if len(probabilidades) != niveles:
                    messagebox.showerror("Error", 
                        f"Necesitas {niveles} probabilidades (una por nivel)")
                    return
                
                # Validar probabilidades
                for p in probabilidades:
                    if not 0 <= p <= 1:
                        messagebox.showerror("Error", 
                            "Las probabilidades deben estar entre 0 y 1")
                        return
                
                # Crear y dibujar árbol INTERACTIVO
                arbol = DiagramaArbol(niveles, probabilidades)
                fig = arbol.dibujar(interactivo=True)  # ⬅️ Modo interactivo activado
                
                # Limpiar frame anterior
                for widget in frame_arbol.winfo_children():
                    widget.destroy()
                
                # Mostrar en canvas con toolbar de navegación
                from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
                
                canvas = FigureCanvasTkAgg(fig, master=frame_arbol)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
                # Agregar toolbar para mejor interacción
                toolbar = NavigationToolbar2Tk(canvas, frame_arbol)
                toolbar.update()
                
                messagebox.showinfo("✅ Árbol Interactivo Generado", 
                    f"Árbol generado con {niveles} niveles\n\n"
                    f"💡 CÓMO USAR:\n"
                    f"• Haz CLICK en cualquier nodo para ver opciones\n"
                    f"• Puedes EDITAR las probabilidades de cada nivel\n"
                    f"• Los cambios se actualizan automáticamente en el árbol\n\n"
                    f"🌳 ¡Explora y modifica tu árbol de probabilidades!")
                
            except ValueError as e:
                messagebox.showerror("Error", 
                    f"Valores inválidos. Verifica los datos:\n{str(e)}")
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Error al generar árbol:\n{str(e)}")
        
        # Botón generar
        btn_frame = tk.Frame(scrollable_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="🌳 Generar Árbol",
            command=generar_arbol,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            width=20,
            height=2,
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Limpiar",
            command=lambda: [widget.destroy() for widget in frame_arbol.winfo_children()],
            bg=COLOR_WARNING,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="⬅️ Regresar",
            command=ventana.destroy,
            bg="#9C27B0",
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        ).pack(side='left', padx=5)
        
        # Mensaje inicial
        tk.Label(
            frame_arbol,
            text="👆 Configura los parámetros arriba y presiona 'Generar Árbol'",
            font=("Helvetica", 12),
            fg=TEXT_MUTED,
            bg=BG_WHITE
        ).pack(expand=True)
    
    def abrir_chi_cuadrado(self):
        """Prueba de Chi-cuadrado"""
        ventana = tk.Toplevel(self.root)
        ventana.title("χ² Prueba de Chi-cuadrado")
        
        # Obtener dimensiones de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        
        # Configurar ventana
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
        ventana.configure(bg=BG_LIGHT)
        
        # ===== CREAR CANVAS PRINCIPAL CON SCROLL =====
        # Frame contenedor principal
        main_container = tk.Frame(ventana, bg=BG_LIGHT)
        main_container.pack(fill='both', expand=True)
        
        # Canvas para scroll
        main_canvas = tk.Canvas(main_container, bg=BG_LIGHT, highlightthickness=0)
        main_canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=main_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(main_canvas, bg=BG_LIGHT)
        
        # Crear ventana en el canvas
        canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        
        # Función para actualizar el scroll region
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox('all'))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        
        # Hacer que el frame scrollable se expanda al ancho del canvas
        def configure_canvas_width(event):
            main_canvas.itemconfig(canvas_window, width=event.width)
        
        main_canvas.bind('<Configure>', configure_canvas_width)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para diferentes sistemas operativos
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac
        main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        chi = PruebaChiCuadrado()
        
        # Título
        tk.Label(
            scrollable_frame,
            text="χ² PRUEBA DE CHI-CUADRADO",
            font=("Helvetica", 16, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY
        ).pack(pady=15)
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  χ² PRUEBA DE CHI-CUADRADO                                           ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 QUÉ ES:
   Prueba estadística para determinar si existe asociación entre variables categóricas

🔹 TIPOS DE PRUEBAS:
   → INDEPENDENCIA: ¿Las variables están relacionadas?
   → BONDAD DE AJUSTE: ¿Los datos siguen cierta distribución?

🔹 CÓMO INTERPRETAR:
   → p-valor < 0.05: Hay asociación significativa (rechazar H₀)
   → p-valor ≥ 0.05: No hay evidencia de asociación (no rechazar H₀)

🔹 QUÉ VERÁS:
   → Estadístico χ² calculado
   → Grados de libertad
   → p-valor
   → Conclusión estadística

💡 EJEMPLO: ¿El género afecta la preferencia de producto?
        """
        
        frame_inst = tk.Frame(scrollable_frame, bg="#FCE4EC")
        frame_inst.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            frame_inst,
            text=instrucciones_text,
            bg="#FCE4EC",
            fg="#C2185B",
            font=("Consolas", 9),
            justify='left',
            anchor='w'
        ).pack(padx=15, pady=15)
        
        # Notebook para diferentes tipos de pruebas
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ========== PESTAÑA 1: PRUEBA DE INDEPENDENCIA ==========
        tab_independencia = tk.Frame(notebook, bg=BG_WHITE)
        notebook.add(tab_independencia, text="Prueba de Independencia")
        
        frame_input_ind = tk.LabelFrame(tab_independencia, text="Tabla de Contingencia (Frecuencias Observadas)",
                                        padx=15, pady=15, bg=BG_WHITE, font=("Helvetica", 11, "bold"))
        frame_input_ind.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame_input_ind, text="Ingresa los datos de la tabla de contingencia:", 
                bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=0, column=0, columnspan=4, pady=5, sticky='w')
        
        tk.Label(frame_input_ind, text="Ejemplo: Género (filas) vs Preferencia (columnas)",
                bg=BG_WHITE, font=("Helvetica", 9), fg=TEXT_MUTED).grid(row=1, column=0, columnspan=4, sticky='w')
        
        # Entradas para la tabla (2x3 por defecto)
        tk.Label(frame_input_ind, text="Fila 1:", bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        entry_f1_c1 = tk.Entry(frame_input_ind, width=8)
        entry_f1_c1.grid(row=2, column=1, padx=2)
        entry_f1_c1.insert(0, "30")
        entry_f1_c2 = tk.Entry(frame_input_ind, width=8)
        entry_f1_c2.grid(row=2, column=2, padx=2)
        entry_f1_c2.insert(0, "20")
        entry_f1_c3 = tk.Entry(frame_input_ind, width=8)
        entry_f1_c3.grid(row=2, column=3, padx=2)
        entry_f1_c3.insert(0, "10")
        
        tk.Label(frame_input_ind, text="Fila 2:", bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=3, column=0, sticky='w', pady=5)
        entry_f2_c1 = tk.Entry(frame_input_ind, width=8)
        entry_f2_c1.grid(row=3, column=1, padx=2)
        entry_f2_c1.insert(0, "15")
        entry_f2_c2 = tk.Entry(frame_input_ind, width=8)
        entry_f2_c2.grid(row=3, column=2, padx=2)
        entry_f2_c2.insert(0, "25")
        entry_f2_c3 = tk.Entry(frame_input_ind, width=8)
        entry_f2_c3.grid(row=3, column=3, padx=2)
        entry_f2_c3.insert(0, "20")
        
        # Área de resultados
        text_result_ind = scrolledtext.ScrolledText(tab_independencia, height=20, width=100, 
                                                     font=("Consolas", 10), bg=BG_WHITE)
        text_result_ind.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para gráfico
        frame_graf_ind = tk.Frame(tab_independencia, bg=BG_WHITE)
        frame_graf_ind.pack(fill='both', expand=True, padx=10, pady=5)
        
        def calcular_independencia():
            try:
                # Obtener valores
                fila1 = [float(entry_f1_c1.get()), float(entry_f1_c2.get()), float(entry_f1_c3.get())]
                fila2 = [float(entry_f2_c1.get()), float(entry_f2_c2.get()), float(entry_f2_c3.get())]
                tabla = np.array([fila1, fila2])
                
                # Realizar prueba
                resultados = chi.prueba_independencia(tabla)
                
                # Mostrar resultados
                texto = "=" * 100 + "\n"
                texto += "PRUEBA DE INDEPENDENCIA CHI-CUADRADO (χ²)\n"
                texto += "=" * 100 + "\n\n"
                
                texto += "HIPÓTESIS:\n"
                texto += "H₀: Las variables son independientes (no hay relación)\n"
                texto += "H₁: Las variables son dependientes (sí hay relación)\n\n"
                
                texto += "TABLA DE CONTINGENCIA (Observados):\n"
                texto += f"{tabla}\n\n"
                
                texto += "VALORES ESPERADOS (bajo H₀):\n"
                texto += f"{resultados['valores_esperados']}\n\n"
                
                texto += "RESULTADOS DE LA PRUEBA:\n"
                texto += f"Estadístico χ² = {resultados['chi2_estadistico']:.4f}\n"
                texto += f"Grados de libertad = {resultados['grados_libertad']}\n"
                texto += f"Valor p = {resultados['p_value']:.4f}\n"
                texto += f"Nivel de significancia α = {resultados['alpha']}\n\n"
                
                texto += "DECISIÓN:\n"
                texto += f"{resultados['decision']}\n\n"
                
                texto += "CONCLUSIÓN:\n"
                texto += f"{resultados['conclusion']}\n\n"
                
                texto += "INTERPRETACIÓN:\n"
                if resultados['p_value'] < resultados['alpha']:
                    texto += f"Con un valor p = {resultados['p_value']:.4f} < α = {resultados['alpha']}, hay evidencia\n"
                    texto += "estadística suficiente para afirmar que las variables están relacionadas.\n"
                else:
                    texto += f"Con un valor p = {resultados['p_value']:.4f} >= α = {resultados['alpha']}, NO hay evidencia\n"
                    texto += "estadística suficiente para afirmar que las variables están relacionadas.\n"
                
                text_result_ind.delete("1.0", tk.END)
                text_result_ind.insert(tk.END, texto)
                
                # Crear gráfico
                for widget in frame_graf_ind.winfo_children():
                    widget.destroy()
                
                fig = chi.graficar_heatmap(tabla, "Tabla de Contingencia - Frecuencias Observadas",
                                          ["Fila 1", "Fila 2"], ["Col 1", "Col 2", "Col 3"])
                
                canvas = FigureCanvasTkAgg(fig, master=frame_graf_ind)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular:\n{str(e)}")
        
        btn_calc_ind = tk.Button(frame_input_ind, text="📊 Calcular Chi-cuadrado", command=calcular_independencia,
                                bg=COLOR_SUCCESS, fg="#000000", font=("Helvetica", 11, "bold"),
                                cursor="hand2", padx=20, pady=8, activebackground="#FFEB3B", activeforeground="#000000")
        btn_calc_ind.grid(row=4, column=0, columnspan=4, pady=15)
        
        # ========== PESTAÑA 2: BONDAD DE AJUSTE ==========
        tab_bondad = tk.Frame(notebook, bg=BG_WHITE)
        notebook.add(tab_bondad, text="Bondad de Ajuste")
        
        frame_input_bon = tk.LabelFrame(tab_bondad, text="Datos para Bondad de Ajuste",
                                        padx=15, pady=15, bg=BG_WHITE, font=("Helvetica", 11, "bold"))
        frame_input_bon.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame_input_bon, text="Frecuencias Observadas (separadas por comas):",
                bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
        entry_observados = tk.Entry(frame_input_bon, width=50, font=("Helvetica", 10))
        entry_observados.grid(row=0, column=1, padx=5, pady=5)
        entry_observados.insert(0, "18, 22, 15, 20, 19, 26")
        
        tk.Label(frame_input_bon, text="Frecuencias Esperadas (separadas por comas, dejar vacío para uniforme):",
                bg=BG_WHITE, font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
        entry_esperados = tk.Entry(frame_input_bon, width=50, font=("Helvetica", 10))
        entry_esperados.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_input_bon, text="Ejemplo: Lanzamiento de dado 120 veces, esperado = 20 en cada cara",
                bg=BG_WHITE, font=("Helvetica", 9), fg=TEXT_MUTED).grid(row=2, column=0, columnspan=2, sticky='w')
        
        # Área de resultados
        text_result_bon = scrolledtext.ScrolledText(tab_bondad, height=20, width=100,
                                                    font=("Consolas", 10), bg=BG_WHITE)
        text_result_bon.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para gráfico
        frame_graf_bon = tk.Frame(tab_bondad, bg=BG_WHITE)
        frame_graf_bon.pack(fill='both', expand=True, padx=10, pady=5)
        
        def calcular_bondad():
            try:
                # Obtener valores
                obs_str = entry_observados.get().split(',')
                observados = np.array([float(x.strip()) for x in obs_str])
                
                esp_str = entry_esperados.get().strip()
                if esp_str:
                    esperados = np.array([float(x.strip()) for x in esp_str.split(',')])
                else:
                    esperados = None
                
                # Realizar prueba
                resultados = chi.bondad_ajuste(observados, esperados)
                
                # Mostrar resultados
                texto = "=" * 100 + "\n"
                texto += "PRUEBA DE BONDAD DE AJUSTE CHI-CUADRADO (χ²)\n"
                texto += "=" * 100 + "\n\n"
                
                texto += "HIPÓTESIS:\n"
                texto += "H₀: Los datos se ajustan a la distribución esperada\n"
                texto += "H₁: Los datos NO se ajustan a la distribución esperada\n\n"
                
                texto += "DATOS:\n"
                texto += f"Observados: {resultados['valores_observados']}\n"
                texto += f"Esperados:  {resultados['valores_esperados']}\n\n"
                
                texto += "RESULTADOS DE LA PRUEBA:\n"
                texto += f"Estadístico χ² = {resultados['chi2_estadistico']:.4f}\n"
                texto += f"Grados de libertad = {resultados['grados_libertad']}\n"
                texto += f"Valor p = {resultados['p_value']:.4f}\n"
                texto += f"Nivel de significancia α = {resultados['alpha']}\n\n"
                
                texto += "DECISIÓN:\n"
                texto += f"{resultados['decision']}\n\n"
                
                texto += "CONCLUSIÓN:\n"
                texto += f"{resultados['conclusion']}\n\n"
                
                texto += "INTERPRETACIÓN:\n"
                if resultados['p_value'] < resultados['alpha']:
                    texto += f"Con un valor p = {resultados['p_value']:.4f} < α = {resultados['alpha']}, hay evidencia\n"
                    texto += "de que los datos NO se ajustan a la distribución esperada.\n"
                else:
                    texto += f"Con un valor p = {resultados['p_value']:.4f} >= α = {resultados['alpha']}, NO hay evidencia\n"
                    texto += "de que los datos NO se ajustan a la distribución esperada. Se acepta el ajuste.\n"
                
                text_result_bon.delete("1.0", tk.END)
                text_result_bon.insert(tk.END, texto)
                
                # Crear gráfico
                for widget in frame_graf_bon.winfo_children():
                    widget.destroy()
                
                categorias = [f"Cat {i+1}" for i in range(len(observados))]
                fig = chi.graficar_comparacion(resultados['valores_observados'], 
                                              resultados['valores_esperados'],
                                              categorias, "Comparación: Observados vs Esperados")
                
                canvas = FigureCanvasTkAgg(fig, master=frame_graf_bon)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular:\n{str(e)}")
        
        btn_calc_bon = tk.Button(frame_input_bon, text="📊 Calcular Chi-cuadrado", command=calcular_bondad,
                                bg=COLOR_SUCCESS, fg="#000000", font=("Helvetica", 11, "bold"),
                                cursor="hand2", padx=20, pady=8, activebackground="#FFEB3B", activeforeground="#000000")
        btn_calc_bon.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Botón regresar
        tk.Button(
            ventana,
            text="⬅️ Regresar al Menú",
            command=ventana.destroy,
            bg="#9C27B0",
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=8,
            activebackground="#FFEB3B",
            activeforeground="#000000"
        ).pack(pady=10)
    
