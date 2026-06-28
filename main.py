# BS-Kine - Gestión de Pacientes
# Creado por: Braian Nicolas Videla (2026)
# Distribuido bajo la Licencia MIT.

import wx 
import base_datos # Importa la base de datos
from interfaz import FramePrincipal # Trae unicamente la ventana principal desde el archivo interfaz.py

class BSKineApp(wx.App): # Crea una clase que representa toda la aplicacion
    def OnInit(self): # Este es un metodo propio de wx.App en wxPython que lo que hace es ejecutar automaticamente el metodo arrancar, por lo que no hace falta llamarlo manualmente
        base_datos.inicializar() # Llama a la base de datos para crear la tabla de pacientes si no existe
        self.frame = FramePrincipal() # Crea el objeto de la ventana principal
        self.frame.Show() # Hace que la ventana se vuelva visible en la pantalla
        return True # Le avisa al sistema que la app arranco correctamente

if __name__ == "__main__": # Pregunta si estas ejecutando ESTE archivo directamente
    app = BSKineApp(False) # Crea la aplicacion (False es para que los errores salgan en la consola y no en cartelitos)
    app.MainLoop() # Inicia el bucle infinito que mantiene la ventana abierta esperando que el usuario haga clic en algo