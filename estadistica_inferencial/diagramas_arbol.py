import matplotlib.pyplot as plt

class DiagramaArbol:
    def __init__(self, niveles, probabilidades):
        if len(probabilidades) != niveles:
            raise ValueError("La cantidad de probabilidades debe coincidir con el número de niveles")
        self.niveles = niveles
        self.probabilidades = probabilidades

    def dibujar(self):
        fig, ax = plt.subplots(figsize=(10, 4 + self.niveles))
        ax.axis("off")

        # Calcular posiciones recursivamente
        def construir(x, y, nivel, label):
            ax.text(x, y, label,
                    ha='center', va='center',
                    bbox=dict(facecolor='lightblue', boxstyle='round,pad=0.3'))

            if nivel < self.niveles:
                p = self.probabilidades[nivel]
                # Espaciado horizontal depende del nivel
                dx = 0.5 / (2**nivel)
                y_hijo = y - 1

                # Éxito
                x_e = x - dx
                ax.plot([x, x_e], [y, y_hijo], 'k-')
                ax.text((x + x_e)/2, (y + y_hijo)/2, f"P={p:.2f}", fontsize=8, color="green")
                construir(x_e, y_hijo, nivel + 1, f"E{nivel+1}")

                # Fracaso
                x_f = x + dx
                ax.plot([x, x_f], [y, y_hijo], 'k-')
                ax.text((x + x_f)/2, (y + y_hijo)/2, f"P={1-p:.2f}", fontsize=8, color="red")
                construir(x_f, y_hijo, nivel + 1, f"F{nivel+1}")

        construir(0.5, 0, 0, "Inicio")
        plt.title("Árbol de Probabilidades")
        plt.tight_layout()
        return fig


# Ejemplo de uso
if __name__ == "__main__":
    arbol = DiagramaArbol(3, [0.6, 0.7, 0.5])
    arbol.dibujar()
    plt.show()

