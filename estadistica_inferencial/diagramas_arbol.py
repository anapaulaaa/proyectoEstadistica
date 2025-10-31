import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.backend_bases import MouseButton
import tkinter as tk
from tkinter import simpledialog, messagebox

class DiagramaArbol:
    def __init__(self, niveles, probabilidades):
        if len(probabilidades) != niveles:
            raise ValueError("La cantidad de probabilidades debe coincidir con el número de niveles")
        self.niveles = niveles
        self.probabilidades = probabilidades
        self.nodos_info = {}  # Almacenar información de nodos (posición, nivel, tipo)
        self.textos = {}      # Almacenar objetos de texto para actualizar
        self.prob_textos = {} # Almacenar textos de probabilidades

    def dibujar(self, interactivo=True):
        """
        Dibuja el árbol de probabilidades
        
        Args:
            interactivo (bool): Si es True, permite editar nodos al hacer clic
        """
        fig, ax = plt.subplots(figsize=(12, 4 + self.niveles * 1.2))
        ax.axis("off")
        
        self.fig = fig
        self.ax = ax
        self.nodos_info = {}
        self.textos = {}
        self.prob_textos = {}

        # Calcular posiciones recursivamente
        def construir(x, y, nivel, label, prob_padre=None, tipo=None):
            # Crear el nodo
            nodo_id = f"{x}_{y}_{nivel}"
            
            # Dibujar el nodo con estilo mejorado
            if nivel == 0:
                color = '#4CAF50'  # Verde para inicio
            elif 'E' in label:
                color = '#2196F3'  # Azul para éxito
            else:
                color = '#FF5722'  # Rojo/naranja para fracaso
            
            texto = ax.text(x, y, label,
                    ha='center', va='center',
                    bbox=dict(facecolor=color, boxstyle='round,pad=0.5', 
                             edgecolor='black', linewidth=1.5, alpha=0.8),
                    fontsize=10, fontweight='bold', color='white',
                    picker=5)  # Hacer el texto clickeable
            
            # Guardar información del nodo
            self.nodos_info[nodo_id] = {
                'x': x, 'y': y, 'nivel': nivel, 'label': label, 
                'tipo': tipo, 'texto': texto
            }
            self.textos[nodo_id] = texto

            if nivel < self.niveles:
                p = self.probabilidades[nivel]
                # Espaciado horizontal depende del nivel
                dx = 0.6 / (2**nivel)
                y_hijo = y - 1.2

                # Éxito (izquierda)
                x_e = x - dx
                ax.plot([x, x_e], [y, y_hijo], 'k-', linewidth=2, alpha=0.6)
                prob_text_e = ax.text((x + x_e)/2 - 0.05, (y + y_hijo)/2, 
                                     f"P={p:.3f}", 
                                     fontsize=9, color="green", fontweight='bold',
                                     bbox=dict(facecolor='white', alpha=0.7, 
                                             boxstyle='round,pad=0.3'))
                self.prob_textos[f"{nivel}_e"] = {'texto': prob_text_e, 'nivel': nivel}
                construir(x_e, y_hijo, nivel + 1, f"E{nivel+1}", p, 'exito')

                # Fracaso (derecha)
                x_f = x + dx
                ax.plot([x, x_f], [y, y_hijo], 'k-', linewidth=2, alpha=0.6)
                prob_text_f = ax.text((x + x_f)/2 + 0.05, (y + y_hijo)/2, 
                                     f"P={1-p:.3f}", 
                                     fontsize=9, color="red", fontweight='bold',
                                     bbox=dict(facecolor='white', alpha=0.7, 
                                             boxstyle='round,pad=0.3'))
                self.prob_textos[f"{nivel}_f"] = {'texto': prob_text_f, 'nivel': nivel}
                construir(x_f, y_hijo, nivel + 1, f"F{nivel+1}", 1-p, 'fracaso')

        construir(0.5, 0, 0, "Inicio")
        
        plt.title("🌳 Árbol de Probabilidades Interactivo\n(Click en los nodos para editar probabilidades)", 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Agregar instrucciones
        instrucciones = ("💡 Instrucciones:\n"
                        "• Click en cualquier nodo para ver opciones\n"
                        "• Edita las probabilidades de cada nivel\n"
                        "• Los cambios se actualizan automáticamente")
        ax.text(0.02, 0.98, instrucciones, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Conectar evento de click si es interactivo
        if interactivo:
            fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        plt.tight_layout()
        return fig
    
    def on_click(self, event):
        """Maneja el evento de click en el gráfico"""
        if event.inaxes != self.ax:
            return
        
        # Verificar si se hizo click en un nodo
        for nodo_id, info in self.nodos_info.items():
            texto = info['texto']
            contains, _ = texto.contains(event)
            
            if contains:
                self.mostrar_menu_nodo(info)
                break
    
    def mostrar_menu_nodo(self, info):
        """Muestra un menú para editar el nodo"""
        nivel = info['nivel']
        label = info['label']
        
        # Crear ventana de diálogo
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        if nivel >= self.niveles:
            messagebox.showinfo(
                "Nodo Hoja",
                f"Este es un nodo final: {label}\n\n"
                f"No tiene probabilidades asociadas.\n"
                f"Representa un resultado del árbol."
            )
            root.destroy()
            return
        
        # Mostrar opciones
        prob_actual = self.probabilidades[nivel]
        
        respuesta = messagebox.askyesno(
            f"Editar Probabilidad - Nivel {nivel + 1}",
            f"Nodo: {label}\n"
            f"Nivel: {nivel + 1}\n"
            f"Probabilidad actual de ÉXITO: {prob_actual:.3f}\n"
            f"Probabilidad actual de FRACASO: {1-prob_actual:.3f}\n\n"
            f"¿Desea cambiar esta probabilidad?"
        )
        
        if respuesta:
            # Pedir nueva probabilidad
            nueva_prob = simpledialog.askfloat(
                "Nueva Probabilidad",
                f"Ingrese la nueva probabilidad de ÉXITO para el nivel {nivel + 1}:\n"
                f"(Debe estar entre 0 y 1)\n\n"
                f"Probabilidad actual: {prob_actual:.3f}",
                minvalue=0.0,
                maxvalue=1.0,
                initialvalue=prob_actual
            )
            
            if nueva_prob is not None:
                # Actualizar la probabilidad
                self.probabilidades[nivel] = nueva_prob
                
                # Redibujar el árbol
                self.actualizar_arbol()
                
                messagebox.showinfo(
                    "✅ Actualizado",
                    f"Probabilidad del nivel {nivel + 1} actualizada:\n\n"
                    f"Éxito: {nueva_prob:.3f}\n"
                    f"Fracaso: {1-nueva_prob:.3f}\n\n"
                    f"El árbol se ha actualizado."
                )
        
        root.destroy()
    
    def actualizar_arbol(self):
        """Actualiza el árbol con las nuevas probabilidades"""
        # Limpiar el gráfico actual
        self.ax.clear()
        self.ax.axis("off")
        
        # Redibujar
        self.nodos_info = {}
        self.textos = {}
        self.prob_textos = {}
        
        # Reconstruir el árbol
        def construir(x, y, nivel, label, prob_padre=None, tipo=None):
            nodo_id = f"{x}_{y}_{nivel}"
            
            if nivel == 0:
                color = '#4CAF50'
            elif 'E' in label:
                color = '#2196F3'
            else:
                color = '#FF5722'
            
            texto = self.ax.text(x, y, label,
                    ha='center', va='center',
                    bbox=dict(facecolor=color, boxstyle='round,pad=0.5', 
                             edgecolor='black', linewidth=1.5, alpha=0.8),
                    fontsize=10, fontweight='bold', color='white',
                    picker=5)
            
            self.nodos_info[nodo_id] = {
                'x': x, 'y': y, 'nivel': nivel, 'label': label, 
                'tipo': tipo, 'texto': texto
            }
            self.textos[nodo_id] = texto

            if nivel < self.niveles:
                p = self.probabilidades[nivel]
                dx = 0.6 / (2**nivel)
                y_hijo = y - 1.2

                # Éxito
                x_e = x - dx
                self.ax.plot([x, x_e], [y, y_hijo], 'k-', linewidth=2, alpha=0.6)
                prob_text_e = self.ax.text((x + x_e)/2 - 0.05, (y + y_hijo)/2, 
                                     f"P={p:.3f}", 
                                     fontsize=9, color="green", fontweight='bold',
                                     bbox=dict(facecolor='white', alpha=0.7, 
                                             boxstyle='round,pad=0.3'))
                self.prob_textos[f"{nivel}_e"] = {'texto': prob_text_e, 'nivel': nivel}
                construir(x_e, y_hijo, nivel + 1, f"E{nivel+1}", p, 'exito')

                # Fracaso
                x_f = x + dx
                self.ax.plot([x, x_f], [y, y_hijo], 'k-', linewidth=2, alpha=0.6)
                prob_text_f = self.ax.text((x + x_f)/2 + 0.05, (y + y_hijo)/2, 
                                     f"P={1-p:.3f}", 
                                     fontsize=9, color="red", fontweight='bold',
                                     bbox=dict(facecolor='white', alpha=0.7, 
                                             boxstyle='round,pad=0.3'))
                self.prob_textos[f"{nivel}_f"] = {'texto': prob_text_f, 'nivel': nivel}
                construir(x_f, y_hijo, nivel + 1, f"F{nivel+1}", 1-p, 'fracaso')

        construir(0.5, 0, 0, "Inicio")
        
        self.ax.set_title("🌳 Árbol de Probabilidades Interactivo\n(Click en los nodos para editar probabilidades)", 
                 fontsize=14, fontweight='bold', pad=20)
        
        instrucciones = ("💡 Instrucciones:\n"
                        "• Click en cualquier nodo para ver opciones\n"
                        "• Edita las probabilidades de cada nivel\n"
                        "• Los cambios se actualizan automáticamente")
        self.ax.text(0.02, 0.98, instrucciones, transform=self.ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Redibujar el canvas
        self.fig.canvas.draw()


# Ejemplo de uso
if __name__ == "__main__":
    arbol = DiagramaArbol(3, [0.6, 0.7, 0.5])
    arbol.dibujar(interactivo=True)
    plt.show()


