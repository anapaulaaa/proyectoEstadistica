"""Componentes reutilizables para ventanas de analisis."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config_interfaz import *
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
        
        # Exponer este frame para que otras vistas agreguen instrucciones custom.
        self.main_frame = scrollable_frame
        main_frame = self.main_frame
        
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

