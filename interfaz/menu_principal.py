"""
Menu Principal de StatPro - VERSION COMPLETA
Todas las funcionalidades implementadas
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_interfaz import *
from estadistica_descriptiva.analisis_estadistico import calcular_tendencia_central, generar_dfs, generar_dfsvai
from estadistica_descriptiva.medidas_posicion import generar_tabla_posicion, crear_boxplot
from estadistica_descriptiva.medidas_dispersión import generar_tabla_dispersion, graficar_dispersion
from estadistica_descriptiva.medidas_forma import analisis_completo_forma, generar_tabla_forma, graficar_forma
from estadistica_descriptiva.graficas import graficar_frecuencia
from utils.tooltip import crear_tooltip
from interfaz.componentes_analisis import VentanaAnalisis, crear_panel_instrucciones
from interfaz.menu_inferencial_mixin import MenuInferencialMixin

class MenuPrincipal(MenuInferencialMixin):
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
                    if isinstance(valor, (int, float)):
                        resultado += f"{medida:<30} {valor:<15.2f} {desc}\n"
                    else:
                        resultado += f"{medida:<30} {str(valor):<15} {desc}\n"
                
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
