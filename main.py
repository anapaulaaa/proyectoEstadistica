"""
MAIN - StatPro
Punto de entrada principal del sistema
Integra: Login → Menú → Funcionalidades
"""
import tkinter as tk
from interfaz.pantalla_login import PantallaLogin
from interfaz.menu_principal import MenuPrincipal


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
        
        # Crear pantalla de login
        PantallaLogin(self.root, self.on_login_exitoso)
    
    def on_login_exitoso(self, usuario):
        """Callback cuando el login es exitoso"""
        self.usuario_actual = usuario
        print(f"✅ Usuario logueado: {usuario}")
        
        # Mostrar menú principal
        self.mostrar_menu_principal()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Crear menú principal
        MenuPrincipal(self.root, self.usuario_actual, self.on_cerrar_sesion)
    
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