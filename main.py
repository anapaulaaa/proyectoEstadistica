"""
MAIN - StatPro
Punto de entrada principal del sistema
Integra: Login → Menú → Funcionalidades
"""
import tkinter as tk
from interfaz.pantalla_login import PantallaLogin
from interfaz.menu_principal import MenuPrincipal
from interfaz.selector_nivel import SelectorNivel
from interfaz.ventana_estadistica_ii import VentanaEstadisticaII
from config_interfaz import WINDOW_WIDTH, WINDOW_HEIGHT


class StatProMain:
    def __init__(self):
        self.root = tk.Tk()
        self.usuario_actual = None
        
        # Iniciar con pantalla de login
        self.mostrar_login()

    def _maximizar_ventana(self):
        """Intenta abrir la ventana ocupando toda la pantalla (multiplataforma)."""
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")
        try:
            self.root.state("zoomed")
        except Exception:
            try:
                self.root.attributes("-zoomed", True)
            except Exception:
                pass
    
    def mostrar_login(self):
        """Muestra la pantalla de login"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reconfigurar la ventana para el login con un tamaño más cómodo
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(680, int(screen_width * 0.92))
        window_height = min(860, int(screen_height * 0.92))
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(600, 760)
        self.root.resizable(True, True)
        
        # Crear pantalla de login
        PantallaLogin(self.root, self.on_login_exitoso)
    
    def on_login_exitoso(self, usuario):
        """Callback cuando el login es exitoso"""
        self.usuario_actual = usuario
        print(f"✅ Usuario logueado: {usuario}")
        
        # Mostrar selector de modulo
        self.mostrar_selector_nivel()

    def mostrar_selector_nivel(self):
        """Muestra el selector de Estadistica I o Estadistica II"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("1200x750")
        self.root.resizable(True, True)

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f'1200x750+{x}+{y}')

        SelectorNivel(
            self.root,
            self.usuario_actual,
            self.mostrar_menu_principal,
            self.mostrar_estadistica_ii,
            self.on_cerrar_sesion,
        )
    
    def mostrar_menu_principal(self):
        """Muestra la ventana de Estadistica I"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Reconfigurar la ventana para el menú principal
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        
        # Centrar la ventana del menú principal
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}')
        
        # Crear menú principal
        MenuPrincipal(
            self.root,
            self.usuario_actual,
            self.on_cerrar_sesion,
            self.mostrar_selector_nivel,
        )

    def mostrar_estadistica_ii(self):
        """Muestra la ventana placeholder de Estadistica II"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.resizable(True, True)
        self._maximizar_ventana()

        VentanaEstadisticaII(
            self.root,
            self.usuario_actual,
            self.mostrar_selector_nivel,
            self.on_cerrar_sesion,
        )
    
    def on_cerrar_sesion(self):
        """Callback cuando se cierra sesión"""
        print("🚪 Cerrando sesión...")
        self.usuario_actual = None
        
        # Volver al login
        self.mostrar_login()
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 Iniciando StatPro - Analizador Estadístico")
    print("=" * 60)
    
    app = StatProMain()
    app.run()


if __name__ == "__main__":
    main()