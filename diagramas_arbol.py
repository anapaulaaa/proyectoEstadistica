import matplotlib.pyplot as plt

class DiagramaArbol:
    def __init__(self, niveles, probabilidades):
        if len(probabilidades) != niveles:
            raise ValueError("La cantidad de probabilidades debe coincidir con el número de niveles")
        self.niveles = niveles
        self.probabilidades = probabilidades

    def dibujar(self):
        fig, ax = plt.subplots(figsize=(8, 4 + self.niveles))
        ax.axis('off')

        # Función recursiva para dibujar nodos
        def dibujar_nodo(x, y, nivel, label):
            ax.text(x, y, label, ha='center', va='center', bbox=dict(facecolor='lightblue', boxstyle='round,pad=0.3'))
            if nivel < self.niveles:
                p = self.probabilidades[nivel]
                # Hijo éxito
                x_exito = x - 0.5 / (nivel + 1)
                y_hijo = y - 1
                ax.plot([x, x_exito], [y, y_hijo], 'k-')
                dibujar_nodo(x_exito, y_hijo, nivel + 1, f"E{nivel+1}\nP={p}")
                ax.text((x + x_exito)/2, (y + y_hijo)/2, f"P={p}", ha='center', va='center')

                # Hijo fracaso
                x_fracaso = x + 0.5 / (nivel + 1)
                ax.plot([x, x_fracaso], [y, y_hijo], 'k-')
                dibujar_nodo(x_fracaso, y_hijo, nivel + 1, f"F{nivel+1}\nP={1-p}")
                ax.text((x + x_fracaso)/2, (y + y_hijo)/2, f"P={1-p}", ha='center', va='center')

        dibujar_nodo(0.5, 0, 0, "Inicio")
        plt.title("Árbol de Probabilidades Simple")
        plt.tight_layout()
        return fig
