"""
Menú Principal de StatPro - VERSIÓN COMPLETA
Todas las funcionalidades implementadas
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import comb

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_interfaz import *
from estadistica_descriptiva.analisis_estadistico import calcular_tendencia_central, generar_dfs, generar_dfsvai
from estadistica_descriptiva.medidas_posicion import analisis_completo_posicion, generar_tabla_posicion, crear_boxplot
from estadistica_descriptiva.medidas_dispersión import analisis_completo_dispersion, generar_tabla_dispersion, graficar_dispersion
from estadistica_descriptiva.medidas_forma import analisis_completo_forma, generar_tabla_forma, graficar_forma
from estadistica_descriptiva.graficas import graficar_tendencia, graficar_frecuencia
from estadistica_inferencial.probabilidades import ProbabilidadesElementales
from estadistica_inferencial.distribuciones import DistribucionBernoulli, DistribucionBinomial
from estadistica_inferencial.distribucion_normal import DistribucionNormal
from estadistica_inferencial.distribucion_poisson import DistribucionPoisson
from estadistica_inferencial.bayes import TeoremaBayes
from estadistica_inferencial.regresion_correlacion import CorrelacionLineal, RegresionLinealSimple, RegresionNoLineal
from estadistica_inferencial.diagramas_arbol import DiagramaArbol


class VentanaAnalisis(tk.Toplevel):
    """Ventana genérica para mostrar análisis - VERSIÓN MEJORADA"""
    
    def __init__(self, parent, titulo, datos=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("1400x900")  # ⬅️ Más grande
        self.datos = datos
        
        # Configurar ventana para que sea responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame principal con scroll
        main_frame = tk.Frame(self, bg=BG_LIGHT)
        main_frame.pack(fill='both', expand=True)
        
        # ===== BARRA DE TÍTULO =====
        frame_titulo = tk.Frame(main_frame, bg=COLOR_PRIMARY, height=70)
        frame_titulo.pack(fill='x', side='top')
        
        lbl_titulo = tk.Label(
            frame_titulo,
            text=titulo,
            font=("Helvetica", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT,
            pady=20
        )
        lbl_titulo.pack()
        
        # ===== BOTÓN CARGAR DATOS =====
        if datos is None:
            btn_frame = tk.Frame(main_frame, bg=BG_LIGHT)
            btn_frame.pack(fill='x', pady=15)
            
            tk.Button(
                btn_frame,
                text=f"{ICONO_ARCHIVO} Cargar Datos CSV",
                command=self.cargar_datos,
                bg=COLOR_SUCCESS,
                fg=TEXT_LIGHT,
                font=("Helvetica", 12, "bold"),
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=10
            ).pack()
        
        # ===== CONTENEDOR CON PESTAÑAS =====
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # PESTAÑA 1: Resultados en Texto
        self.tab_texto = tk.Frame(self.notebook, bg=BG_WHITE)
        self.notebook.add(self.tab_texto, text="📄 Resultados")
        
        # Frame para el texto con scroll
        frame_texto = tk.Frame(self.tab_texto, bg=BG_WHITE)
        frame_texto.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar vertical
        scrollbar_y = tk.Scrollbar(frame_texto)
        scrollbar_y.pack(side='right', fill='y')
        
        # Scrollbar horizontal
        scrollbar_x = tk.Scrollbar(frame_texto, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')
        
        # Área de texto con mejor formato
        self.text_resultados = tk.Text(
            frame_texto,
            height=30,
            width=150,
            font=("Courier New", 11),  # ⬅️ Fuente más grande
            wrap=tk.NONE,  # ⬅️ Sin wrap para ver todo
            bg=BG_WHITE,
            fg=TEXT_DARK,
            relief='solid',
            borderwidth=1,
            padx=10,
            pady=10,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        self.text_resultados.pack(fill='both', expand=True)
        
        scrollbar_y.config(command=self.text_resultados.yview)
        scrollbar_x.config(command=self.text_resultados.xview)
        
        # PESTAÑA 2: Gráficos
        self.tab_graficos = tk.Frame(self.notebook, bg=BG_WHITE)
        self.notebook.add(self.tab_graficos, text="📊 Gráficos")
        
        self.frame_graficos = tk.Frame(self.tab_graficos, bg=BG_WHITE)
        self.frame_graficos.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ===== BARRA DE BOTONES INFERIOR =====
        frame_botones = tk.Frame(main_frame, bg=BG_LIGHT)
        frame_botones.pack(fill='x', side='bottom', pady=10)
        
        tk.Button(
            frame_botones,
            text="💾 Exportar Resultados",
            command=self.exportar_resultados,
            bg=COLOR_INFO,
            fg=TEXT_LIGHT,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_botones,
            text="🖨️ Imprimir",
            command=self.imprimir,
            bg=COLOR_SECONDARY,
            fg=TEXT_LIGHT,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_botones,
            text="🔄 Limpiar",
            command=self.limpiar,
            bg=COLOR_WARNING,
            fg=TEXT_LIGHT,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_botones,
            text="❌ Cerrar",
            command=self.destroy,
            bg=COLOR_DANGER,
            fg=TEXT_LIGHT,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side='right', padx=5)
    
    def cargar_datos(self):
        """Carga datos desde CSV"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                from utils.cargar_datos import importar_csv
                self.datos = importar_csv(ruta)
                
                info = f"✅ ARCHIVO CARGADO CORRECTAMENTE\n\n"
                info += f"Archivo: {ruta.split('/')[-1]}\n"
                info += f"Filas: {len(self.datos)}\n"
                info += f"Columnas: {len(self.datos.columns)}\n\n"
                info += f"Columnas disponibles:\n"
                for col in self.datos.columns:
                    info += f"  • {col}\n"
                
                messagebox.showinfo("Éxito", info)
            except Exception as e:
                messagebox.showerror("Error", f"❌ No se pudo cargar el archivo:\n\n{str(e)}")
    
    def mostrar_texto(self, texto):
        """Muestra texto en el área de resultados"""
        self.text_resultados.delete("1.0", tk.END)
        self.text_resultados.insert(tk.END, texto)
        
        # Cambiar a la pestaña de resultados
        self.notebook.select(self.tab_texto)
    
    def mostrar_grafico(self, figura):
        """Muestra un gráfico de matplotlib"""
        # Limpiar gráficos anteriores
        for widget in self.frame_graficos.winfo_children():
            widget.destroy()
        
        # Crear canvas con scroll
        canvas_frame = tk.Frame(self.frame_graficos, bg=BG_WHITE)
        canvas_frame.pack(fill='both', expand=True)
        
        canvas = FigureCanvasTkAgg(figura, canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Cambiar a la pestaña de gráficos
        self.notebook.select(self.tab_graficos)
    
    def exportar_resultados(self):
        """Exporta los resultados a un archivo de texto"""
        contenido = self.text_resultados.get("1.0", tk.END)
        
        if contenido.strip():
            ruta = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            if ruta:
                try:
                    with open(ruta, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    messagebox.showinfo("Éxito", f"✅ Resultados exportados a:\n{ruta}")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ No se pudo exportar:\n{str(e)}")
        else:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
    
    def imprimir(self):
        """Simula la impresión (abre diálogo de impresión del sistema)"""
        messagebox.showinfo("Imprimir", "💡 Usa Ctrl+P o Cmd+P para imprimir desde tu navegador/sistema")
    
    def limpiar(self):
        """Limpia los resultados"""
        respuesta = messagebox.askyesno("Confirmar", "¿Desea limpiar todos los resultados?")
        if respuesta:
            self.text_resultados.delete("1.0", tk.END)
            for widget in self.frame_graficos.winfo_children():
                widget.destroy()

class MenuPrincipal:
    def __init__(self, root, usuario, callback_cerrar_sesion):
        self.root = root
        self.usuario = usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion
        
        self.root.title(f"{NOMBRE_PROYECTO} - Menú Principal")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_LIGHT)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        self.crear_barra_superior()
        
        self.frame_principal = tk.Frame(self.root, bg=BG_LIGHT)
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        frame_bienvenida = tk.Frame(self.frame_principal, bg=BG_LIGHT)
        frame_bienvenida.pack(fill='x', pady=(0, 30))
        
        lbl_bienvenida = tk.Label(
            frame_bienvenida,
            text=f"Bienvenido/a, {self.usuario.upper()}",
            font=("Helvetica", 24, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY
        )
        lbl_bienvenida.pack()
        
        lbl_subtitulo = tk.Label(
            frame_bienvenida,
            text="Seleccione el tipo de análisis que desea realizar",
            font=("Helvetica", 12),
            bg=BG_LIGHT,
            fg=TEXT_MUTED
        )
        lbl_subtitulo.pack(pady=(5, 0))
        
        frame_modulos = tk.Frame(self.frame_principal, bg=BG_LIGHT)
        frame_modulos.pack(fill='both', expand=True)
        
        self.crear_seccion_descriptiva(frame_modulos)
        self.crear_seccion_inferencial(frame_modulos)
    
    def crear_barra_superior(self):
        barra = tk.Frame(self.root, bg=COLOR_PRIMARY, height=80)
        barra.pack(fill='x', side='top')
        
        barra_content = tk.Frame(barra, bg=COLOR_PRIMARY)
        barra_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        frame_logo = tk.Frame(barra_content, bg=COLOR_PRIMARY)
        frame_logo.pack(side='left')
        
        tk.Label(
            frame_logo,
            text=f"{ICONO_ESTADISTICA} {NOMBRE_PROYECTO}",
            font=("Helvetica", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT
        ).pack(side='left')
        
        frame_usuario = tk.Frame(barra_content, bg=COLOR_PRIMARY)
        frame_usuario.pack(side='right')
        
        tk.Label(
            frame_usuario,
            text=f"👤 {self.usuario}",
            font=("Helvetica", 11),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT
        ).pack(side='left', padx=10)
        
        btn_cerrar = tk.Button(
            frame_usuario,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            bg=COLOR_DANGER,
            fg=TEXT_LIGHT,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        btn_cerrar.pack(side='left')
    
    def crear_seccion_descriptiva(self, parent):
        """Crea la sección de Estadística Descriptiva"""
        frame = tk.LabelFrame(
            parent,
            text=TITULO_DESCRIPTIVA,
            font=("Helvetica", 14, "bold"),
            bg=BG_WHITE,
            fg=COLOR_PRIMARY,
            padx=20,
            pady=20,
            relief="solid",
            borderwidth=2
        )
        frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Colores claros para fondo
        colores_fondo = ["#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#E0F7FA"]
        
        botones = [
            ("📊 Cuadros y Gráficos Estadísticos", colores_fondo[0], self.abrir_cuadros),
            ("📈 Medidas de Tendencia Central", colores_fondo[1], self.abrir_tendencia),
            ("📍 Medidas de Posición", colores_fondo[2], self.abrir_posicion),
            ("📏 Medidas de Dispersión", colores_fondo[3], self.abrir_dispersion),
            ("📉 Medidas de Forma", colores_fondo[4], self.abrir_forma),
        ]
        
        for texto, color_fondo, comando in botones:
            btn = tk.Button(
                frame,
                text=texto,
                command=comando,
                bg=color_fondo,
                fg="#000000",  # ⬅️ TEXTO NEGRO
                font=("Helvetica", 13, "bold"),
                width=40,
                height=2,
                relief="raised",
                borderwidth=2,
                cursor="hand2",
                anchor='center',
                padx=10,
                pady=10,
                activebackground="#FFEB3B",  # Amarillo al hacer clic
                activeforeground="#000000"
            )
            btn.pack(fill='x', pady=10, padx=10)
            
            # Efectos hover
            def on_enter(e, b=btn):
                b.config(bg="#FFEB3B", relief="sunken")  # Amarillo hover
            
            def on_leave(e, b=btn, original_color=color_fondo):
                b.config(bg=original_color, relief="raised")
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def crear_seccion_inferencial(self, parent):
        """Crea la sección de Estadística Inferencial"""
        frame = tk.LabelFrame(
            parent,
            text=TITULO_INFERENCIAL,
            font=("Helvetica", 14, "bold"),
            bg=BG_WHITE,
            fg=COLOR_SECONDARY,
            padx=20,
            pady=20,
            relief="solid",
            borderwidth=2
        )
        frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        # Colores claros para fondo
        colores_fondo = ["#FCE4EC", "#F1F8E9", "#FFF9C4", "#E1F5FE", "#FFEBEE"]
        
        botones = [
            ("🎲 Cálculo de Probabilidades", colores_fondo[0], self.abrir_probabilidades),
            ("🔄 Teorema de Bayes", colores_fondo[1], self.abrir_bayes),
            ("📊 Distribuciones (Normal, Binomial, Poisson)", colores_fondo[2], self.abrir_distribuciones),
            ("📈 Correlación y Regresión Simple", colores_fondo[3], self.abrir_regresion),
            ("🌳 Árboles de Decisión", colores_fondo[4], self.abrir_arboles),
        ]
        
        for texto, color_fondo, comando in botones:
            btn = tk.Button(
                frame,
                text=texto,
                command=comando,
                bg=color_fondo,
                fg="#000000",  # ⬅️ TEXTO NEGRO
                font=("Helvetica", 13, "bold"),
                width=40,
                height=2,
                relief="raised",
                borderwidth=2,
                cursor="hand2",
                anchor='center',
                padx=10,
                pady=10,
                activebackground="#FFEB3B",  # Amarillo al hacer clic
                activeforeground="#000000"
            )
            btn.pack(fill='x', pady=10, padx=10)
            
            # Efectos hover
            def on_enter(e, b=btn):
                b.config(bg="#FFEB3B", relief="sunken")  # Amarillo hover
            
            def on_leave(e, b=btn, original_color=color_fondo):
                b.config(bg=original_color, relief="raised")
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
    # ===== ESTADÍSTICA DESCRIPTIVA =====
    
    def abrir_cuadros(self):
        ventana = VentanaAnalisis(self.root, "📊 Cuadros y Gráficos Estadísticos")
        
        if ventana.datos is not None and 'Edad' in ventana.datos.columns:
            datos_edad = ventana.datos['Edad']
            dfs = generar_dfs(datos_edad)
            dfsvai = generar_dfsvai(datos_edad)
            
            resultado = f"{'='*80}\nCUADRO DE FRECUENCIA SIMPLE\n{'='*80}\n\n"
            resultado += dfs.to_string(index=False)
            resultado += f"\n\n{'='*80}\nCUADRO DE FRECUENCIA AGRUPADA\n{'='*80}\n\n"
            resultado += dfsvai.to_string(index=False)
            
            ventana.mostrar_texto(resultado)
            graficar_frecuencia(dfs, 'simple')
            graficar_frecuencia(dfsvai, 'agrupada')
    
    def abrir_tendencia(self):
        ventana = VentanaAnalisis(self.root, "📈 Medidas de Tendencia Central")
        
        if ventana.datos is not None and 'Edad' in ventana.datos.columns:
            datos_edad = ventana.datos['Edad']
            tendencia = calcular_tendencia_central(datos_edad)
            
            resultado = f"{'='*80}\nMEDIDAS DE TENDENCIA CENTRAL\n{'='*80}\n\n"
            for medida, valor in tendencia.items():
                resultado += f"{medida:25s}: {valor}\n"
            
            ventana.mostrar_texto(resultado)
            graficar_tendencia(datos_edad)
    
    def abrir_posicion(self):
        ventana = VentanaAnalisis(self.root, "📍 Medidas de Posición")
        
        if ventana.datos is not None and 'Edad' in ventana.datos.columns:
            datos_edad = ventana.datos['Edad']
            tabla = generar_tabla_posicion(datos_edad)
            
            resultado = f"{'='*80}\nMEDIDAS DE POSICIÓN\n{'='*80}\n\n"
            resultado += tabla.to_string(index=False)
            
            ventana.mostrar_texto(resultado)
            fig = crear_boxplot(datos_edad)
            ventana.mostrar_grafico(fig)
    
    def abrir_dispersion(self):
        ventana = VentanaAnalisis(self.root, "📏 Medidas de Dispersión")
        
        if ventana.datos is not None and 'Edad' in ventana.datos.columns:
            datos_edad = ventana.datos['Edad']
            tabla = generar_tabla_dispersion(datos_edad)
            
            resultado = f"{'='*80}\nMEDIDAS DE DISPERSIÓN\n{'='*80}\n\n"
            resultado += tabla.to_string(index=False)
            
            ventana.mostrar_texto(resultado)
            fig = graficar_dispersion(datos_edad)
            ventana.mostrar_grafico(fig)
    
    def abrir_forma(self):
        ventana = VentanaAnalisis(self.root, "📉 Medidas de Forma")
        
        if ventana.datos is not None and 'Edad' in ventana.datos.columns:
            datos_edad = ventana.datos['Edad']
            tabla = generar_tabla_forma(datos_edad)
            
            resultado = f"{'='*80}\nMEDIDAS DE FORMA\n{'='*80}\n\n"
            resultado += tabla.to_string(index=False)
            
            ventana.mostrar_texto(resultado)
            fig = graficar_forma(datos_edad)
            ventana.mostrar_grafico(fig)
    
    # ===== ESTADÍSTICA INFERENCIAL =====
    
    def abrir_probabilidades(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("🎲 Cálculo de Probabilidades Elementales")
        ventana.geometry("1000x700")
        ventana.configure(bg=BG_LIGHT)
        
        prob = ProbabilidadesElementales()
        
        # Frame superior para inputs
        frame_input = tk.LabelFrame(ventana, text="Definir Espacio Muestral y Eventos", 
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
        
        tk.Button(frame_input, text="Definir", command=def_espacio, bg=COLOR_SUCCESS, fg=TEXT_LIGHT).grid(row=0, column=2, padx=5)
        
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
        
        tk.Button(frame_input, text="Definir Evento", command=def_evento, bg=COLOR_INFO, fg=TEXT_LIGHT).grid(row=2, column=2, padx=5)
        
        # Área de resultados
        text_prob = scrolledtext.ScrolledText(ventana, height=25, width=120)
        text_prob.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botones de cálculo
        frame_calc = tk.Frame(ventana, bg=BG_LIGHT)
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
        
        tk.Button(frame_calc, text="P(A)", command=calc_simple, bg=COLOR_PRIMARY, fg=TEXT_LIGHT).grid(row=1, column=0, pady=5)
        tk.Button(frame_calc, text="P(A ∪ B)", command=calc_union, bg=COLOR_SECONDARY, fg=TEXT_LIGHT).grid(row=1, column=1, pady=5)
    
    def abrir_bayes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("🔄 Teorema de Bayes")
        ventana.geometry("800x600")
        
        tk.Label(ventana, text="📊 Teorema de Bayes", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        frame = tk.Frame(ventana)
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
        
        text_result = scrolledtext.ScrolledText(ventana, height=20, width=80)
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
        
        tk.Button(ventana, text="Calcular", command=calcular, bg=COLOR_SUCCESS, 
                 fg=TEXT_LIGHT, font=FONT_BUTTON).pack(pady=10)
    
    def abrir_distribuciones(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("📊 Distribuciones de Probabilidad")
        ventana.geometry("1000x700")
        
        notebook = ttk.Notebook(ventana)
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
                
                text = f"{'='*60}\nDISTRIBUCIÓN BINOMIAL\n{'='*60}\n\n"
                text += f"Parámetros: n={n}, p={p}\n"
                text += f"P(X = {k}) = {resultado['probabilidad']:.6f}\n"
                text += f"Porcentaje: {resultado['porcentaje']}%\n"
                text += f"\nFórmula: {resultado['formula']}\n"
                
                text_binom.delete("1.0", tk.END)
                text_binom.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(tab_binom, text="Calcular", command=calc_binomial, 
                 bg=COLOR_PRIMARY, fg=TEXT_LIGHT, font=FONT_BUTTON).pack(pady=5)
        
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
                prob = normal.probabilidad_menor(x)
                
                text = f"{'='*60}\nDISTRIBUCIÓN NORMAL\n{'='*60}\n\n"
                text += f"Parámetros: μ={mu}, σ={sigma}\n"
                text += f"P(X < {x}) = {prob['probabilidad']:.6f}\n"
                text += f"Porcentaje: {prob['porcentaje']}%\n"
                
                text_normal.delete("1.0", tk.END)
                text_normal.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(tab_normal, text="Calcular", command=calc_normal, 
                 bg=COLOR_SECONDARY, fg=TEXT_LIGHT, font=FONT_BUTTON).pack(pady=5)
        
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
                
                text = f"{'='*60}\nDISTRIBUCIÓN DE POISSON\n{'='*60}\n\n"
                text += f"Parámetro: λ={lambd}\n"
                text += f"P(X = {k}) = {resultado['probabilidad']:.6f}\n"
                text += f"Porcentaje: {resultado['porcentaje']}%\n"
                text += f"\nFórmula: {resultado['formula']}\n"
                
                text_poisson.delete("1.0", tk.END)
                text_poisson.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(tab_poisson, text="Calcular", command=calc_poisson, 
                 bg=COLOR_INFO, fg=TEXT_LIGHT, font=FONT_BUTTON).pack(pady=5)
    
    def abrir_regresion(self):
        """Regresión y Correlación Simple"""
        ventana = VentanaAnalisis(self.root, "📈 Correlación y Regresión Simple")
        
        if ventana.datos is not None:
            # Seleccionar columnas
            columnas = list(ventana.datos.columns)
            
            ventana_seleccion = tk.Toplevel(ventana)
            ventana_seleccion.title("Seleccionar Variables")
            ventana_seleccion.geometry("400x300")
            
            tk.Label(ventana_seleccion, text="Variable X (independiente):", 
                    font=("Helvetica", 11, "bold")).pack(pady=10)
            combo_x = ttk.Combobox(ventana_seleccion, values=columnas, width=30)
            combo_x.pack(pady=5)
            
            tk.Label(ventana_seleccion, text="Variable Y (dependiente):", 
                    font=("Helvetica", 11, "bold")).pack(pady=10)
            combo_y = ttk.Combobox(ventana_seleccion, values=columnas, width=30)
            combo_y.pack(pady=5)
            
            def calcular_regresion():
                try:
                    col_x = combo_x.get()
                    col_y = combo_y.get()
                    
                    if not col_x or not col_y:
                        messagebox.showwarning("Advertencia", "Seleccione ambas variables")
                        return
                    
                    x = ventana.datos[col_x].dropna()
                    y = ventana.datos[col_y].dropna()
                    
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
                    
                    # Mostrar resultados
                    texto = f"{'='*80}\n"
                    texto += f"ANÁLISIS DE CORRELACIÓN Y REGRESIÓN\n"
                    texto += f"{'='*80}\n\n"
                    texto += f"Variables: X={col_x}, Y={col_y}\n"
                    texto += f"N = {len(x)} observaciones\n\n"
                    
                    texto += f"--- CORRELACIÓN ---\n"
                    texto += f"Coeficiente de Pearson (r): {resultado_corr['r']}\n"
                    texto += f"R² (determinación): {resultado_corr['r_cuadrado']}\n"
                    texto += f"Interpretación: {resultado_corr['interpretacion']}\n"
                    texto += f"Significativo: {'Sí' if resultado_corr['significativo'] else 'No'} (p={resultado_corr['p_valor']:.6f})\n\n"
                    
                    texto += f"--- REGRESIÓN LINEAL SIMPLE ---\n"
                    texto += f"Ecuación: {ecuacion['ecuacion']}\n"
                    texto += f"Intercepto (a): {ecuacion['a_intercepto']}\n"
                    texto += f"Pendiente (b): {ecuacion['b_pendiente']}\n"
                    texto += f"R²: {resumen['r2_determinacion']} ({resumen['r2_porcentaje']})\n"
                    texto += f"RMSE: {resumen['rmse']}\n"
                    texto += f"{resumen['interpretacion_r2']}\n\n"
                    
                    texto += f"--- COMPARACIÓN DE MODELOS ---\n"
                    texto += f"Mejor modelo: {comparacion['mejor_modelo']}\n"
                    texto += f"R² del mejor: {comparacion['mejor_r2']}\n"
                    texto += f"Ecuación: {comparacion['mejor_ecuacion']}\n"
                    texto += f"{comparacion['recomendacion']}\n\n"
                    
                    texto += "MODELOS COMPARADOS:\n"
                    for nombre, datos in comparacion['modelos'].items():
                        texto += f"  • {nombre}: R²={datos['r2']:.4f}\n"
                    
                    ventana.mostrar_texto(texto)
                    
                    # Mostrar gráficos
                    fig_corr = corr.graficar_correlacion()
                    plt.show()
                    
                    fig_reg = reg_lineal.graficar()
                    ventana.mostrar_grafico(fig_reg)
                    
                    fig_comp = reg_no_lineal.graficar_comparacion()
                    plt.show()
                    
                    ventana_seleccion.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error en el análisis:\n{str(e)}")
            
            tk.Button(
                ventana_seleccion, 
                text="Calcular Regresión", 
                command=calcular_regresion,
                bg=COLOR_SUCCESS,
                fg=TEXT_LIGHT,
                font=FONT_BUTTON,
                width=20,
                height=2
            ).pack(pady=20)
    
    def abrir_arboles(self):
        """Árboles de Probabilidad"""
        ventana = tk.Toplevel(self.root)
        ventana.title("🌳 Árboles de Decisión - Probabilidades")
        ventana.geometry("1000x700")
        
        tk.Label(
            ventana, 
            text="🌳 Generador de Árboles de Probabilidad",
            font=("Helvetica", 16, "bold")
        ).pack(pady=15)
        
        # Frame para inputs
        frame_input = tk.LabelFrame(ventana, text="Configuración del Árbol", 
                                     padx=20, pady=15, font=("Helvetica", 11, "bold"))
        frame_input.pack(padx=20, pady=10, fill='x')
        
        tk.Label(frame_input, text="Número de niveles:", 
                font=("Helvetica", 10)).grid(row=0, column=0, sticky='w', pady=5)
        entry_niveles = tk.Entry(frame_input, width=10)
        entry_niveles.grid(row=0, column=1, padx=5)
        entry_niveles.insert(0, "3")
        
        tk.Label(frame_input, text="Probabilidades por nivel (separadas por coma):", 
                font=("Helvetica", 10)).grid(row=1, column=0, sticky='w', pady=5)
        entry_probs = tk.Entry(frame_input, width=40)
        entry_probs.grid(row=1, column=1, padx=5)
        entry_probs.insert(0, "0.6, 0.7, 0.5")
        
        tk.Label(frame_input, text="Ejemplo: 0.6, 0.7, 0.5 (una por cada nivel)", 
                font=("Helvetica", 8), fg=TEXT_MUTED).grid(row=2, column=0, columnspan=2, pady=2)
        
        # Frame para el árbol
        frame_arbol = tk.Frame(ventana, bg=BG_WHITE, relief='solid', borderwidth=1)
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
                
                # Crear y dibujar árbol
                arbol = DiagramaArbol(niveles, probabilidades)
                fig = arbol.dibujar()
                
                # Mostrar en canvas
                canvas = FigureCanvasTkAgg(fig, master=frame_arbol)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
                messagebox.showinfo("Éxito", 
                    f"✅ Árbol generado con {niveles} niveles")
                
            except ValueError as e:
                messagebox.showerror("Error", 
                    f"Valores inválidos. Verifica los datos:\n{str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar árbol:\n{str(e)}")
        
        # Botón generar
        btn_frame = tk.Frame(ventana)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="🌳 Generar Árbol",
            command=generar_arbol,
            bg=COLOR_SUCCESS,
            fg=TEXT_LIGHT,
            font=("Helvetica", 11, "bold"),
            width=20,
            height=2,
            cursor="hand2"
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Limpiar",
            command=lambda: [widget.destroy() for widget in frame_arbol.winfo_children()],
            bg=COLOR_WARNING,
            fg=TEXT_LIGHT,
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            cursor="hand2"
        ).pack(side='left', padx=5)
        
        # Generar árbol por defecto
        generar_arbol()
    
    def cerrar_sesion(self):
        """Cierra la sesión"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro que desea cerrar sesión?"
        )
        if respuesta:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.callback_cerrar_sesion()


# Función de prueba
def test_menu():
    def callback_cerrar():
        print("Sesión cerrada")
        root.destroy()
    
    root = tk.Tk()
    menu = MenuPrincipal(root, "Ana Paula", callback_cerrar)
    root.mainloop()


if __name__ == "__main__":
    test_menu()