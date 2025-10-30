import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog as sd
import pandas as pd
from utils.cargar_datos import importar_csv
from estadistica_descriptiva.analisis_estadistico import calcular_tendencia_central, generar_dfs, generar_dfsvai
from estadistica_descriptiva.graficas import graficar_tendencia, graficar_frecuencia
from utils.exportar_resultados import exportar_resultados
from estadistica_inferencial.probabilidades import ProbabilidadesElementales
import matplotlib.pyplot as plt
from math import comb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from estadistica_inferencial.diagramas_arbol import DiagramaArbol  # Tu clase del árbol de probabilidades

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Estadístico")
        self.root.geometry("1200x900")

        self.prob = ProbabilidadesElementales()

        # Notebook principal
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill='both')

        # Inicializar pestañas
        self.init_estad_tab()
        self.init_prob_tab()

    # ------------------ PESTAÑA ESTADÍSTICA ------------------ #
    def init_estad_tab(self):
        self.tab_estad = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_estad, text='Estadística')

        lbl_title = tk.Label(self.tab_estad, text="Análisis Estadístico", font=("Arial", 16))
        lbl_title.pack(pady=10)

        btn_cargar = tk.Button(self.tab_estad, text="Cargar archivo CSV", command=self.cargar_archivo, 
                              bg="#27AE60", fg="#000000", font=("Helvetica", 10, "bold"), 
                              activebackground="#FFEB3B", activeforeground="#000000")
        btn_cargar.pack(pady=5)

        # Área de resultados
        lbl_resultados = tk.Label(self.tab_estad, text="Resultados", font=("Arial", 14))
        lbl_resultados.pack(pady=10)

        self.text_resultados = tk.Text(self.tab_estad, height=25, width=130)
        self.text_resultados.pack(padx=10, pady=5)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if ruta:
            self.datos = importar_csv(ruta)
            if self.datos is not None:
                messagebox.showinfo("Éxito", f"Archivo '{ruta}' cargado correctamente")
                self.mostrar_estadisticas()
            else:
                messagebox.showerror("Error", "No se pudo cargar el archivo CSV")

    def mostrar_estadisticas(self):
        if hasattr(self, 'datos') and 'Edad' in self.datos.columns:
            tendencia = calcular_tendencia_central(self.datos['Edad'])
            dfs = generar_dfs(self.datos['Edad'])
            dfsvai = generar_dfsvai(self.datos['Edad'])

            # Mostrar resultados en Text
            self.text_resultados.delete("1.0", tk.END)
            self.text_resultados.insert(tk.END, "=== Medidas de Tendencia Central ===\n")
            self.text_resultados.insert(tk.END, f"{tendencia}\n\n")
            self.text_resultados.insert(tk.END, "=== Cuadro de Frecuencia Simple ===\n")
            self.text_resultados.insert(tk.END, f"{dfs}\n\n")
            self.text_resultados.insert(tk.END, "=== Cuadro de Frecuencia Agrupada con Intervalos ===\n")
            self.text_resultados.insert(tk.END, f"{dfsvai}\n\n")

            # Graficar
            graficar_tendencia(self.datos['Edad'])
            graficar_frecuencia(dfs, 'simple')
            graficar_frecuencia(dfsvai, 'agrupada')

            # Exportar resultados
            exportar_resultados(tendencia, dfs, dfsvai)
        else:
            messagebox.showwarning("Advertencia", "La columna 'Edad' no está presente en los datos")

    # ------------------ PESTAÑA PROBABILIDAD ------------------ #
    def init_prob_tab(self):
        self.tab_prob = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_prob, text='Probabilidad')

        lbl_title = tk.Label(self.tab_prob, text="Análisis de Probabilidad", font=("Arial", 16))
        lbl_title.pack(pady=10)

        # Entrada de espacio muestral
        frame_espacio = tk.LabelFrame(self.tab_prob, text="Espacio Muestral", padx=10, pady=10)
        frame_espacio.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_espacio, text="Elementos separados por coma:").grid(row=0, column=0, sticky="w")
        self.entry_espacio = tk.Entry(frame_espacio, width=80)
        self.entry_espacio.grid(row=0, column=1, padx=5)

        btn_def_espacio = tk.Button(frame_espacio, text="Definir Espacio Muestral", command=self.definir_espacio,
                                   bg="#27AE60", fg="#000000", font=("Helvetica", 10, "bold"),
                                   activebackground="#FFEB3B", activeforeground="#000000")
        btn_def_espacio.grid(row=0, column=2, padx=5)

        # Entrada de eventos
        frame_eventos = tk.LabelFrame(self.tab_prob, text="Eventos", padx=10, pady=10)
        frame_eventos.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_eventos, text="Nombre del evento:").grid(row=0, column=0)
        self.entry_nombre_evento = tk.Entry(frame_eventos, width=20)
        self.entry_nombre_evento.grid(row=0, column=1, padx=5)

        tk.Label(frame_eventos, text="Elementos separados por coma:").grid(row=0, column=2)
        self.entry_elementos_evento = tk.Entry(frame_eventos, width=50)
        self.entry_elementos_evento.grid(row=0, column=3, padx=5)

        btn_def_evento = tk.Button(frame_eventos, text="Definir Evento", command=self.definir_evento,
                                  bg="#16A085", fg="#000000", font=("Helvetica", 10, "bold"),
                                  activebackground="#FFEB3B", activeforeground="#000000")
        btn_def_evento.grid(row=0, column=4, padx=5)

        # Área de resultados de probabilidad
        lbl_resultados = tk.Label(self.tab_prob, text="Resultados", font=("Arial", 14))
        lbl_resultados.pack(pady=10)

        self.text_prob = tk.Text(self.tab_prob, height=15, width=130)
        self.text_prob.pack(padx=10, pady=5)

        # Frame para mostrar gráfico del árbol
        self.frame_arbol = tk.Frame(self.tab_prob)
        self.frame_arbol.pack(padx=10, pady=10, fill="both", expand=True)

        # Botones de operaciones
        frame_ops = tk.Frame(self.tab_prob)
        frame_ops.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_ops, text="Evento A:").grid(row=0, column=0)
        self.entry_a = tk.Entry(frame_ops, width=20)
        self.entry_a.grid(row=0, column=1, padx=5)

        tk.Label(frame_ops, text="Evento B:").grid(row=0, column=2)
        self.entry_b = tk.Entry(frame_ops, width=20)
        self.entry_b.grid(row=0, column=3, padx=5)

        # BOTONES ORIGINALES
        botones = [
            ("Probabilidad Simple A", self.prob_simple),
            ("Probabilidad Unión", self.prob_union),
            ("Probabilidad Intersección", self.prob_interseccion),
            ("Complemento A", self.prob_complemento),
            ("P(A|B)", self.prob_condicional),
            ("Ver Independencia", self.ver_independencia),
            ("Resumen Eventos", self.resumen_eventos),
        ]
        for i, (text, cmd) in enumerate(botones):
            tk.Button(frame_ops, text=text, width=20, command=cmd,
                     bg="#3498DB", fg="#000000", font=("Helvetica", 9, "bold"),
                     activebackground="#FFEB3B", activeforeground="#000000").grid(row=1, column=i, padx=5, pady=3)

        # BOTONES NUEVOS: Distribución, Bayes, Árbol
        botones_nuevos = [
            ("Distribución Bernoulli", self.calcular_bernoulli),
            ("Distribución Binomial", self.calcular_binomial),
            ("Teorema de Bayes", self.calcular_bayes),
            ("Árbol de Probabilidades", self.generar_arbol)
        ]
        for i, (text, cmd) in enumerate(botones_nuevos):
            tk.Button(frame_ops, text=text, width=20, command=cmd,
                     bg="#E74C3C", fg="#000000", font=("Helvetica", 9, "bold"),
                     activebackground="#FFEB3B", activeforeground="#000000").grid(row=2, column=i, padx=5, pady=3)

    # ------------------ FUNCIONES PROBABILIDAD ------------------ #
    def definir_espacio(self):
        datos = self.entry_espacio.get()
        if datos:
            elementos = [x.strip() for x in datos.split(',')]
            self.prob.definir_espacio_muestral(elementos)
            self.text_prob.insert(tk.END, f"Espacio muestral definido: {elementos}\n")
        else:
            messagebox.showwarning("Advertencia", "Ingrese elementos para el espacio muestral")

    def definir_evento(self):
        nombre = self.entry_nombre_evento.get()
        elementos = [x.strip() for x in self.entry_elementos_evento.get().split(',')]
        if nombre and elementos:
            try:
                self.prob.definir_evento(nombre, elementos)
                self.text_prob.insert(tk.END, f"Evento '{nombre}' definido con elementos: {elementos}\n")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Complete nombre y elementos del evento")

    def prob_simple(self):
        a = self.entry_a.get()
        if a:
            try:
                resultado = self.prob.probabilidad_simple(a)
                self.text_prob.insert(tk.END, f"Probabilidad simple de '{a}': {resultado}\n")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def prob_union(self):
        a, b = self.entry_a.get(), self.entry_b.get()
        if a and b:
            try:
                if self.prob.eventos_excluyentes(a, b):
                    res = self.prob.probabilidad_union_excluyentes(a, b)
                else:
                    res = self.prob.probabilidad_union_no_excluyentes(a, b)
                self.text_prob.insert(tk.END, f"Probabilidad unión de '{a}' y '{b}': {res}\n")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def prob_interseccion(self):
        a, b = self.entry_a.get(), self.entry_b.get()
        if a and b:
            try:
                res = self.prob.interseccion_eventos(a, b)
                self.text_prob.insert(tk.END, f"Intersección de '{a}' y '{b}': {res}\n")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def prob_complemento(self):
        a = self.entry_a.get()
        if a:
            try:
                res = self.prob.probabilidad_complemento(a)
                self.text_prob.insert(tk.END, f"Complemento de '{a}': {res}\n")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def prob_condicional(self):
        a, b = self.entry_a.get(), self.entry_b.get()
        if a and b:
            try:
                res = self.prob.probabilidad_condicional(a, b)
                self.text_prob.insert(tk.END, f"Probabilidad condicional P({a}|{b}): {res}\n")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def ver_independencia(self):
        a, b = self.entry_a.get(), self.entry_b.get()
        if a and b:
            try:
                res = self.prob.eventos_independientes(a, b)
                self.text_prob.insert(tk.END, f"Independencia de '{a}' y '{b}': {res}\n")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def resumen_eventos(self):
        res = self.prob.resumen_eventos()
        self.text_prob.insert(tk.END, f"Resumen de eventos:\n{res}\n")

    # ------------------ FUNCIONES NUEVAS ------------------ #
    def calcular_bernoulli(self):
        p = sd.askfloat("Bernoulli", "Probabilidad de éxito (p):")
        if p is not None:
            q = 1 - p
            self.text_prob.insert(tk.END, f"Distribución Bernoulli (p={p}):\nÉxito: {p}\nFracaso: {q}\n\n")

    def calcular_binomial(self):
        n = sd.askinteger("Binomial", "Número de ensayos (n):")
        p = sd.askfloat("Binomial", "Probabilidad de éxito (p):")
        k = sd.askinteger("Binomial", "Número de éxitos (k):")
        if None not in (n, p, k):
            prob = comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
            self.text_prob.insert(tk.END, f"Distribución Binomial P(X={k})={prob}\n\n")

    def calcular_bayes(self):
        try:
            P_A = float(sd.askstring("Bayes", "P(A)"))
            P_B = float(sd.askstring("Bayes", "P(B)"))
            P_B_A = float(sd.askstring("Bayes", "P(B|A)"))
            P_B_notA = float(sd.askstring("Bayes", "P(B|¬A)"))
            P_A_B = (P_B_A * P_A) / ((P_B_A * P_A) + (P_B_notA * (1 - P_A)))
            self.text_prob.insert(tk.END, f"Teorema de Bayes: P(A|B)={P_A_B}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    # ------------------ FUNCION GENERAR ARBOL ------------------ #
    def generar_arbol(self):
        try:
            niveles = sd.askinteger("Árbol", "Número de niveles")
            if niveles is None or niveles <= 0:
                raise ValueError("Número de niveles debe ser positivo")

            probabilidades = []
            for i in range(niveles):
                p = sd.askfloat("Árbol", f"Probabilidad de éxito en nivel {i+1} (0-1)")
                if p is None or not (0 <= p <= 1):
                    raise ValueError("Probabilidades deben estar entre 0 y 1")
                probabilidades.append(p)

            # Limpiar frame
            for widget in self.frame_arbol.winfo_children():
                widget.destroy()

            # Crear y dibujar árbol
            arbol = DiagramaArbol(niveles, probabilidades)
            fig = arbol.dibujar()
            canvas = FigureCanvasTkAgg(fig, master=self.frame_arbol)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

# ------------------ MAIN ------------------ #
def main():
    print("Iniciando Analizador Estadístico - Interfaz Gráfica...")
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
