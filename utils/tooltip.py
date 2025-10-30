"""
Tooltip - Mensajes emergentes para widgets de Tkinter
"""
import tkinter as tk


class Tooltip:
    """Crea tooltips (mensajes emergentes) para cualquier widget"""
    
    def __init__(self, widget, text, delay=500):
        """
        widget: El widget al que se le agregará el tooltip
        text: El texto a mostrar
        delay: Milisegundos antes de mostrar el tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.id_after = None
        
        # Bindings
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Button>", self.on_leave)
    
    def on_enter(self, event=None):
        """Cuando el mouse entra al widget"""
        self.schedule_tooltip()
    
    def on_leave(self, event=None):
        """Cuando el mouse sale del widget"""
        self.cancel_tooltip()
        self.hide_tooltip()
    
    def schedule_tooltip(self):
        """Programa mostrar el tooltip después del delay"""
        self.cancel_tooltip()
        self.id_after = self.widget.after(self.delay, self.show_tooltip)
    
    def cancel_tooltip(self):
        """Cancela mostrar el tooltip"""
        if self.id_after:
            self.widget.after_cancel(self.id_after)
            self.id_after = None
    
    def show_tooltip(self):
        """Muestra el tooltip"""
        if self.tooltip_window:
            return
        
        # Posición del widget
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Crear ventana flotante
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Sin bordes de ventana
        tw.wm_geometry(f"+{x}+{y}")
        
        # Contenido del tooltip
        label = tk.Label(
            tw,
            text=self.text,
            justify='left',
            background="#FFFFCC",
            foreground="#000000",
            relief='solid',
            borderwidth=1,
            font=("Helvetica", 9),
            padx=8,
            pady=4
        )
        label.pack()
    
    def hide_tooltip(self):
        """Oculta el tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def crear_tooltip(widget, texto):
    """Función helper para crear tooltips fácilmente"""
    return Tooltip(widget, texto)
