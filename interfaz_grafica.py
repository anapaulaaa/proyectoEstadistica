import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

# Importar las funciones del proyecto
from analisis_estadistico import calcular_tendencia_central, generar_dfs, generar_dfsvai
from cargar_datos import importar_csv
from exportar_resultados import exportar_resultados
from graficas import graficar_frecuencia

class AnalizadorEstadisticoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Estadístico")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.datos = None
        self.columna_seleccionada = None
        self.tendencia = None
        self.dfs = None
        self.dfsvai = None
        
        # Crear la interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Analizador Estadístico", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de control (izquierda)
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Botón cargar archivo
        ttk.Button(control_frame, text="📁 Cargar CSV", 
                  command=self.cargar_archivo, width=20).grid(row=0, column=0, pady=5)
        
        # Label para mostrar archivo cargado
        self.archivo_label = ttk.Label(control_frame, text="Ningún archivo cargado", 
                                      foreground='gray')
        self.archivo_label.grid(row=1, column=0, pady=5)
        
        # Combobox para seleccionar columna
        ttk.Label(control_frame, text="Columna a analizar:").grid(row=2, column=0, pady=(10, 5))
        self.columna_combo = ttk.Combobox(control_frame, state="disabled", width=17)
        self.columna_combo.grid(row=3, column=0, pady=5)
        self.columna_combo.bind('<<ComboboxSelected>>', self.columna_seleccionada_cambio)
        
        # Frame para número de bins
        bins_frame = ttk.Frame(control_frame)
        bins_frame.grid(row=4, column=0, pady=(10, 5))
        ttk.Label(bins_frame, text="Bins:").pack(side=tk.LEFT)
        self.bins_var = tk.StringVar(value="10")
        bins_spin = ttk.Spinbox(bins_frame, from_=5, to=50, width=5, 
                               textvariable=self.bins_var)
        bins_spin.pack(side=tk.LEFT, padx=(5, 0))
        
        # Botón analizar
        self.analizar_btn = ttk.Button(control_frame, text="📊 Analizar Datos", 
                                      command=self.analizar_datos, state="disabled")
        self.analizar_btn.grid(row=5, column=0, pady=10)
        
        # Separador
        ttk.Separator(control_frame, orient='horizontal').grid(row=6, column=0, 
                                                              sticky=(tk.W, tk.E), pady=10)
        
        # Botones de gráficas
        ttk.Label(control_frame, text="Gráficas:", font=('Arial', 10, 'bold')).grid(row=7, column=0, pady=(5, 10))
        
        self.hist_btn = ttk.Button(control_frame, text="📈 Histograma", 
                                  command=self.mostrar_histograma, state="disabled")
        self.hist_btn.grid(row=8, column=0, pady=2)
        
        self.freq_simple_btn = ttk.Button(control_frame, text="📊 Freq. Simple", 
                                         command=self.mostrar_freq_simple, state="disabled")
        self.freq_simple_btn.grid(row=9, column=0, pady=2)
        
        self.freq_agrup_btn = ttk.Button(control_frame, text="📊 Freq. Agrupada", 
                                        command=self.mostrar_freq_agrupada, state="disabled")
        self.freq_agrup_btn.grid(row=10, column=0, pady=2)
        
        # Separador
        ttk.Separator(control_frame, orient='horizontal').grid(row=11, column=0, 
                                                              sticky=(tk.W, tk.E), pady=10)
        
        # Botón exportar
        self.exportar_btn = ttk.Button(control_frame, text="💾 Exportar Resultados", 
                                      command=self.exportar_resultados, state="disabled")
        self.exportar_btn.grid(row=12, column=0, pady=10)
        
        # Notebook para pestañas (derecha)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña de resultados
        self.frame_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_resultados, text="📋 Resultados")
        
        # Pestaña de tablas
        self.frame_tablas = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_tablas, text="📊 Tablas")
        
        # Pestaña de gráficas
        self.frame_graficas = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_graficas, text="📈 Gráficas")
        
        self.crear_contenido_pestanas()
        
    def crear_contenido_pestanas(self):
        # Contenido pestaña resultados
        self.resultados_text = scrolledtext.ScrolledText(self.frame_resultados, 
                                                        width=60, height=25,
                                                        font=('Consolas', 10))
        self.resultados_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Contenido pestaña tablas
        tabla_notebook = ttk.Notebook(self.frame_tablas)
        tabla_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para tabla simple
        self.frame_tabla_simple = ttk.Frame(tabla_notebook)
        tabla_notebook.add(self.frame_tabla_simple, text="Frecuencia Simple")
        
        # Frame para tabla agrupada
        self.frame_tabla_agrupada = ttk.Frame(tabla_notebook)
        tabla_notebook.add(self.frame_tabla_agrupada, text="Frecuencia Agrupada")
        
        # Treeviews para las tablas
        self.crear_treeviews()
        
        # Contenido pestaña gráficas
        self.frame_canvas = ttk.Frame(self.frame_graficas)
        self.frame_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def crear_treeviews(self):
        # Treeview para tabla simple
        self.tree_simple = ttk.Treeview(self.frame_tabla_simple, show='headings')
        scrollbar_simple = ttk.Scrollbar(self.frame_tabla_simple, orient=tk.VERTICAL, 
                                        command=self.tree_simple.yview)
        self.tree_simple.configure(yscrollcommand=scrollbar_simple.set)
        
        self.tree_simple.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_simple.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para tabla agrupada
        self.tree_agrupada = ttk.Treeview(self.frame_tabla_agrupada, show='headings')
        scrollbar_agrupada = ttk.Scrollbar(self.frame_tabla_agrupada, orient=tk.VERTICAL, 
                                          command=self.tree_agrupada.yview)
        self.tree_agrupada.configure(yscrollcommand=scrollbar_agrupada.set)
        
        self.tree_agrupada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_agrupada.pack(side=tk.RIGHT, fill=tk.Y)
        
    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                self.datos = importar_csv(archivo)
                if self.datos is not None:
                    # Actualizar interfaz
                    nombre_archivo = archivo.split('/')[-1]
                    self.archivo_label.config(text=f"Archivo: {nombre_archivo}", 
                                            foreground='green')
                    
                    # Llenar combobox con columnas numéricas
                    columnas_numericas = self.datos.select_dtypes(include=[np.number]).columns.tolist()
                    self.columna_combo['values'] = columnas_numericas
                    self.columna_combo['state'] = 'readonly'
                    
                    if columnas_numericas:
                        self.columna_combo.current(0)
                        self.columna_seleccionada = columnas_numericas[0]
                        self.analizar_btn['state'] = 'normal'
                    
                    self.mostrar_info_archivo()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")
                
    def mostrar_info_archivo(self):
        info = f"Archivo cargado exitosamente!\n\n"
        info += f"Dimensiones: {self.datos.shape[0]} filas x {self.datos.shape[1]} columnas\n\n"
        info += f"Columnas disponibles:\n"
        for col in self.datos.columns:
            tipo = str(self.datos[col].dtype)
            info += f"  - {col} ({tipo})\n"
        
        info += f"\nPrimeras 5 filas:\n{self.datos.head().to_string()}"
        
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(1.0, info)
        
    def columna_seleccionada_cambio(self, event):
        self.columna_seleccionada = self.columna_combo.get()
        
    def analizar_datos(self):
        if self.datos is None or self.columna_seleccionada is None:
            messagebox.showwarning("Advertencia", "Debe cargar un archivo y seleccionar una columna")
            return
            
        try:
            # Obtener datos de la columna seleccionada
            datos_columna = self.datos[self.columna_seleccionada].dropna()
            bins = int(self.bins_var.get())
            
            # Calcular estadísticas
            self.tendencia = calcular_tendencia_central(datos_columna)
            self.dfs = generar_dfs(datos_columna)
            self.dfsvai = generar_dfsvai(datos_columna, bins=bins)
            
            # Mostrar resultados
            self.mostrar_resultados()
            self.mostrar_tablas()
            
            # Habilitar botones
            self.hist_btn['state'] = 'normal'
            self.freq_simple_btn['state'] = 'normal'
            self.freq_agrup_btn['state'] = 'normal'
            self.exportar_btn['state'] = 'normal'
            
            # Cambiar a pestaña de resultados
            self.notebook.select(self.frame_resultados)
            
            messagebox.showinfo("Éxito", "Análisis completado exitosamente!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar los datos:\n{str(e)}")
            
    def mostrar_resultados(self):
        resultados = f"ANÁLISIS ESTADÍSTICO\n"
        resultados += f"Columna: {self.columna_seleccionada}\n"
        resultados += f"{'='*50}\n\n"
        
        resultados += "MEDIDAS DE TENDENCIA CENTRAL:\n"
        resultados += f"{'-'*35}\n"
        for medida, valor in self.tendencia.items():
            if isinstance(valor, list):
                valor_str = ', '.join(map(str, valor))
                resultados += f"{medida}: {valor_str}\n"
            else:
                resultados += f"{medida}: {valor}\n"
        
        resultados += f"\n\nDATOS GENERALES:\n"
        resultados += f"{'-'*20}\n"
        datos_columna = self.datos[self.columna_seleccionada].dropna()
        resultados += f"Número de observaciones: {len(datos_columna)}\n"
        resultados += f"Valores únicos: {datos_columna.nunique()}\n"
        resultados += f"Valor mínimo: {datos_columna.min()}\n"
        resultados += f"Valor máximo: {datos_columna.max()}\n"
        resultados += f"Rango: {datos_columna.max() - datos_columna.min()}\n"
        resultados += f"Desviación estándar: {round(datos_columna.std(), 2)}\n"
        resultados += f"Varianza: {round(datos_columna.var(), 2)}\n"
        
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(1.0, resultados)
        
    def mostrar_tablas(self):
        # Mostrar tabla de frecuencia simple
        self.tree_simple.delete(*self.tree_simple.get_children())
        
        # Configurar columnas
        columnas_simple = list(self.dfs.columns)
        self.tree_simple['columns'] = columnas_simple
        
        for col in columnas_simple:
            self.tree_simple.heading(col, text=col)
            self.tree_simple.column(col, width=100)
            
        # Insertar datos
        for index, row in self.dfs.iterrows():
            self.tree_simple.insert('', 'end', values=list(row))
            
        # Mostrar tabla de frecuencia agrupada
        self.tree_agrupada.delete(*self.tree_agrupada.get_children())
        
        # Configurar columnas
        columnas_agrupada = list(self.dfsvai.columns)
        self.tree_agrupada['columns'] = columnas_agrupada
        
        for col in columnas_agrupada:
            self.tree_agrupada.heading(col, text=col)
            self.tree_agrupada.column(col, width=120)
            
        # Insertar datos
        for index, row in self.dfsvai.iterrows():
            valores = []
            for val in row:
                if hasattr(val, 'left') and hasattr(val, 'right'):  # Es un intervalo
                    valores.append(f"({val.left:.1f}, {val.right:.1f}]")
                else:
                    valores.append(str(val))
            self.tree_agrupada.insert('', 'end', values=valores)
            
    def limpiar_canvas(self):
        for widget in self.frame_canvas.winfo_children():
            widget.destroy()
            
    def mostrar_histograma(self):
        self.limpiar_canvas()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        datos_columna = self.datos[self.columna_seleccionada].dropna()
        bins = int(self.bins_var.get())
        
        ax.hist(datos_columna, bins=bins, edgecolor='black', alpha=0.7, color='skyblue')
        ax.set_title(f'Histograma - {self.columna_seleccionada}', fontsize=14, fontweight='bold')
        ax.set_xlabel(self.columna_seleccionada)
        ax.set_ylabel('Frecuencia')
        ax.grid(True, alpha=0.3)
        
        # Añadir estadísticas al gráfico
        media = self.tendencia['Media aritmética']
        mediana = self.tendencia['Mediana']
        ax.axvline(media, color='red', linestyle='--', alpha=0.8, label=f'Media: {media}')
        ax.axvline(mediana, color='green', linestyle='--', alpha=0.8, label=f'Mediana: {mediana}')
        ax.legend()
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.frame_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.notebook.select(self.frame_graficas)
        
    def mostrar_freq_simple(self):
        self.limpiar_canvas()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        valores = self.dfs['Valor'].astype(str)
        frecuencias = self.dfs['Frecuencia']
        
        bars = ax.bar(range(len(valores)), frecuencias, color='lightcoral', edgecolor='black')
        ax.set_title(f'Gráfico de Frecuencia Simple - {self.columna_seleccionada}', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Valores')
        ax.set_ylabel('Frecuencia')
        ax.set_xticks(range(len(valores)))
        ax.set_xticklabels(valores, rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Añadir valores sobre las barras
        for bar, freq in zip(bars, frecuencias):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{freq}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.frame_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.notebook.select(self.frame_graficas)
        
    def mostrar_freq_agrupada(self):
        try:
            self.limpiar_canvas()
            
            fig, ax = plt.subplots(figsize=(12, 6), dpi=80)
            
            # Usar las marcas de clase para el eje x
            marcas = self.dfsvai['Marca de Clase']
            frecuencias = self.dfsvai['Frecuencia']
            
            # Calcular ancho de barras basado en la diferencia entre marcas
            if len(marcas) > 1:
                ancho = marcas.diff().median() * 0.8
            else:
                ancho = 1.0
                
            bars = ax.bar(marcas, frecuencias, color='lightgreen', 
                         edgecolor='black', alpha=0.8, width=ancho)
            ax.set_title(f'Gráfico de Frecuencia Agrupada - {self.columna_seleccionada}', 
                        fontsize=14, fontweight='bold')
            ax.set_xlabel('Marca de Clase')
            ax.set_ylabel('Frecuencia')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Añadir valores sobre las barras
            for bar, freq in zip(bars, frecuencias):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(frecuencias)*0.01,
                       f'{freq}', ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            fig.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, self.frame_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Añadir barra de herramientas
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            toolbar = NavigationToolbar2Tk(canvas, self.frame_canvas)
            toolbar.update()
            
            self.notebook.select(self.frame_graficas)
            print("Gráfico de frecuencia agrupada creado exitosamente")  # Debug
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear gráfico de frecuencia agrupada:\n{str(e)}")
            print(f"Error detallado: {e}")  # Debug
        
    def exportar_resultados(self):
        if self.tendencia is None or self.dfs is None or self.dfsvai is None:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
            
        try:
            directorio = filedialog.askdirectory(title="Seleccionar directorio para exportar")
            if directorio:
                # Crear subdirectorio si no existe
                import os
                directorio_datos = os.path.join(directorio, 'datos')
                os.makedirs(directorio_datos, exist_ok=True)
                
                # Exportar usando la función existente
                exportar_resultados(self.tendencia, self.dfs, self.dfsvai)
                
                # Mover archivos al directorio seleccionado
                import shutil
                archivos = ['datos/resultados_tendencia.csv', 
                           'datos/cuadro_frecuencia_simple.csv',
                           'datos/cuadro_frecuencia_agrupada.csv']
                
                for archivo in archivos:
                    if os.path.exists(archivo):
                        nombre_archivo = os.path.basename(archivo)
                        destino = os.path.join(directorio_datos, nombre_archivo)
                        shutil.copy2(archivo, destino)
                
                messagebox.showinfo("Éxito", f"Resultados exportados en:\n{directorio_datos}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")

def main():
    root = tk.Tk()
    app = AnalizadorEstadisticoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()