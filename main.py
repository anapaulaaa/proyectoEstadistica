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
    
    def mostrar_login(self):
        """Muestra la pantalla de login"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Reconfigurar la ventana para el login
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Centrar la ventana del login
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f'500x650+{x}+{y}')
        
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
        MenuPrincipal(self.root, self.usuario_actual, self.on_cerrar_sesion)

    def mostrar_estadistica_ii(self):
        """Muestra la ventana placeholder de Estadistica II"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("1200x750")
        self.root.resizable(True, True)

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f'1200x750+{x}+{y}')

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