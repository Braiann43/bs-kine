import wx 
import constantes 

# Las clases de los paneles 
from panel_inicio import PanelInicio
from panel_nuevo import PanelNuevo
from panel_pacientes import PanelPacientes

# --- VENTANA PRINCIPAL ---
class FramePrincipal(wx.Frame): 
    def __init__(self): 
        super().__init__(None, title="BS-Kine", size=(1024, 768)) # Configura titulo y tamaño
        sz_prin = wx.BoxSizer(wx.HORIZONTAL) # Organizador: divide el menu izquierdo de las pestañas
        
        panel_menu = wx.Panel(self, size=(200, -1)) # Crea el panel izquierdo de 200px (-1 es para que sea alto automático)
        panel_menu.SetBackgroundColour(constantes.C_MENU) # Fondo oscuro
        sz_menu = wx.BoxSizer(wx.VERTICAL) # Apila los botones de arriba hacia abajo
        
        lbl_t = wx.StaticText(panel_menu, label="BS-KINE") # Titulo del menu
        lbl_t.SetForegroundColour(constantes.C_BTN) # Letra fucsia
        lbl_t.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)) # Grande y negrita
        sz_menu.Add(lbl_t, 0, wx.ALIGN_CENTER | wx.ALL, 20) # Centrado y con margen
        
        self.book = wx.Simplebook(self) # Simplebook es como que actua como un cuaderno donde pasamos las páginas
        self.book.AddPage(PanelInicio(self.book), "Inicio") # Mete el panel Inicio en la página 0
        self.book.AddPage(PanelNuevo(self.book), "Nuevo") # Mete el panel Nuevo Paciente en la página 1
        self.book.AddPage(PanelPacientes(self.book), "Pacientes") # Mete el panel Pacientes en la página 2
        
        # Bucle que crea los botones y los conecta a sus pestañas respectivas
        # ESTO LO QUE HACE ES CREAR LOS BOTONES ("Inicio", "Pacientes", "+ Nuevo Paciente") y les asocia un numerito (0, 2 y 1)
        for txt, idx in zip(["Inicio", "Pacientes", "+ Nuevo Paciente"], [0, 2, 1]):
            btn = wx.Button(panel_menu, label=txt) # Crea el boton
            sz_menu.Add(btn, 0, wx.EXPAND | wx.ALL, 5) # Lo añade al menu
            # lambda los que hace es crear una funcion que dice "Cuando toquen este boton, cambien la pestaña a la que corresponde el numerito idx"
            btn.Bind(wx.EVT_BUTTON, lambda e, i=idx: self.book.ChangeSelection(i))
            
        panel_menu.SetSizer(sz_menu) # Aplica la organizacion del menu
        
        sz_prin.Add(panel_menu, 0, wx.EXPAND) # Pega el menu al borde izquierdo de la ventana principal
        sz_prin.Add(self.book, 1, wx.EXPAND) # Hace que las pestañas ocupen el resto de la ventana
        self.SetSizer(sz_prin) # Aplica el diseño global
        self.Layout() # Refresca los elementos para que se dibujen bien