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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.gridspec as gridspec
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
from estadistica_inferencial.chi_cuadrado import PruebaChiCuadrado
from utils.tooltip import crear_tooltip


class VentanaAnalisis(tk.Toplevel):
    """Ventana genérica para mostrar análisis - VERSIÓN MEJORADA CON SCROLL"""
    
    def __init__(self, parent, titulo, datos=None):
        super().__init__(parent)
        self.title(titulo)
        
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Configurar ventana al 90% de la pantalla
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.datos = datos
        
        # Configurar ventana para que sea responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # ===== CREAR CANVAS PRINCIPAL CON SCROLL =====
        # Frame contenedor principal
        main_container = tk.Frame(self, bg="#F5F7FA")
        main_container.pack(fill='both', expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_container, bg="#F5F7FA", highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = tk.Frame(canvas, bg="#F5F7FA")
        
        # Crear ventana en el canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        
        # Función para actualizar el scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        
        # Hacer que el frame scrollable se expanda al ancho del canvas
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas_width)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para diferentes sistemas operativos
        canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        # Ahora usamos scrollable_frame como main_frame
        main_frame = scrollable_frame
        
        # ===== BARRA DE TÍTULO MEJORADA CON SOMBRA =====
        # Frame de sombra
        shadow_frame = tk.Frame(main_frame, bg="#B0BEC5", height=3)
        shadow_frame.pack(fill='x', side='top')
        
        frame_titulo = tk.Frame(main_frame, bg=COLOR_PRIMARY, height=80)
        frame_titulo.pack(fill='x', side='top')
        
        # Contenedor para centrar título e ícono
        title_container = tk.Frame(frame_titulo, bg=COLOR_PRIMARY)
        title_container.pack(expand=True)
        
        lbl_titulo = tk.Label(
            title_container,
            text=titulo,
            font=("Helvetica", 20, "bold"),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT,
            pady=15
        )
        lbl_titulo.pack()
        
        # Subtítulo decorativo
        lbl_subtitle = tk.Label(
            title_container,
            text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            font=("Helvetica", 8),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT
        )
        lbl_subtitle.pack()
        
        # ===== BOTÓN CARGAR DATOS CON ESTILO MODERNO =====
        self.btn_frame = tk.Frame(main_frame, bg="#F5F7FA")
        self.btn_frame.pack(fill='x', pady=20)
        
        if datos is None:
            # Frame para organizar los botones en horizontal con espaciado
            btn_container = tk.Frame(self.btn_frame, bg="#F5F7FA")
            btn_container.pack()
            
            # Card container para botones (efecto elevado)
            card_frame = tk.Frame(btn_container, bg="#FFFFFF", relief='solid', borderwidth=1)
            card_frame.pack(padx=20, pady=10)
            
            # Título de la sección
            tk.Label(
                card_frame,
                text="📂 CARGAR O GENERAR DATOS",
                font=("Helvetica", 11, "bold"),
                bg="#FFFFFF",
                fg="#37474F"
            ).pack(pady=(10, 5))
            
            btn_inner_container = tk.Frame(card_frame, bg="#FFFFFF")
            btn_inner_container.pack(pady=(5, 15), padx=20)
            
            # Botón Cargar CSV con diseño Material
            btn_cargar = tk.Button(
                btn_inner_container,
                text=f"{ICONO_ARCHIVO} Cargar CSV",
                command=self.cargar_datos,
                bg="#4CAF50",
                fg="#000000",
                font=("Helvetica", 11, "bold"),
                relief="flat",
                cursor="hand2",
                padx=25,
                pady=12,
                activebackground="#66BB6A",
                activeforeground="#000000",
                borderwidth=0
            )
            btn_cargar.pack(side='left', padx=8)
            
            # Efecto hover
            def on_enter_cargar(e):
                btn_cargar['bg'] = '#66BB6A'
            def on_leave_cargar(e):
                btn_cargar['bg'] = '#4CAF50'
            btn_cargar.bind("<Enter>", on_enter_cargar)
            btn_cargar.bind("<Leave>", on_leave_cargar)
            
            crear_tooltip(btn_cargar, "📥 Importa datos desde un archivo CSV para análisis")
            
            # Botón Generar Aleatorios con diseño Material
            btn_random = tk.Button(
                btn_inner_container,
                text="🎲 Generar Aleatorios",
                command=self.generar_datos_random,
                bg="#FF9800",
                fg="#000000",
                font=("Helvetica", 11, "bold"),
                relief="flat",
                cursor="hand2",
                padx=25,
                pady=12,
                activebackground="#FFB74D",
                activeforeground="#000000",
                borderwidth=0
            )
            btn_random.pack(side='left', padx=8)
            
            # Efecto hover
            def on_enter_random(e):
                btn_random['bg'] = '#FFB74D'
            def on_leave_random(e):
                btn_random['bg'] = '#FF9800'
            btn_random.bind("<Enter>", on_enter_random)
            btn_random.bind("<Leave>", on_leave_random)
            
            crear_tooltip(btn_random, "🎲 Genera datos aleatorios para probar sin CSV")
        
        # ===== CONTENEDOR CON PESTAÑAS MEJORADO =====
        # Estilo personalizado para las pestañas
        style = ttk.Style()
        style.theme_use('default')
        
        # Configurar estilo de pestañas
        style.configure('Custom.TNotebook', 
                       background='#F5F7FA',
                       borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                       background='#E0E0E0',
                       foreground='#37474F',
                       padding=[20, 10],
                       font=('Helvetica', 10, 'bold'))
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', '#FFFFFF')],
                 foreground=[('selected', COLOR_PRIMARY)],
                 expand=[('selected', [1, 1, 1, 0])])
        
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # PESTAÑA 1: Resultados en Texto con diseño mejorado
        self.tab_texto = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(self.tab_texto, text="📄 Resultados Textuales")
        
        # Frame para el texto con scroll (REFERENCIA para paneles de instrucciones)
        self.text_frame = tk.Frame(self.tab_texto, bg="#FFFFFF")
        self.text_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Card para el área de texto
        frame_texto_card = tk.Frame(self.text_frame, bg="#FFFFFF")
        frame_texto_card.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Título de la sección
        tk.Label(
            frame_texto_card,
            text="📊 RESULTADOS DEL ANÁLISIS",
            font=("Helvetica", 12, "bold"),
            bg="#FFFFFF",
            fg="#37474F",
            anchor='w'
        ).pack(fill='x', pady=(5, 10))
        
        frame_texto = tk.Frame(frame_texto_card, bg="#F5F5F5", relief='solid', borderwidth=1)
        frame_texto.pack(fill='both', expand=True)
        
        # Scrollbar vertical moderna
        scrollbar_y = tk.Scrollbar(frame_texto, bg="#E0E0E0", troughcolor="#F5F5F5")
        scrollbar_y.pack(side='right', fill='y')
        
        # Scrollbar horizontal moderna
        scrollbar_x = tk.Scrollbar(frame_texto, orient='horizontal', bg="#E0E0E0", troughcolor="#F5F5F5")
        scrollbar_x.pack(side='bottom', fill='x')
        
        # Área de texto con mejor formato y colores
        self.text_resultados = tk.Text(
            frame_texto,
            height=32,
            width=130,
            font=("Consolas", 10),  # ⬅️ Fuente monoespaciada
            wrap=tk.NONE,  # ⬅️ Sin wrap automático para mejor formato
            bg="#FAFAFA",
            fg="#212121",
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=20,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectbackground="#B3E5FC",
            selectforeground="#000000",
            insertbackground="#2196F3"
        )
        self.text_resultados.pack(fill='both', expand=True)
        
        scrollbar_y.config(command=self.text_resultados.yview)
        scrollbar_x.config(command=self.text_resultados.xview)
        
        # PESTAÑA 2: Gráficos con diseño mejorado
        self.tab_graficos = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(self.tab_graficos, text="📊 Gráficos Visuales")
        
        # Card para gráficos
        graficos_card = tk.Frame(self.tab_graficos, bg="#FFFFFF")
        graficos_card.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Título de la sección
        tk.Label(
            graficos_card,
            text="📈 VISUALIZACIONES GRÁFICAS",
            font=("Helvetica", 12, "bold"),
            bg="#FFFFFF",
            fg="#37474F",
            anchor='w'
        ).pack(fill='x', pady=(5, 10))
        
        self.frame_graficos = tk.Frame(graficos_card, bg="#F5F5F5", relief='solid', borderwidth=1)
        self.frame_graficos.pack(fill='both', expand=True)
        
        # Mensaje de espera para gráficos
        self.lbl_graficos_placeholder = tk.Label(
            self.frame_graficos,
            text="📊\n\nLos gráficos aparecerán aquí después del análisis\n\n"
                 "Primero carga datos y ejecuta el análisis correspondiente",
            font=("Helvetica", 11),
            bg="#F5F5F5",
            fg="#78909C",
            justify='center'
        )
        self.lbl_graficos_placeholder.pack(expand=True)
        
        # ===== BARRA DE BOTONES INFERIOR CON DISEÑO MODERNO =====
        frame_botones_bg = tk.Frame(main_frame, bg="#ECEFF1", height=70)
        frame_botones_bg.pack(fill='x', side='bottom')
        
        frame_botones = tk.Frame(frame_botones_bg, bg="#ECEFF1")
        frame_botones.pack(pady=15)
        
        # Botón Exportar con Material Design
        btn_exportar = tk.Button(
            frame_botones,
            text="💾 Exportar",
            command=self.exportar_resultados,
            bg="#2196F3",
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#42A5F5",
            activeforeground="#000000",
            borderwidth=0
        )
        btn_exportar.pack(side='left', padx=6)
        
        def on_enter_exportar(e):
            btn_exportar['bg'] = '#42A5F5'
        def on_leave_exportar(e):
            btn_exportar['bg'] = '#2196F3'
        btn_exportar.bind("<Enter>", on_enter_exportar)
        btn_exportar.bind("<Leave>", on_leave_exportar)
        
        crear_tooltip(btn_exportar, "💾 Guarda los resultados en un archivo de texto")
        
        # Botón Imprimir con Material Design
        btn_imprimir = tk.Button(
            frame_botones,
            text="🖨️ Imprimir",
            command=self.imprimir,
            bg="#9C27B0",
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#AB47BC",
            activeforeground="#000000",
            borderwidth=0
        )
        btn_imprimir.pack(side='left', padx=6)
        
        def on_enter_imprimir(e):
            btn_imprimir['bg'] = '#AB47BC'
        def on_leave_imprimir(e):
            btn_imprimir['bg'] = '#9C27B0'
        btn_imprimir.bind("<Enter>", on_enter_imprimir)
        btn_imprimir.bind("<Leave>", on_leave_imprimir)
        
        crear_tooltip(btn_imprimir, "🖨️ Imprime los resultados actuales")
        
        # Botón Limpiar con Material Design
        btn_limpiar = tk.Button(
            frame_botones,
            text="🔄 Limpiar",
            command=self.limpiar,
            bg="#FF9800",
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#FFB74D",
            activeforeground="#000000",
            borderwidth=0
        )
        btn_limpiar.pack(side='left', padx=6)
        
        def on_enter_limpiar(e):
            btn_limpiar['bg'] = '#FFB74D'
        def on_leave_limpiar(e):
            btn_limpiar['bg'] = '#FF9800'
        btn_limpiar.bind("<Enter>", on_enter_limpiar)
        btn_limpiar.bind("<Leave>", on_leave_limpiar)
        
        crear_tooltip(btn_limpiar, "🔄 Borra todos los resultados y gráficos mostrados")
        
        # Botón Regresar con Material Design
        btn_regresar = tk.Button(
            frame_botones,
            text="⬅️ Regresar",
            command=self.destroy,
            bg="#607D8B",
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#78909C",
            activeforeground="#000000",
            borderwidth=0
        )
        btn_regresar.pack(side='right', padx=6)
        
        def on_enter_regresar(e):
            btn_regresar['bg'] = '#78909C'
        def on_leave_regresar(e):
            btn_regresar['bg'] = '#607D8B'
        btn_regresar.bind("<Enter>", on_enter_regresar)
        btn_regresar.bind("<Leave>", on_leave_regresar)
        crear_tooltip(btn_regresar, "Vuelve al menú principal sin cerrar la aplicación")
        
        btn_cerrar = tk.Button(
            frame_botones,
            text="❌ Cerrar Ventana",
            command=self.destroy,
            bg=COLOR_DANGER,
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            activebackground="#FFEB3B",
            activeforeground="#000000"
        )
        btn_cerrar.pack(side='right', padx=5)
        crear_tooltip(btn_cerrar, "Cierra esta ventana de análisis")
    
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
    
    def generar_datos_random(self):
        """Genera datos aleatorios para pruebas"""
        try:
            # Crear ventana de diálogo personalizada
            dialogo = tk.Toplevel(self)
            dialogo.title("Generar Datos Aleatorios")
            dialogo.geometry("400x250")
            dialogo.transient(self)
            dialogo.grab_set()
            
            # Centrar el diálogo
            dialogo.update_idletasks()
            x = (dialogo.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialogo.winfo_screenheight() // 2) - (250 // 2)
            dialogo.geometry(f"400x250+{x}+{y}")
            
            tk.Label(
                dialogo,
                text="🎲 Configurar Datos Aleatorios",
                font=("Helvetica", 14, "bold"),
                fg=COLOR_PRIMARY
            ).pack(pady=15)
            
            # Frame para inputs
            frame_inputs = tk.Frame(dialogo)
            frame_inputs.pack(pady=10)
            
            tk.Label(frame_inputs, text="Cantidad de datos:", 
                    font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5, padx=10)
            entry_cantidad = tk.Entry(frame_inputs, width=15, font=("Helvetica", 10))
            entry_cantidad.grid(row=0, column=1, pady=5, padx=10)
            entry_cantidad.insert(0, "100")
            
            tk.Label(frame_inputs, text="Valor mínimo:", 
                    font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5, padx=10)
            entry_min = tk.Entry(frame_inputs, width=15, font=("Helvetica", 10))
            entry_min.grid(row=1, column=1, pady=5, padx=10)
            entry_min.insert(0, "18")
            
            tk.Label(frame_inputs, text="Valor máximo:", 
                    font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5, padx=10)
            entry_max = tk.Entry(frame_inputs, width=15, font=("Helvetica", 10))
            entry_max.grid(row=2, column=1, pady=5, padx=10)
            entry_max.insert(0, "65")
            
            def generar():
                try:
                    cantidad = int(entry_cantidad.get())
                    valor_min = int(entry_min.get())
                    valor_max = int(entry_max.get())
                    
                    if cantidad <= 0:
                        messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                        return
                    
                    if valor_min >= valor_max:
                        messagebox.showerror("Error", "El valor mínimo debe ser menor al máximo")
                        return
                    
                    # Generar datos aleatorios
                    edades = np.random.randint(valor_min, valor_max + 1, cantidad)
                    self.datos = pd.DataFrame({'Edad': edades})
                    
                    info = f"✅ DATOS ALEATORIOS GENERADOS\n\n"
                    info += f"Cantidad de datos: {cantidad}\n"
                    info += f"Rango: {valor_min} - {valor_max}\n"
                    info += f"Media: {edades.mean():.2f}\n"
                    info += f"Mediana: {np.median(edades):.2f}\n"
                    
                    dialogo.destroy()
                    messagebox.showinfo("Éxito", info)
                    
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al generar datos:\n{str(e)}")
            
            # Botones
            frame_botones = tk.Frame(dialogo)
            frame_botones.pack(pady=15)
            
            tk.Button(
                frame_botones,
                text="🎲 Generar",
                command=generar,
                bg=COLOR_SUCCESS,
                fg="#000000",
                font=("Helvetica", 10, "bold"),
                cursor="hand2",
                padx=20,
                pady=8,
                activebackground="#FFEB3B",
                activeforeground="#000000"
            ).pack(side='left', padx=5)
            
            tk.Button(
                frame_botones,
                text="❌ Cancelar",
                command=dialogo.destroy,
                bg=COLOR_DANGER,
                fg="#000000",
                font=("Helvetica", 10, "bold"),
                cursor="hand2",
                padx=20,
                pady=8,
                activebackground="#FFEB3B",
                activeforeground="#000000"
            ).pack(side='left', padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir diálogo:\n{str(e)}")
    
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

# ============= FUNCIÓN HELPER PARA PANELES DE INSTRUCCIONES MODERNOS =============
def crear_panel_instrucciones(parent, titulo, texto, color_bg="#E8F5E9", color_fg="#2E7D32", color_texto="#1B5E20"):
    """
    Crea un panel de instrucciones con estilo moderno y consistente
    
    Args:
        parent: Widget padre
        titulo: Título del panel
        texto: Texto de las instrucciones
        color_bg: Color de fondo (pastel suave)
        color_fg: Color del título (oscuro para contraste)
        color_texto: Color del texto (oscuro legible)
    """
    # Frame externo con sombra sutil
    outer_frame = tk.Frame(parent, bg="#CFD8DC", relief='flat')
    outer_frame.pack(fill='x', padx=10, pady=(0, 15))
    
    # Frame principal con bordes redondeados simulados
    frame_instrucciones = tk.LabelFrame(
        outer_frame,
        text=f"  📖 {titulo}  ",
        font=("Helvetica", 12, "bold"),
        bg=color_bg,
        fg=color_fg,
        relief="flat",
        borderwidth=0,
        labelanchor='n'
    )
    frame_instrucciones.pack(fill='x', padx=2, pady=2)
    
    # Barra decorativa superior
    top_bar = tk.Frame(frame_instrucciones, bg=color_fg, height=3)
    top_bar.pack(fill='x')
    
    # Contenido del panel
    lbl_instrucciones = tk.Label(
        frame_instrucciones,
        text=texto,
        bg=color_bg,
        fg=color_texto,
        font=("Consolas", 9, "normal"),
        justify='left',
        anchor='w',
        padx=15,
        pady=15
    )
    lbl_instrucciones.pack(fill='x', padx=15, pady=15)
    
    return outer_frame

class MenuPrincipal:
    def __init__(self, root, usuario, callback_cerrar_sesion):
        self.root = root
        self.usuario = usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Configurar ventana al 95% de la pantalla
        window_width = int(screen_width * 0.95)
        window_height = int(screen_height * 0.95)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.title(f"{NOMBRE_PROYECTO} - Menú Principal")
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=BG_LIGHT)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        self.crear_barra_superior()
        
        # ===== CREAR CANVAS CON SCROLL PARA EL CONTENIDO =====
        # Frame contenedor
        container = tk.Frame(self.root, bg=BG_LIGHT)
        container.pack(fill='both', expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(container, bg=BG_LIGHT, highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar vertical
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollable
        scrollable_frame = tk.Frame(canvas, bg=BG_LIGHT)
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        
        # Actualizar scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
        
        # Expandir frame al ancho del canvas
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas_width)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Usar scrollable_frame como frame principal
        self.frame_principal = tk.Frame(scrollable_frame, bg=BG_LIGHT)
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
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            activebackground="#FFEB3B",
            activeforeground="#000000"
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
        
        # Tooltips para cada botón
        tooltips_desc = [
            "Genera tablas de frecuencia simple y agrupada con gráficos de barras",
            "Calcula media, mediana, moda, media geométrica y armónica",
            "Determina cuartiles, deciles, percentiles y crea boxplots",
            "Calcula rango, varianza, desviación estándar y coeficiente de variación",
            "Analiza asimetría y curtosis de la distribución de datos"
        ]
        
        botones = [
            ("📊 Cuadros y Gráficos Estadísticos", colores_fondo[0], self.abrir_cuadros),
            ("📈 Medidas de Tendencia Central", colores_fondo[1], self.abrir_tendencia),
            ("📍 Medidas de Posición", colores_fondo[2], self.abrir_posicion),
            ("📏 Medidas de Dispersión", colores_fondo[3], self.abrir_dispersion),
            ("📉 Medidas de Forma", colores_fondo[4], self.abrir_forma),
        ]
        
        for i, (texto, color_fondo, comando) in enumerate(botones):
            btn = tk.Button(
                frame,
                text=texto,
                command=comando,
                bg=color_fondo,
                fg="#000000",
                font=("Helvetica", 13, "bold"),
                width=40,
                height=2,
                relief="raised",
                borderwidth=2,
                cursor="hand2",
                anchor='center',
                padx=10,
                pady=10,
                activebackground="#FFEB3B",
                activeforeground="#000000"
            )
            btn.pack(fill='x', pady=10, padx=10)
            
            # Agregar tooltip
            crear_tooltip(btn, tooltips_desc[i])
            
            # Efectos hover - mantiene texto negro y bold
            def on_enter(e, b=btn):
                b.config(bg="#FFEB3B", relief="sunken", fg="#000000", font=("Helvetica", 13, "bold"))
            
            def on_leave(e, b=btn, original_color=color_fondo):
                b.config(bg=original_color, relief="raised", fg="#000000", font=("Helvetica", 13, "bold"))
            
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
        colores_fondo = ["#FCE4EC", "#F1F8E9", "#FFF9C4", "#E1F5FE", "#FFEBEE", "#E8EAF6"]
        
        # Tooltips para cada botón
        tooltips_inf = [
            "Calcula probabilidades elementales: unión, intersección, complemento",
            "Aplica el teorema de Bayes para probabilidades condicionales",
            "Trabaja con distribuciones Normal, Binomial y Poisson",
            "Calcula correlación entre variables y regresión lineal simple",
            "Prueba de independencia y bondad de ajuste con Chi-cuadrado",
            "Genera árboles de probabilidad con múltiples niveles"
        ]
        
        botones = [
            ("🎲 Cálculo de Probabilidades", colores_fondo[0], self.abrir_probabilidades),
            ("🔄 Teorema de Bayes", colores_fondo[1], self.abrir_bayes),
            ("📊 Distribuciones (Normal, Binomial, Poisson)", colores_fondo[2], self.abrir_distribuciones),
            ("📈 Correlación y Regresión Simple", colores_fondo[3], self.abrir_regresion),
            ("χ² Prueba de Chi-cuadrado", colores_fondo[5], self.abrir_chi_cuadrado),
            ("🌳 Árboles de Decisión", colores_fondo[4], self.abrir_arboles),
        ]
        
        for i, (texto, color_fondo, comando) in enumerate(botones):
            btn = tk.Button(
                frame,
                text=texto,
                command=comando,
                bg=color_fondo,
                fg="#000000",
                font=("Helvetica", 13, "bold"),
                width=40,
                height=2,
                relief="raised",
                borderwidth=2,
                cursor="hand2",
                anchor='center',
                padx=10,
                pady=10,
                activebackground="#FFEB3B",
                activeforeground="#000000"
            )
            btn.pack(fill='x', pady=10, padx=10)
            
            # Agregar tooltip
            crear_tooltip(btn, tooltips_inf[i])
            
            # Efectos hover - mantiene texto negro y bold
            def on_enter(e, b=btn):
                b.config(bg="#FFEB3B", relief="sunken", fg="#000000", font=("Helvetica", 13, "bold"))
            
            def on_leave(e, b=btn, original_color=color_fondo):
                b.config(bg=original_color, relief="raised", fg="#000000", font=("Helvetica", 13, "bold"))
            
            btn.bind("<Enter>", on_leave)
            btn.bind("<Leave>", on_leave)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
# ===== ESTADÍSTICA DESCRIPTIVA =====
    
    def abrir_analisis_completo(self):
        """Análisis Estadístico Completo: Cuadros de Frecuencia + Tendencia Central"""
        ventana = VentanaAnalisis(self.root, "📊 Análisis Estadístico Completo")
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📊 ANÁLISIS ESTADÍSTICO COMPLETO                                    ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 QUÉ INCLUYE:
   → Medidas de Tendencia Central (media, mediana, moda)
   → Cuadros de Frecuencia Simple
   → Cuadros de Frecuencia Agrupada (con intervalos)

🔹 PASO 1: Carga Datos
   → Click en "Cargar CSV"
   → Selecciona archivo con columna "Edad"

🔹 PASO 2: Procesar
   → Click en "Procesar Datos"
   → Navega por las pestañas para ver resultados

🔹 QUÉ VERÁS:
   → Pestaña 1: Tendencia Central (promedios, mediana, moda)
   → Pestaña 2: Frecuencias Simples (conteo por valor)
   → Pestaña 3: Frecuencias Agrupadas (conteo por rangos)

💡 TIP: Ideal para análisis exploratorio de datos numéricos
        """
        
        crear_panel_instrucciones(
            ventana.main_frame,
            "ANÁLISIS ESTADÍSTICO COMPLETO",
            instrucciones_text,
            color_bg="#E1F5FE",
            color_fg="#01579B",
            color_texto="#01579B"
        )
        
        def procesar_datos():
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "Primero debe cargar un archivo CSV")
                return
            
            if 'Edad' not in ventana.datos.columns:
                messagebox.showwarning("Advertencia", 
                    f"La columna 'Edad' no existe.\n\nColumnas disponibles:\n{', '.join(ventana.datos.columns)}")
                return
            
            try:
                datos_edad = ventana.datos['Edad'].dropna()
                
                # ========== CALCULAR TODO ==========
                # Tendencia central
                tendencia = calcular_tendencia_central(datos_edad)
                
                # Cuadros de frecuencia
                dfs = generar_dfs(datos_edad)
                dfsvai = generar_dfsvai(datos_edad)
                
                # ========== CREAR NOTEBOOK CON PESTAÑAS ==========
                # Limpiar notebook si ya existe
                for widget in ventana.notebook.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            child.destroy()
                
                # Pestaña 1: Medidas de Tendencia Central
                tab_tendencia = tk.Frame(ventana.notebook, bg='#FFFFFF')
                ventana.notebook.insert(0, tab_tendencia, text="📈 Tendencia Central")
                
                text_tendencia = tk.Text(tab_tendencia, height=30, width=120,
                    font=("Consolas", 10), wrap=tk.WORD, bg="#FFFFFF", fg="#000000",
                    relief='solid', borderwidth=1, padx=15, pady=15)
                text_tendencia.pack(fill='both', expand=True, padx=10, pady=10)
                
                resultado_tendencia = "=" * 100 + "\n"
                resultado_tendencia += "MEDIDAS DE TENDENCIA CENTRAL\n"
                resultado_tendencia += "=" * 100 + "\n\n"
                
                resultado_tendencia += f"{'Medida':<30} {'Valor':<20} {'Descripción'}\n"
                resultado_tendencia += "-" * 100 + "\n\n"
                
                descripciones = {
                    'Media aritmética': 'Promedio de todos los valores',
                    'Mediana': 'Valor central que divide los datos en dos partes iguales',
                    'Moda': 'Valor(es) que más se repite(n)',
                    'Media Geométrica': 'Raíz n-ésima del producto de n valores',
                    'Media Armónica': 'Recíproco de la media de los recíprocos'
                }
                
                for medida, valor in tendencia.items():
                    desc = descripciones.get(medida, '')
                    resultado_tendencia += f"{medida:<30} {str(valor):<20} {desc}\n"
                
                resultado_tendencia += "\n" + "=" * 100 + "\n"
                resultado_tendencia += "INTERPRETACIÓN\n"
                resultado_tendencia += "=" * 100 + "\n\n"
                
                media = tendencia['Media aritmética']
                mediana = tendencia['Mediana']
                
                resultado_tendencia += f"• El valor promedio es {media}\n"
                resultado_tendencia += f"• El 50% de los datos están por debajo de {mediana}\n"
                resultado_tendencia += f"• Los valores más frecuentes son: {tendencia['Moda']}\n\n"
                
                if media > mediana:
                    resultado_tendencia += f"• La distribución está sesgada hacia la derecha (media > mediana)\n"
                elif media < mediana:
                    resultado_tendencia += f"• La distribución está sesgada hacia la izquierda (media < mediana)\n"
                else:
                    resultado_tendencia += f"• La distribución es simétrica (media = mediana)\n"
                
                text_tendencia.insert(tk.END, resultado_tendencia)
                
                # Pestaña 2: Cuadros de Frecuencia
                tab_frecuencia = tk.Frame(ventana.notebook, bg='#FFFFFF')
                ventana.notebook.insert(1, tab_frecuencia, text="📋 Cuadros de Frecuencia")
                
                text_frecuencia = tk.Text(tab_frecuencia, height=30, width=120,
                    font=("Consolas", 10), wrap=tk.WORD, bg="#FFFFFF", fg="#000000",
                    relief='solid', borderwidth=1, padx=15, pady=15)
                text_frecuencia.pack(fill='both', expand=True, padx=10, pady=10)
                
                resultado_frecuencia = "=" * 100 + "\n"
                resultado_frecuencia += "CUADRO DE FRECUENCIA SIMPLE\n"
                resultado_frecuencia += "=" * 100 + "\n\n"
                resultado_frecuencia += dfs.to_string(index=False) + "\n\n"
                
                resultado_frecuencia += "=" * 100 + "\n"
                resultado_frecuencia += "CUADRO DE FRECUENCIA AGRUPADA (CON INTERVALOS)\n"
                resultado_frecuencia += "=" * 100 + "\n\n"
                resultado_frecuencia += dfsvai.to_string(index=False) + "\n\n"
                
                resultado_frecuencia += "=" * 100 + "\n"
                resultado_frecuencia += "ESTADÍSTICAS BÁSICAS\n"
                resultado_frecuencia += "=" * 100 + "\n\n"
                resultado_frecuencia += f"Número total de datos: {len(datos_edad)}\n"
                resultado_frecuencia += f"Valor mínimo: {datos_edad.min()}\n"
                resultado_frecuencia += f"Valor máximo: {datos_edad.max()}\n"
                resultado_frecuencia += f"Rango: {datos_edad.max() - datos_edad.min()}\n"
                
                text_frecuencia.insert(tk.END, resultado_frecuencia)
                
                # Pestaña 3: Resumen General
                tab_resumen = tk.Frame(ventana.notebook, bg='#FFFFFF')
                ventana.notebook.insert(2, tab_resumen, text="📊 Resumen General")
                
                text_resumen = tk.Text(tab_resumen, height=30, width=120,
                    font=("Consolas", 11), wrap=tk.WORD, bg="#FFFFFF", fg="#000000",
                    relief='solid', borderwidth=1, padx=15, pady=15)
                text_resumen.pack(fill='both', expand=True, padx=10, pady=10)
                
                resumen = "=" * 100 + "\n"
                resumen += "RESUMEN ESTADÍSTICO COMPLETO\n"
                resumen += "=" * 100 + "\n\n"
                
                resumen += f"📊 CONJUNTO DE DATOS\n"
                resumen += f"   • Total de observaciones: {len(datos_edad)}\n"
                resumen += f"   • Rango de valores: {datos_edad.min()} - {datos_edad.max()}\n"
                resumen += f"   • Amplitud del rango: {datos_edad.max() - datos_edad.min()}\n\n"
                
                resumen += f"📈 MEDIDAS DE TENDENCIA CENTRAL\n"
                resumen += f"   • Media aritmética: {media}\n"
                resumen += f"   • Mediana: {mediana}\n"
                resumen += f"   • Moda: {tendencia['Moda']}\n"
                resumen += f"   • Media geométrica: {tendencia['Media Geométrica']}\n"
                resumen += f"   • Media armónica: {tendencia['Media Armónica']}\n\n"
                
                resumen += f"📋 DISTRIBUCIÓN DE FRECUENCIAS\n"
                resumen += f"   • Valores únicos: {len(dfs)}\n"
                resumen += f"   • Intervalos de clase: {len(dfsvai)}\n"
                resumen += f"   • Valor más frecuente: {dfs.loc[dfs['Frecuencia'].idxmax(), 'Valor']} "
                resumen += f"(aparece {dfs['Frecuencia'].max()} veces)\n\n"
                
                resumen += f"🎯 INTERPRETACIÓN\n"
                if media > mediana:
                    resumen += f"   • Distribución: Sesgada a la derecha (asimétrica positiva)\n"
                    resumen += f"   • Significado: Hay más valores pequeños y algunos valores grandes que elevan la media\n"
                elif media < mediana:
                    resumen += f"   • Distribución: Sesgada a la izquierda (asimétrica negativa)\n"
                    resumen += f"   • Significado: Hay más valores grandes y algunos valores pequeños que reducen la media\n"
                else:
                    resumen += f"   • Distribución: Simétrica\n"
                    resumen += f"   • Significado: Los datos están equilibrados alrededor del centro\n"
                
                text_resumen.insert(tk.END, resumen)
                
                # ========== GRÁFICOS ==========
                try:
                    # Crear figura con múltiples subplots
                    fig = plt.figure(figsize=(16, 10))
                    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
                    
                    # Subplot 1: Histograma con medidas de tendencia
                    ax1 = fig.add_subplot(gs[0, 0])
                    ax1.hist(datos_edad, bins=20, alpha=0.7, color='steelblue', 
                            edgecolor='black', label='Frecuencia')
                    ax1.axvline(media, color='red', linestyle='--', linewidth=2, 
                               label=f'Media = {media:.2f}')
                    ax1.axvline(mediana, color='green', linestyle='--', linewidth=2, 
                               label=f'Mediana = {mediana:.2f}')
                    
                    modas = tendencia['Moda']
                    if isinstance(modas, list):
                        for i, moda in enumerate(modas):
                            if i == 0:
                                ax1.axvline(moda, color='orange', linestyle=':', linewidth=2, 
                                           alpha=0.7, label='Moda')
                            else:
                                ax1.axvline(moda, color='orange', linestyle=':', linewidth=2, alpha=0.7)
                    
                    ax1.set_xlabel('Edad', fontsize=11)
                    ax1.set_ylabel('Frecuencia', fontsize=11)
                    ax1.set_title('Distribución con Medidas de Tendencia Central', 
                                 fontsize=12, fontweight='bold')
                    ax1.legend(fontsize=9)
                    ax1.grid(True, alpha=0.3)
                    
                    # Subplot 2: Frecuencia simple
                    ax2 = fig.add_subplot(gs[0, 1])
                    positions = range(len(dfs))
                    bars = ax2.bar(positions, dfs['Frecuencia'], color='steelblue', 
                                  edgecolor='black', alpha=0.7)
                    for bar, height in zip(bars, dfs['Frecuencia']):
                        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                f'{int(height)}', ha='center', va='bottom', fontsize=8)
                    ax2.set_xticks(positions[::max(1, len(positions)//10)])
                    ax2.set_xticklabels(dfs['Valor'].astype(str).tolist()[::max(1, len(positions)//10)], 
                                       rotation=45, ha='right')
                    ax2.set_xlabel('Valor', fontsize=11)
                    ax2.set_ylabel('Frecuencia', fontsize=11)
                    ax2.set_title('Distribución de Frecuencia Simple', fontsize=12, fontweight='bold')
                    ax2.grid(True, alpha=0.3, axis='y')
                    
                    # Subplot 3: Frecuencia agrupada
                    ax3 = fig.add_subplot(gs[1, 0])
                    positions = range(len(dfsvai))
                    bars = ax3.bar(positions, dfsvai['Frecuencia'], color='coral', 
                                  edgecolor='black', alpha=0.7)
                    for bar, height in zip(bars, dfsvai['Frecuencia']):
                        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                f'{int(height)}', ha='center', va='bottom', fontsize=8)
                    labels = dfsvai['Intervalo'].astype(str).tolist()
                    ax3.set_xticks(positions)
                    ax3.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
                    ax3.set_xlabel('Intervalo', fontsize=11)
                    ax3.set_ylabel('Frecuencia', fontsize=11)
                    ax3.set_title('Distribución de Frecuencia Agrupada', fontsize=12, fontweight='bold')
                    ax3.grid(True, alpha=0.3, axis='y')
                    
                    # Subplot 4: Comparación de medidas
                    ax4 = fig.add_subplot(gs[1, 1])
                    medidas = ['Media', 'Mediana', 'M.Geom', 'M.Arm']
                    valores = [media, mediana, tendencia['Media Geométrica'], 
                              tendencia['Media Armónica']]
                    colores_barras = ['#E74C3C', '#27AE60', '#3498DB', '#F39C12']
                    bars = ax4.bar(medidas, valores, color=colores_barras, 
                                  edgecolor='black', alpha=0.7)
                    for bar, valor in zip(bars, valores):
                        ax4.text(bar.get_x() + bar.get_width()/2., valor + 0.3,
                                f'{valor:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
                    ax4.set_ylabel('Valor', fontsize=11)
                    ax4.set_title('Comparación de Medidas de Tendencia Central', 
                                 fontsize=12, fontweight='bold')
                    ax4.grid(True, alpha=0.3, axis='y')
                    
                    plt.tight_layout()
                    ventana.mostrar_grafico(fig)
                    
                except Exception as e:
                    print(f"Error al generar gráficos: {e}")
                    import traceback
                    traceback.print_exc()
                    messagebox.showwarning("Advertencia", 
                        "Los datos se procesaron pero hubo un error al generar los gráficos")
                
                # Cambiar a la primera pestaña
                ventana.notebook.select(0)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar datos:\n\n{str(e)}")
                import traceback
                traceback.print_exc()
        
        # Botón para procesar después de cargar datos
        btn_procesar = tk.Button(
            ventana.btn_frame,
            text="▶️ Procesar Datos Cargados",
            command=procesar_datos,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=FONT_BUTTON,
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        )
        btn_procesar.pack(pady=10)
    
    def abrir_cuadros(self):
        """Cuadros de Frecuencia Simple y Agrupada"""
        ventana = VentanaAnalisis(self.root, "📊 Cuadros y Gráficos Estadísticos")
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📊 CUADROS Y GRÁFICOS DE FRECUENCIA                                 ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 PASO 1: Carga tus datos
   → Click en "📁 Cargar CSV" o "🎲 Generar Datos Aleatorios"
   
🔹 PASO 2: Procesa la información
   → Click en "▶️ Procesar Datos Cargados"
   → Se generarán tablas de frecuencia simple y agrupada
   
🔹 PASO 3: Analiza resultados (OPCIONAL)
   → Click en "📈 Ver Tendencia Central" para medidas adicionales
   
📊 QUÉ VERÁS:
   ✓ Tabla de frecuencia simple (valores individuales)
   ✓ Tabla de frecuencia agrupada (intervalos/clases)
   ✓ Gráficos de barras automáticos
   ✓ Estadísticas básicas (min, max, rango)

💡 TIP: La columna debe llamarse "Edad" o modifica el código
        """
        
        crear_panel_instrucciones(
            ventana.text_frame,
            "INSTRUCCIONES DE USO",
            instrucciones_text,
            color_bg="#E8F5E9",
            color_fg="#2E7D32",
            color_texto="#1B5E20"
        )
        
        def procesar_datos():
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "❌ Primero debe cargar un archivo CSV")
                return
            
            if 'Edad' not in ventana.datos.columns:
                messagebox.showwarning("Advertencia", 
                    f"❌ La columna 'Edad' no existe.\n\n📋 Columnas disponibles:\n{', '.join(ventana.datos.columns)}")
                return
            
            try:
                datos_edad = ventana.datos['Edad'].dropna()
                
                # Generar cuadros
                dfs = generar_dfs(datos_edad)
                dfsvai = generar_dfsvai(datos_edad)
                
                # ============= FORMATEAR RESULTADOS CON ESTILO =============
                resultado = ""
                
                # Header principal
                resultado += "╔" + "═" * 98 + "╗\n"
                resultado += "║" + " " * 28 + "📊 CUADRO DE FRECUENCIA SIMPLE" + " " * 39 + "║\n"
                resultado += "╚" + "═" * 98 + "╝\n\n"
                
                # Tabla con formato mejorado
                resultado += dfs.to_string(index=False) + "\n\n"
                
                # Segunda tabla
                resultado += "╔" + "═" * 98 + "╗\n"
                resultado += "║" + " " * 20 + "📊 CUADRO DE FRECUENCIA AGRUPADA (CON INTERVALOS)" + " " * 29 + "║\n"
                resultado += "╚" + "═" * 98 + "╝\n\n"
                
                resultado += dfsvai.to_string(index=False) + "\n\n"
                
                # Estadísticas en formato visual
                resultado += "╔" + "═" * 98 + "╗\n"
                resultado += "║" + " " * 35 + "📈 ESTADÍSTICAS BÁSICAS" + " " * 40 + "║\n"
                resultado += "╚" + "═" * 98 + "╝\n\n"
                
                stats = [
                    ("📊 Número total de datos", len(datos_edad)),
                    ("🔽 Valor mínimo", datos_edad.min()),
                    ("🔼 Valor máximo", datos_edad.max()),
                    ("📏 Rango (max - min)", datos_edad.max() - datos_edad.min()),
                    ("📍 Media aproximada", f"{datos_edad.mean():.2f}"),
                    ("🎯 Mediana aproximada", f"{datos_edad.median():.2f}")
                ]
                
                for stat_name, stat_value in stats:
                    resultado += f"  {stat_name:<30} →  {stat_value}\n"
                
                resultado += "\n" + "─" * 100 + "\n"
                resultado += "💡 INTERPRETACIÓN:\n"
                resultado += f"   • Los datos van desde {datos_edad.min()} hasta {datos_edad.max()}\n"
                resultado += f"   • El rango de variación es de {datos_edad.max() - datos_edad.min()} unidades\n"
                resultado += f"   • El valor central aproximado es {datos_edad.median():.2f}\n"
                
                ventana.mostrar_texto(resultado)
                
                # Generar gráficos
                try:
                    # Gráfico de frecuencia simple
                    fig_simple = graficar_frecuencia(dfs, 'simple', 
                        titulo_simple='Distribución de Frecuencia Simple')
                    
                    # Gráfico de frecuencia agrupada
                    fig_agrupada = graficar_frecuencia(dfsvai, 'agrupada', 
                        titulo_agrupada='Distribución de Frecuencia Agrupada')
                    
                    # Mostrar el gráfico agrupado en la ventana principal
                    ventana.mostrar_grafico(fig_agrupada)
                    
                    # Mostrar el gráfico simple en una ventana separada
                    plt.figure(fig_simple.number)
                    plt.show()
                    
                except Exception as e:
                    print(f"Error al generar gráficos: {e}")
                    import traceback
                    traceback.print_exc()
                    messagebox.showwarning("Advertencia", 
                        "✅ Los datos se procesaron pero hubo un error al generar los gráficos")
                
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al procesar datos:\n\n{str(e)}")
        
        def ver_tendencia_central():
            """Muestra medidas de tendencia central para los datos cargados"""
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "❌ Primero debe cargar y procesar datos")
                return
            
            if 'Edad' not in ventana.datos.columns:
                messagebox.showwarning("Advertencia", "❌ La columna 'Edad' no existe")
                return
            
            try:
                datos_edad = ventana.datos['Edad'].dropna()
                tendencia = calcular_tendencia_central(datos_edad)
                
                # Crear ventana emergente con resultados
                ventana_tend = tk.Toplevel(ventana)
                ventana_tend.title("📈 Medidas de Tendencia Central")
                ventana_tend.geometry("800x600")
                
                # Frame principal con scroll
                frame_scroll = tk.Frame(ventana_tend)
                frame_scroll.pack(fill='both', expand=True, padx=10, pady=10)
                
                text_widget = scrolledtext.ScrolledText(
                    frame_scroll,
                    wrap=tk.WORD,
                    font=("Courier New", 10),
                    bg="#FFFEF7",
                    fg="#1A237E"
                )
                text_widget.pack(fill='both', expand=True)
                
                # Formatear resultados
                resultado = ""
                resultado += "╔" + "═" * 78 + "╗\n"
                resultado += "║" + " " * 20 + "📈 MEDIDAS DE TENDENCIA CENTRAL" + " " * 27 + "║\n"
                resultado += "╚" + "═" * 78 + "╝\n\n"
                
                # Crear tabla visual
                resultado += f"{'MEDIDA':<30} {'VALOR':<15} {'DESCRIPCIÓN'}\n"
                resultado += "─" * 80 + "\n\n"
                
                medidas_info = [
                    ('📊 Media Aritmética', tendencia['Media aritmética'], 
                     'Promedio de todos los valores'),
                    ('🎯 Mediana', tendencia['Mediana'], 
                     'Valor central (50%)'),
                    ('🔢 Moda', tendencia['Moda'], 
                     'Valor(es) más frecuente(s)'),
                    ('📐 Media Geométrica', tendencia['Media Geométrica'], 
                     'Raíz n del producto'),
                    ('⚖️ Media Armónica', tendencia['Media Armónica'], 
                     'Para promedios de tasas')
                ]
                
                for medida, valor, desc in medidas_info:
                    resultado += f"{medida:<30} {str(valor):<15.2f} {desc}\n" if isinstance(valor, (int, float)) else f"{medida:<30} {str(valor):<15} {desc}\n"
                
                resultado += "\n" + "╔" + "═" * 78 + "╗\n"
                resultado += "║" + " " * 28 + "💡 INTERPRETACIÓN" + " " * 32 + "║\n"
                resultado += "╚" + "═" * 78 + "╝\n\n"
                
                media = tendencia['Media aritmética']
                mediana = tendencia['Mediana']
                
                resultado += f"  ✓ El valor promedio es {media:.2f}\n"
                resultado += f"  ✓ El 50% de los datos están por debajo de {mediana:.2f}\n"
                resultado += f"  ✓ Los valores más frecuentes son: {tendencia['Moda']}\n\n"
                
                if media > mediana:
                    resultado += f"  📊 Distribución SESGADA A LA DERECHA (media > mediana)\n"
                    resultado += f"      → Hay valores extremos altos que elevan la media\n"
                elif media < mediana:
                    resultado += f"  📊 Distribución SESGADA A LA IZQUIERDA (media < mediana)\n"
                    resultado += f"      → Hay valores extremos bajos que reducen la media\n"
                else:
                    resultado += f"  📊 Distribución SIMÉTRICA (media = mediana)\n"
                    resultado += f"      → Los datos están balanceados alrededor del centro\n"
                
                text_widget.insert('1.0', resultado)
                text_widget.config(state='disabled')
                
                # Botón cerrar
                btn_cerrar = tk.Button(
                    ventana_tend,
                    text="✖ Cerrar",
                    command=ventana_tend.destroy,
                    bg="#E53935",
                    fg="#000000",
                    font=("Helvetica", 11, "bold"),
                    cursor="hand2"
                )
                btn_cerrar.pack(pady=10)
                
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al calcular tendencia:\n\n{str(e)}")
        
        # ============= FRAME DE BOTONES CON DISEÑO MEJORADO =============
        frame_botones_custom = tk.Frame(ventana.btn_frame, bg=BG_WHITE)
        frame_botones_custom.pack(pady=15)
        
        # Botón principal procesar
        btn_procesar = tk.Button(
            frame_botones_custom,
            text="▶️ PROCESAR DATOS CARGADOS",
            command=procesar_datos,
            bg="#4CAF50",
            fg="#000000",
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
            width=30,
            height=2,
            relief="raised",
            borderwidth=3,
            activebackground="#66BB6A",
            activeforeground="#000000"
        )
        btn_procesar.grid(row=0, column=0, padx=10, pady=5)
        
        # Botón tendencia central
        btn_tendencia = tk.Button(
            frame_botones_custom,
            text="📈 VER TENDENCIA CENTRAL",
            command=ver_tendencia_central,
            bg="#2196F3",
            fg="#000000",
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
            width=30,
            height=2,
            relief="raised",
            borderwidth=3,
            activebackground="#42A5F5",
            activeforeground="#000000"
        )
        btn_tendencia.grid(row=0, column=1, padx=10, pady=5)
    
    def abrir_tendencia(self):
        """Medidas de Tendencia Central"""
        ventana = VentanaAnalisis(self.root, "📈 Medidas de Tendencia Central")
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📈 MEDIDAS DE TENDENCIA CENTRAL                                     ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 PASO 1: Carga tus datos
   → Click en "📁 Cargar CSV" o "🎲 Generar Datos Aleatorios"
   
🔹 PASO 2: Procesa la información
   → Click en "▶️ CALCULAR MEDIDAS"
   → Se calcularán todas las medidas de tendencia central
   
📊 MEDIDAS QUE SE CALCULAN:
   ✓ Media Aritmética → Promedio simple de los datos
   ✓ Mediana → Valor central que divide los datos en 2 partes iguales
   ✓ Moda → Valor(es) que más se repite(n)
   ✓ Media Geométrica → Útil para tasas de crecimiento
   ✓ Media Armónica → Útil para promediar velocidades o tasas

📈 GRÁFICO INCLUIDO:
   • Histograma con líneas que marcan media, mediana y moda
   • Interpretación automática del sesgo de la distribución

💡 TIP: Si media = mediana, la distribución es simétrica
        """
        
        crear_panel_instrucciones(
            ventana.text_frame,
            "INSTRUCCIONES DE USO",
            instrucciones_text,
            color_bg="#E3F2FD",
            color_fg="#1565C0",
            color_texto="#0D47A1"
        )
        
        def procesar_datos():
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "❌ Primero debe cargar un archivo CSV")
                return
            
            if 'Edad' not in ventana.datos.columns:
                messagebox.showwarning("Advertencia", 
                    f"❌ La columna 'Edad' no existe.\n\n📋 Columnas disponibles:\n{', '.join(ventana.datos.columns)}")
                return
            
            try:
                datos_edad = ventana.datos['Edad'].dropna()
                
                # Calcular medidas
                tendencia = calcular_tendencia_central(datos_edad)
                
                # ============= FORMATEAR RESULTADOS CON ESTILO =============
                resultado = ""
                
                resultado += "╔" + "═" * 98 + "╗\n"
                resultado += "║" + " " * 28 + "📈 MEDIDAS DE TENDENCIA CENTRAL" + " " * 38 + "║\n"
                resultado += "╚" + "═" * 98 + "╝\n\n"
                
                resultado += f"{'MEDIDA':<35} {'VALOR':<20} {'DESCRIPCIÓN'}\n"
                resultado += "─" * 100 + "\n\n"
                
                medidas_display = [
                    ('📊 Media Aritmética', tendencia['Media aritmética'], 
                     'Promedio de todos los valores'),
                    ('🎯 Mediana', tendencia['Mediana'], 
                     'Valor central (divide datos 50-50)'),
                    ('🔢 Moda', tendencia['Moda'], 
                     'Valor(es) más frecuente(s)'),
                    ('📐 Media Geométrica', tendencia['Media Geométrica'], 
                     'Raíz n-ésima del producto de n valores'),
                    ('⚖️ Media Armónica', tendencia['Media Armónica'], 
                     'Recíproco de la media de recíprocos')
                ]
                
                for medida, valor, desc in medidas_display:
                    if isinstance(valor, (int, float)):
                        resultado += f"{medida:<35} {valor:<20.4f} {desc}\n"
                    else:
                        resultado += f"{medida:<35} {str(valor):<20} {desc}\n"
                
                resultado += "\n" + "╔" + "═" * 98 + "╗\n"
                resultado += "║" + " " * 35 + "💡 INTERPRETACIÓN" + " " * 45 + "║\n"
                resultado += "╚" + "═" * 98 + "╝\n\n"
                
                media = tendencia['Media aritmética']
                mediana = tendencia['Mediana']
                
                resultado += f"  ✓ El valor promedio es: {media:.2f}\n"
                resultado += f"  ✓ El 50% de los datos están por debajo de: {mediana:.2f}\n"
                resultado += f"  ✓ Los valores más frecuentes son: {tendencia['Moda']}\n\n"
                
                resultado += "  📊 ANÁLISIS DE SIMETRÍA:\n"
                if abs(media - mediana) < 0.1:
                    resultado += f"     → Distribución SIMÉTRICA (media ≈ mediana)\n"
                    resultado += f"     → Los datos están balanceados alrededor del centro\n"
                elif media > mediana:
                    resultado += f"     → Distribución SESGADA A LA DERECHA (media > mediana)\n"
                    resultado += f"     → Hay valores extremos altos que elevan la media\n"
                    resultado += f"     → La mayoría de datos están por debajo de la media\n"
                else:
                    resultado += f"     → Distribución SESGADA A LA IZQUIERDA (media < mediana)\n"
                    resultado += f"     → Hay valores extremos bajos que reducen la media\n"
                    resultado += f"     → La mayoría de datos están por encima de la media\n"
                
                resultado += "\n  📈 RECOMENDACIÓN:\n"
                if abs(media - mediana) < 0.5:
                    resultado += f"     → Usa la MEDIA como medida representativa\n"
                else:
                    resultado += f"     → Usa la MEDIANA (más robusta ante valores extremos)\n"
                
                ventana.mostrar_texto(resultado)
                
                # Generar gráfico mejorado
                try:
                    fig = plt.figure(figsize=(14, 7))
                    
                    # Histograma con estilo mejorado
                    n, bins, patches = plt.hist(datos_edad, bins=20, alpha=0.7, 
                                                color='#64B5F6', edgecolor='#1976D2', 
                                                linewidth=1.5, label='Frecuencia')
                    
                    # Colorear el bin de la moda
                    if isinstance(tendencia['Moda'], list):
                        moda_val = tendencia['Moda'][0]
                    else:
                        moda_val = tendencia['Moda']
                    
                    # Líneas de tendencia con estilo
                    plt.axvline(media, color='#D32F2F', linestyle='--', linewidth=2.5, 
                               label=f'Media = {media:.2f}', alpha=0.9)
                    plt.axvline(mediana, color='#388E3C', linestyle='--', linewidth=2.5, 
                               label=f'Mediana = {mediana:.2f}', alpha=0.9)
                    
                    # Marcar modas
                    modas = tendencia['Moda']
                    if isinstance(modas, list):
                        for i, moda in enumerate(modas):
                            plt.axvline(moda, color='#FF6F00', linestyle=':', linewidth=2, 
                                       alpha=0.7, label=f'Moda {i+1} = {moda}' if i == 0 else '')
                    
                    plt.xlabel('Valores', fontsize=13, fontweight='bold')
                    plt.ylabel('Frecuencia', fontsize=13, fontweight='bold')
                    plt.title('📈 Distribución con Medidas de Tendencia Central', 
                             fontsize=15, fontweight='bold', pad=20)
                    plt.legend(fontsize=11, loc='best', framealpha=0.9)
                    plt.grid(True, alpha=0.3, linestyle='--')
                    plt.tight_layout()
                    
                    ventana.mostrar_grafico(fig)
                    
                except Exception as e:
                    print(f"Error al generar gráfico: {e}")
                
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al procesar datos:\n\n{str(e)}")
        
        # Botón con diseño mejorado
        btn_procesar = tk.Button(
            ventana.btn_frame,
            text="▶️ CALCULAR MEDIDAS",
            command=procesar_datos,
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
        btn_procesar.pack(pady=15)
    
    def abrir_posicion(self):
        """Medidas de Posición"""
        ventana = VentanaAnalisis(self.root, "📍 Medidas de Posición")
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📍 MEDIDAS DE POSICIÓN (CUARTILES, DECILES, PERCENTILES)           ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 PASO 1: Carga tus datos
   → Click en "📁 Cargar CSV" o "🎲 Generar Datos Aleatorios"
   
🔹 PASO 2: Procesa la información
   → Click en "▶️ CALCULAR MEDIDAS DE POSICIÓN"
   → Se generarán cuartiles, deciles y percentiles
   
📊 MEDIDAS QUE SE CALCULAN:
   ✓ Cuartiles (Q1, Q2, Q3) → Dividen datos en 4 partes iguales
   ✓ Deciles (D1-D9) → Dividen datos en 10 partes iguales
   ✓ Percentiles (P10, P25, P50, P75, P90) → Dividen en 100 partes
   ✓ Rango Intercuartílico (IQR) → Dispersión del 50% central

📈 GRÁFICO INCLUIDO:
   • Diagrama de Caja (Boxplot) con cuartiles y valores atípicos

💡 TIP: El Q2 (segundo cuartil) es igual a la mediana
        """
        
        crear_panel_instrucciones(
            ventana.text_frame,
            "INSTRUCCIONES DE USO",
            instrucciones_text,
            color_bg="#F3E5F5",
            color_fg="#7B1FA2",
            color_texto="#4A148C"
        )
        
        def procesar_datos():
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "Primero debe cargar un archivo CSV")
                return
            
            if 'Edad' not in ventana.datos.columns:
                messagebox.showwarning("Advertencia", 
                    f"La columna 'Edad' no existe.\n\nColumnas disponibles:\n{', '.join(ventana.datos.columns)}")
                return
            
            try:
                datos_edad = ventana.datos['Edad'].dropna()
                
                # Generar tabla
                tabla = generar_tabla_posicion(datos_edad)
                
                # Formatear resultados
                resultado = "=" * 120 + "\n"
                resultado += "MEDIDAS DE POSICIÓN (Cuartiles, Deciles, Percentiles)\n"
                resultado += "=" * 120 + "\n\n"
                resultado += tabla.to_string(index=False) + "\n\n"
                
                resultado += "=" * 120 + "\n"
                resultado += "INTERPRETACIÓN\n"
                resultado += "=" * 120 + "\n\n"
                resultado += "• Los cuartiles dividen los datos en 4 partes iguales (25% cada una)\n"
                resultado += "• Los deciles dividen los datos en 10 partes iguales (10% cada una)\n"
                resultado += "• Los percentiles dividen los datos en 100 partes iguales (1% cada una)\n"
                resultado += "• El rango intercuartílico (IQR) contiene el 50% central de los datos\n"
                
                ventana.mostrar_texto(resultado)
                
                # Generar gráfico
                try:
                    fig = crear_boxplot(datos_edad, 
                        titulo="Diagrama de Caja - Medidas de Posición")
                    ventana.mostrar_grafico(fig)
                except Exception as e:
                    print(f"Error al generar gráfico: {e}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar datos:\n\n{str(e)}")
        
        btn_procesar = tk.Button(
            ventana.btn_frame,
            text="▶️ Procesar Datos Cargados",
            command=procesar_datos,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=FONT_BUTTON,
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        )
        btn_procesar.pack(pady=10)
    
    def abrir_dispersion(self):
        """Medidas de Dispersión"""
        ventana = VentanaAnalisis(self.root, "📏 Medidas de Dispersión")
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📏 MEDIDAS DE DISPERSIÓN (VARIABILIDAD DE LOS DATOS)                ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 PASO 1: Carga tus datos
   → Click en "📁 Cargar CSV" o "🎲 Generar Datos Aleatorios"
   
🔹 PASO 2: Procesa la información
   → Click en "▶️ CALCULAR MEDIDAS DE DISPERSIÓN"
   → Se analizará la variabilidad de los datos
   
📊 MEDIDAS QUE SE CALCULAN:
   ✓ Rango → Diferencia entre máximo y mínimo
   ✓ Rango Intercuartílico (IQR) → Dispersión del 50% central
   ✓ Varianza → Promedio de desviaciones al cuadrado
   ✓ Desviación Estándar → Raíz de la varianza
   ✓ Coeficiente de Variación (CV) → Dispersión relativa en %

📈 INTERPRETACIÓN DEL CV:
   • CV < 15% → Datos muy homogéneos
   • CV 15-30% → Variabilidad moderada
   • CV > 30% → Datos muy heterogéneos

💡 TIP: Desviación estándar baja = datos concentrados
        """
        
        crear_panel_instrucciones(
            ventana.text_frame,
            "INSTRUCCIONES DE USO",
            instrucciones_text,
            color_bg="#E0F2F1",
            color_fg="#00695C",
            color_texto="#004D40"
        )
        
        def procesar_datos():
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "Primero debe cargar un archivo CSV")
                return
            
            if 'Edad' not in ventana.datos.columns:
                messagebox.showwarning("Advertencia", 
                    f"La columna 'Edad' no existe.\n\nColumnas disponibles:\n{', '.join(ventana.datos.columns)}")
                return
            
            try:
                datos_edad = ventana.datos['Edad'].dropna()
                
                # Generar tabla
                tabla = generar_tabla_dispersion(datos_edad)
                
                # Formatear resultados
                resultado = "=" * 120 + "\n"
                resultado += "MEDIDAS DE DISPERSIÓN\n"
                resultado += "=" * 120 + "\n\n"
                resultado += tabla.to_string(index=False) + "\n\n"
                
                resultado += "=" * 120 + "\n"
                resultado += "¿QUÉ SIGNIFICAN ESTAS MEDIDAS?\n"
                resultado += "=" * 120 + "\n\n"
                resultado += "• RANGO: Diferencia entre el valor máximo y mínimo\n"
                resultado += "• IQR: Rango donde se concentra el 50% central de los datos\n"
                resultado += "• VARIANZA: Promedio de las desviaciones al cuadrado\n"
                resultado += "• DESVIACIÓN ESTÁNDAR: Raíz cuadrada de la varianza (misma unidad que los datos)\n"
                resultado += "• COEFICIENTE DE VARIACIÓN: Medida relativa de dispersión (útil para comparar)\n"
                resultado += "  - CV < 15%: Datos muy homogéneos\n"
                resultado += "  - CV 15-30%: Variabilidad moderada\n"
                resultado += "  - CV > 30%: Datos muy heterogéneos\n"
                
                ventana.mostrar_texto(resultado)
                
                # Generar gráfico
                try:
                    fig = graficar_dispersion(datos_edad, 
                        titulo="Análisis de Dispersión de los Datos")
                    ventana.mostrar_grafico(fig)
                except Exception as e:
                    print(f"Error al generar gráfico: {e}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar datos:\n\n{str(e)}")
        
        btn_procesar = tk.Button(
            ventana.btn_frame,
            text="▶️ Procesar Datos Cargados",
            command=procesar_datos,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=FONT_BUTTON,
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        )
        btn_procesar.pack(pady=10)
    
    def abrir_forma(self):
        """Medidas de Forma"""
        ventana = VentanaAnalisis(self.root, "📉 Medidas de Forma")
        
        # ============= PANEL DE INSTRUCCIONES =============
        instrucciones_text = """
╔══════════════════════════════════════════════════════════════════════╗
║  📉 MEDIDAS DE FORMA (ASIMETRÍA Y CURTOSIS)                          ║
╚══════════════════════════════════════════════════════════════════════╝

🔹 PASO 1: Carga tus datos
   → Click en "📁 Cargar CSV" o "🎲 Generar Datos Aleatorios"
   
🔹 PASO 2: Procesa la información
   → Click en "▶️ CALCULAR MEDIDAS DE FORMA"
   → Se analizará la forma de la distribución
   
📊 MEDIDAS QUE SE CALCULAN:
   ✓ Coeficiente de Asimetría (Skewness)
   ✓ Coeficiente de Curtosis (Kurtosis)
   
📈 INTERPRETACIÓN ASIMETRÍA:
   • = 0 → Distribución simétrica (normal)
   • > 0 → Asimetría positiva (cola derecha larga)
   • < 0 → Asimetría negativa (cola izquierda larga)

📈 INTERPRETACIÓN CURTOSIS:
   • = 3 → Distribución normal (mesocúrtica)
   • > 3 → Distribución leptocúrtica (pico alto)
   • < 3 → Distribución platicúrtica (pico bajo)

💡 TIP: Valores entre -0.5 y 0.5 indican simetría aproximada
        """
        
        crear_panel_instrucciones(
            ventana.text_frame,
            "INSTRUCCIONES DE USO",
            instrucciones_text,
            color_bg="#FCE4EC",
            color_fg="#C2185B",
            color_texto="#880E4F"
        )
        
        def procesar_datos():
            if ventana.datos is None:
                messagebox.showwarning("Advertencia", "Primero debe cargar un archivo CSV")
                return
            
            if 'Edad' not in ventana.datos.columns:
                messagebox.showwarning("Advertencia", 
                    f"La columna 'Edad' no existe.\n\nColumnas disponibles:\n{', '.join(ventana.datos.columns)}")
                return
            
            try:
                datos_edad = ventana.datos['Edad'].dropna()
                
                # Generar tabla y análisis
                tabla = generar_tabla_forma(datos_edad)
                analisis = analisis_completo_forma(datos_edad)
                
                # Formatear resultados
                resultado = "=" * 120 + "\n"
                resultado += "MEDIDAS DE FORMA (Asimetría y Curtosis)\n"
                resultado += "=" * 120 + "\n\n"
                resultado += tabla.to_string(index=False) + "\n\n"
                
                resultado += "=" * 120 + "\n"
                resultado += "INTERPRETACIÓN DETALLADA\n"
                resultado += "=" * 120 + "\n\n"
                
                asim = analisis['asimetria']
                kurt = analisis['curtosis']
                
                resultado += "🔹 ASIMETRÍA (Skewness)\n"
                resultado += f"   Valor: {asim['asimetria']:.4f}\n"
                resultado += f"   Clasificación: {asim['clasificacion']}\n"
                resultado += f"   Interpretación: {asim['interpretacion']}\n"
                resultado += f"   {asim['descripcion']}\n\n"
                
                resultado += "🔹 CURTOSIS (Kurtosis)\n"
                resultado += f"   Valor: {kurt['curtosis']:.4f}\n"
                resultado += f"   Clasificación: {kurt['clasificacion']}\n"
                resultado += f"   Interpretación: {kurt['interpretacion']}\n"
                resultado += f"   {kurt['descripcion']}\n\n"
                
                resultado += "🔹 CONCLUSIÓN GENERAL\n"
                resultado += f"   {analisis['forma_general']}\n"
                
                if analisis['es_aproximadamente_normal']:
                    resultado += "   ✅ La distribución es aproximadamente normal\n"
                else:
                    resultado += "   ⚠️  La distribución NO es normal\n"
                
                ventana.mostrar_texto(resultado)
                
                # Generar gráfico
                try:
                    fig = graficar_forma(datos_edad, 
                        titulo="Análisis de Forma de la Distribución")
                    ventana.mostrar_grafico(fig)
                except Exception as e:
                    print(f"Error al generar gráfico: {e}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar datos:\n\n{str(e)}")
        
        btn_procesar = tk.Button(
            ventana.btn_frame,
            text="▶️ Procesar Datos Cargados",
            command=procesar_datos,
            bg=COLOR_SUCCESS,
            fg="#000000",
            font=FONT_BUTTON,
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        )
        btn_procesar.pack(pady=10)
    # ===== ESTADÍSTICA INFERENCIAL =====
    
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
                    
                    # ============= MOSTRAR GRÁFICOS =============
                    try:
                        # 1. Gráfico de Correlación (dispersión simple)
                        fig_corr = corr.graficar_correlacion()
                        ventana.mostrar_grafico(fig_corr)
                        
                        # 2. Gráfico de Regresión Lineal
                        fig_reg = reg_lineal.graficar()
                        plt.show()
                        
                        # 3. Gráfico COMPLETO con TODOS los modelos 
                        # (Lineal, Exponencial, Logarítmica, Potencial)
                        # Esta gráfica muestra 6 subplots:
                        # - 4 gráficos de dispersión con líneas de ajuste
                        # - 1 gráfico de barras comparando R²
                        # - 1 panel de resumen con ecuaciones
                        fig_comp = reg_no_lineal.graficar_comparacion()
                        ventana.mostrar_grafico(fig_comp)
                        
                        # Mensaje informativo
                        messagebox.showinfo(
                            "📊 Gráficos Generados Exitosamente",
                            "✅ Se han generado 3 ventanas con gráficos:\n\n"
                            "1️⃣ CORRELACIÓN\n"
                            "   → Diagrama de dispersión simple\n\n"
                            "2️⃣ REGRESIÓN LINEAL\n"
                            "   → Dispersión + línea de ajuste roja\n"
                            "   → Ecuación y = a + bx\n\n"
                            "3️⃣ COMPARACIÓN COMPLETA (6 gráficos):\n"
                            "   📊 Modelo Lineal (línea roja)\n"
                            "   📈 Modelo Exponencial (línea verde)\n"
                            "   📉 Modelo Logarítmico (línea morada)\n"
                            "   ⚡ Modelo Potencial (línea naranja)\n"
                            "   🏆 Comparación R² (barras)\n"
                            "   📋 Resumen de ecuaciones\n\n"
                            "💡 Usa las herramientas 🔍🏠💾 para:\n"
                            "   • Hacer zoom en áreas específicas\n"
                            "   • Mover y explorar el gráfico\n"
                            "   • Guardar imágenes en alta calidad"
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