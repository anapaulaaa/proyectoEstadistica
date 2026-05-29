"""
Pantalla de Login para StatPro - VERSIÓN CORREGIDA
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os
from pathlib import Path

from PIL import Image, ImageTk

# Agregar el directorio raíz al path para importar config_interfaz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_interfaz import *

class PantallaLogin:
    def __init__(self, root, callback_exito):
        """
        root: ventana principal de Tkinter
        callback_exito: función a ejecutar cuando el login sea exitoso
        """
        self.root = root
        self.callback_exito = callback_exito
        self._logo_photo = None
        
        # Configurar título de ventana
        self.root.title(f"{NOMBRE_PROYECTO} - Login")
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal con color de fondo
        self.frame_principal = tk.Frame(self.root, bg=BG_LIGHT)
        self.frame_principal.pack(fill='both', expand=True)

        self._cargar_logo_login()
        
        # ===== SECCIÓN SUPERIOR: Logo y Título =====
        frame_header = tk.Frame(self.frame_principal, bg=COLOR_PRIMARY, height=150)
        frame_header.pack(fill='x', pady=0)

        frame_header_contenido = tk.Frame(frame_header, bg=COLOR_PRIMARY)
        frame_header_contenido.pack(expand=True, pady=(16, 10))

        if self._logo_photo is not None:
            tk.Label(
                frame_header_contenido,
                image=self._logo_photo,
                bg=COLOR_PRIMARY,
            ).pack(pady=(0, 8))
        else:
            # Fallback visual si el logo no está disponible aún.
            tk.Label(
                frame_header_contenido,
                text=ICONO_ESTADISTICA,
                font=("Helvetica", 50),
                bg=COLOR_PRIMARY,
                fg=TEXT_LIGHT
            ).pack(pady=(0, 5))
        
        # Título del proyecto
        lbl_titulo = tk.Label(
            frame_header_contenido,
            text=NOMBRE_PROYECTO,
            font=("Helvetica", 18, "bold"),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT
        )
        lbl_titulo.pack(pady=(0, 6))
        
        # Subtítulo
        lbl_subtitulo = tk.Label(
            frame_header_contenido,
            text="Sistema de Análisis Estadístico",
            font=("Helvetica", 10),
            bg=COLOR_PRIMARY,
            fg=TEXT_LIGHT
        )
        lbl_subtitulo.pack(pady=(0, 4))

        # ===== SECCIÓN CENTRAL: Formulario de Login =====
        frame_login = tk.Frame(self.frame_principal, bg=BG_LIGHT)
        frame_login.pack(pady=30, padx=40, fill='both', expand=True)

        # Título del formulario
        lbl_login = tk.Label(
            frame_login,
            text="Iniciar Sesión",
            font=("Helvetica", 16, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_PRIMARY
        )
        lbl_login.pack(pady=(0, 20))

        # Campo Usuario
        lbl_usuario = tk.Label(
            frame_login,
            text="Usuario:",
            font=FONT_NORMAL,
            bg=BG_LIGHT,
            fg=TEXT_DARK
        )
        lbl_usuario.pack(anchor='w', pady=(10, 5))

        self.entry_usuario = tk.Entry(
            frame_login,
            font=FONT_NORMAL,
            width=35,
            relief='solid',
            borderwidth=1,
            fg='gray'
        )
        self.entry_usuario.pack(pady=(0, 15), ipady=8)
        self.entry_usuario.insert(0, "Ingresa tu usuario")
        self.entry_usuario.focus()

        # Placeholder behavior para usuario
        def on_entry_usuario_focus_in(event):
            if self.entry_usuario.get() == "Ingresa tu usuario":
                self.entry_usuario.delete(0, tk.END)
                self.entry_usuario.config(fg='black')

        def on_entry_usuario_focus_out(event):
            if self.entry_usuario.get() == "":
                self.entry_usuario.insert(0, "Ingresa tu usuario")
                self.entry_usuario.config(fg='gray')

        self.entry_usuario.bind("<FocusIn>", on_entry_usuario_focus_in)
        self.entry_usuario.bind("<FocusOut>", on_entry_usuario_focus_out)

        # Campo Contraseña
        lbl_password = tk.Label(
            frame_login,
            text="Contraseña:",
            font=FONT_NORMAL,
            bg=BG_LIGHT,
            fg=TEXT_DARK
        )
        lbl_password.pack(anchor='w', pady=(10, 5))

        self.entry_password = tk.Entry(
            frame_login,
            font=FONT_NORMAL,
            width=35,
            show="●",
            relief='solid',
            borderwidth=1,
            fg='gray'
        )
        self.entry_password.pack(pady=(0, 10), ipady=8)
        self.entry_password.insert(0, "●●●●●●●●")

        # Placeholder behavior para contraseña
        def on_entry_password_focus_in(event):
            if self.entry_password.get() == "●●●●●●●●":
                self.entry_password.delete(0, tk.END)
                self.entry_password.config(show="●", fg='black')

        def on_entry_password_focus_out(event):
            if self.entry_password.get() == "":
                self.entry_password.config(show="")
                self.entry_password.insert(0, "●●●●●●●●")
                self.entry_password.config(fg='gray')

        self.entry_password.bind("<FocusIn>", on_entry_password_focus_in)
        self.entry_password.bind("<FocusOut>", on_entry_password_focus_out)

        # Bind Enter key para ambos campos
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())
        self.entry_password.bind('<Return>', lambda e: self.validar_login())

        # Checkbox mostrar contraseña
        self.var_mostrar = tk.BooleanVar()
        chk_mostrar = tk.Checkbutton(
            frame_login,
            text="Mostrar contraseña",
            variable=self.var_mostrar,
            command=self.toggle_password,
            font=("Helvetica", 9),
            bg=BG_LIGHT,
            fg=TEXT_DARK,
            activebackground=BG_LIGHT,
            selectcolor=BG_LIGHT
        )
        chk_mostrar.pack(anchor='w', pady=(0, 20))

        # Botón Iniciar Sesión
        btn_login = tk.Button(
            frame_login,
            text="🔐 INICIAR SESIÓN",
            command=self.validar_login,
            bg=COLOR_PRIMARY,
            fg="#000000",
            font=FONT_BUTTON,
            width=25,
            height=2,
            relief="flat",
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        )
        btn_login.pack(pady=10)

        # Botón Invitado
        btn_invitado = tk.Button(
            frame_login,
            text="👤 Acceso como Invitado",
            command=self.login_invitado,
            bg=COLOR_INFO,
            fg="#000000",
            font=FONT_BUTTON,
            width=25,
            height=2,
            relief="flat",
            cursor="hand2",
            activebackground="#FFEB3B",
            activeforeground="#000000"
        )
        btn_invitado.pack(pady=5)

        # ===== SECCIÓN INFERIOR: Información =====
        frame_footer = tk.Frame(self.frame_principal, bg=BG_LIGHT)
        frame_footer.pack(side='bottom', fill='x', pady=20)

        # Información de usuarios
        lbl_info = tk.Label(
            frame_footer,
            text=f"{ICONO_INFO} Usuarios de prueba: admin, ana, profesor, invitado",
            font=("Helvetica", 9),
            bg=BG_LIGHT,
            fg=TEXT_MUTED
        )
        lbl_info.pack()

        # Información del autor
        lbl_autor = tk.Label(
            frame_footer,
            text=f"Desarrollado por {AUTOR} | {CARRERA}",
            font=("Helvetica", 8),
            bg=BG_LIGHT,
            fg=TEXT_MUTED
        )
        lbl_autor.pack(pady=(5, 0))

        lbl_uni = tk.Label(
            frame_footer,
            text=UNIVERSIDAD,
            font=("Helvetica", 8, "bold"),
            bg=BG_LIGHT,
            fg=COLOR_SECONDARY
        )
        lbl_uni.pack()

    def _cargar_logo_login(self):
        """Carga el logo principal del login si existe en el proyecto."""
        raiz = Path(__file__).resolve().parent.parent
        rutas_posibles = [
            raiz / "assets" / "logo.png",
            raiz / "assets" / "logo.jpg",
            raiz / "assets" / "logo.jpeg",
            raiz / "logo.png",
            raiz / "logo.jpg",
            raiz / "logo.jpeg",
        ]

        for ruta in rutas_posibles:
            if not ruta.exists():
                continue
            try:
                imagen = Image.open(ruta)
                ancho, alto = imagen.size
                nuevo_ancho = 180
                nuevo_alto = max(1, int(alto * (nuevo_ancho / ancho)))
                imagen = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                self._logo_photo = ImageTk.PhotoImage(imagen)
                return
            except Exception:
                self._logo_photo = None
                return
    
    def toggle_password(self):
        """Muestra u oculta la contraseña"""
        if self.var_mostrar.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="●")
    
    def validar_login(self):
        """Valida las credenciales del usuario"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()
        
        # Verificar placeholders
        if usuario == "Ingresa tu usuario" or usuario == "":
            messagebox.showwarning(
                "Campo vacío",
                "Por favor ingrese su usuario"
            )
            self.entry_usuario.focus()
            return
        
        if password == "●●●●●●●●" or password == "":
            messagebox.showwarning(
                "Campo vacío",
                "Por favor ingrese su contraseña"
            )
            self.entry_password.focus()
            return
        
        # Validar contra usuarios predefinidos
        if usuario in USUARIOS and USUARIOS[usuario] == password:
            messagebox.showinfo(
                "Éxito",
                f"{ICONO_EXITO} {MSG_LOGIN_EXITOSO}\n\n¡Bienvenido/a {usuario}!"
            )
            self.cerrar_y_continuar(usuario)
        else:
            messagebox.showerror(
                "Error",
                f"{ICONO_ERROR} {MSG_LOGIN_FALLIDO}\n\nVerifique sus credenciales e intente nuevamente."
            )
            # Limpiar contraseña y restaurar placeholder
            self.entry_password.delete(0, tk.END)
            self.entry_password.config(show="")
            self.entry_password.insert(0, "●●●●●●●●")
            self.entry_password.config(fg='gray')
            self.entry_usuario.focus()
    
    def login_invitado(self):
        """Acceso rápido como invitado"""
        respuesta = messagebox.askyesno(
            "Acceso Invitado",
            "¿Desea acceder como invitado?\n\nTendrá acceso completo al sistema."
        )
        if respuesta:
            self.cerrar_y_continuar("invitado")
    
    def cerrar_y_continuar(self, usuario):
        """Cierra el login y ejecuta el callback"""
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Ejecutar callback con nombre de usuario
        self.callback_exito(usuario)


# Función para probar el login independientemente
def test_login():
    def on_login_exitoso(usuario):
        print(f"✅ Login exitoso para: {usuario}")
        messagebox.showinfo("Test", f"Login exitoso!\nUsuario: {usuario}")
        root.destroy()
    
    root = tk.Tk()
    app = PantallaLogin(root, on_login_exitoso)
    root.mainloop()


if __name__ == "__main__":
    test_login()