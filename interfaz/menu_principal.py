"""
Menú Principal de StatPro
Panel de control con acceso a todas las funcionalidades
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_interfaz import *


class MenuPrincipal:
    def __init__(self, root, usuario, callback_cerrar_sesion):
        """
        root: ventana principal de Tkinter
        usuario: nombre del usuario logueado
        callback_cerrar_sesion: función para cerrar sesión
        """
        self.root = root
        self.usuario = usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion
        self.datos = None  # Para almacenar datos cargados
        
        # Configurar ventana
        self.root.title(f"{NOMBRE_PROYECTO} - Menú Principal")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_LIGHT)
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz del menú principal"""
        
        # ===== BARRA SUPERIOR =====
        self.crear_barra_superior()
        
        # ===== CONTENEDOR PRINCIPAL =====
        self.frame_principal = tk.Frame(self.root, bg=BG_LIGHT)
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ===== TÍTULO DE BIENVENIDA =====
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
        
        # ===== SECCIÓN DE MÓDULOS =====
        # Frame para las dos columnas
        frame_modulos = tk.Frame(self.frame_principal, bg=BG_LIGHT)
        frame_modulos.pack(fill='both', expand=True)
        
        # Columna 1: Estadística Descriptiva
        self.crear_seccion_descriptiva(frame_modulos)
        
        # Columna 2: Estadística Inferencial
        self.crear_seccion_inferencial(frame_modulos)
    
    def crear_barra_superior(self):
        """Crea la barra superior con logo y opciones"""
        barra = tk.Frame(self.root, bg=COLOR_PRIMARY, height=80)
        barra.pack(fill='x', side='top')
        
        # Frame interno para contenido
        barra_content = tk.Frame(barra, bg=COLOR_PRIMARY)
        barra_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Logo y título (izquierda)
        frame_logo = tk.Frame(barra_content, bg=COLOR_PRIMARY)
        frame_logo.pack(side='left')
        
        tk.Label(
            frame_logo,
            text=f"{ICONO_ESTADISTICA} {NOMBRE_PROYECTO}",
            font=("Helvetica", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT
        ).pack(side='left')
        
        # Botón cargar datos (centro-derecha)
        tk.Button(
            barra_content,
            text=f"{ICONO_ARCHIVO} Cargar Datos CSV",
            command=self.cargar_archivo,
            bg=COLOR_SUCCESS,
            fg=TEXT_LIGHT,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        ).pack(side='left', padx=20)
        
        # Información usuario y cerrar sesión (derecha)
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
    
    def cargar_archivo(self):
        """Carga un archivo CSV"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            try:
                from utils.cargar_datos import importar_csv
                self.datos = importar_csv(ruta)
                
                if self.datos is not None:
                    messagebox.showinfo(
                        "Éxito",
                        f"{ICONO_EXITO} Archivo cargado correctamente\n\n"
                        f"Filas: {len(self.datos)}\n"
                        f"Columnas: {len(self.datos.columns)}\n"
                        f"Columnas: {', '.join(self.datos.columns)}"
                    )
                else:
                    messagebox.showerror("Error", "No se pudo cargar el archivo")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo:\n{str(e)}")
    
    def crear_seccion_descriptiva(self, parent):
        """Crea la sección de Estadística Descriptiva"""
        # Frame contenedor
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
        
        # Botones de funcionalidades
        botones = [
            ("📊 Cuadros y Gráficos Estadísticos", COLOR_PRIMARY, self.abrir_cuadros),
            ("📈 Medidas de Tendencia Central", COLOR_SECONDARY, self.abrir_tendencia),
            ("📍 Medidas de Posición", COLOR_INFO, self.abrir_posicion),
            ("📏 Medidas de Dispersión", COLOR_WARNING, self.abrir_dispersion),
            ("📉 Medidas de Forma", COLOR_SUCCESS, self.abrir_forma),
        ]
        
        for texto, color, comando in botones:
            btn = tk.Button(
                frame,
                text=texto,
                command=comando,
                bg=color,
                fg=TEXT_LIGHT,
                font=FONT_BUTTON,
                width=35,
                height=2,
                relief="flat",
                cursor="hand2",
                anchor='w',
                padx=15
            )
            btn.pack(fill='x', pady=8)
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief="raised"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief="flat"))
    
    def crear_seccion_inferencial(self, parent):
        """Crea la sección de Estadística Inferencial"""
        # Frame contenedor
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
        
        # Botones de funcionalidades
        botones = [
            ("🎲 Cálculo de Probabilidades", COLOR_PRIMARY, self.abrir_probabilidades),
            ("🔄 Teorema de Bayes", COLOR_SECONDARY, self.abrir_bayes),
            ("📊 Distribuciones (Normal, Binomial, Poisson)", COLOR_INFO, self.abrir_distribuciones),
            ("📈 Correlación y Regresión Simple", COLOR_WARNING, self.abrir_regresion),
            ("📉 Regresión Lineal Múltiple", COLOR_SUCCESS, self.abrir_regresion_multiple),
            ("🌳 Árboles de Decisión", COLOR_DANGER, self.abrir_arboles),
        ]
        
        for texto, color, comando in botones:
            btn = tk.Button(
                frame,
                text=texto,
                command=comando,
                bg=color,
                fg=TEXT_LIGHT,
                font=FONT_BUTTON,
                width=35,
                height=2,
                relief="flat",
                cursor="hand2",
                anchor='w',
                padx=15
            )
            btn.pack(fill='x', pady=8)
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief="raised"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief="flat"))
    
    def verificar_datos_cargados(self):
        """Verifica si hay datos cargados"""
        if self.datos is None:
            respuesta = messagebox.askyesno(
                "Sin datos",
                "No hay datos cargados.\n\n¿Desea cargar un archivo CSV ahora?"
            )
            if respuesta:
                self.cargar_archivo()
            return False
        return True
    
    # ===== CALLBACKS DE BOTONES - ESTADÍSTICA DESCRIPTIVA =====
    def abrir_cuadros(self):
        """Abre ventana de cuadros y gráficos"""
        if not self.verificar_datos_cargados():
            return
        
        from ventanas.ventana_cuadros import VentanaCuadros
        VentanaCuadros(self.root, self.datos)
    
    def abrir_tendencia(self):
        """Abre ventana de medidas de tendencia central"""
        if not self.verificar_datos_cargados():
            return
        
        from ventanas.ventana_tendencia import VentanaTendencia
        VentanaTendencia(self.root, self.datos)
    
    def abrir_posicion(self):
        """Abre ventana de medidas de posición"""
        if not self.verificar_datos_cargados():
            return
        
        from ventanas.ventana_posicion import VentanaPosicion
        VentanaPosicion(self.root, self.datos)
    
    def abrir_dispersion(self):
        """Abre ventana de medidas de dispersión"""
        if not self.verificar_datos_cargados():
            return
        
        from ventanas.ventana_dispersion import VentanaDispersion
        VentanaDispersion(self.root, self.datos)
    
    def abrir_forma(self):
        """Abre ventana de medidas de forma"""
        if not self.verificar_datos_cargados():
            return
        
        from ventanas.ventana_forma import VentanaForma
        VentanaForma(self.root, self.datos)
    
    # ===== CALLBACKS DE BOTONES - ESTADÍSTICA INFERENCIAL =====
    def abrir_probabilidades(self):
        """Abre ventana de probabilidades"""
        from ventanas.ventana_probabilidades import VentanaProbabilidades
        VentanaProbabilidades(self.root)
    
    def abrir_bayes(self):
        """Abre ventana de Teorema de Bayes"""
        from ventanas.ventana_bayes import VentanaBayes
        VentanaBayes(self.root)
    
    def abrir_distribuciones(self):
        """Abre ventana de distribuciones"""
        from ventanas.ventana_distribuciones import VentanaDistribuciones
        VentanaDistribuciones(self.root)
    
    def abrir_regresion(self):
        """Abre ventana de regresión simple"""
        if not self.verificar_datos_cargados():
            return
        
        from ventanas.ventana_regresion import VentanaRegresion
        VentanaRegresion(self.root, self.datos)
    
    def abrir_regresion_multiple(self):
        """Abre ventana de regresión múltiple"""
        if not self.verificar_datos_cargados():
            return
        
        from ventanas.ventana_regresion_multiple import VentanaRegresionMultiple
        VentanaRegresionMultiple(self.root, self.datos)
    
    def abrir_arboles(self):
        """Abre ventana de árboles de decisión"""
        from ventanas.ventana_arboles import VentanaArboles
        VentanaArboles(self.root)
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro que desea cerrar sesión?"
        )
        if respuesta:
            # Limpiar ventana
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Ejecutar callback
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