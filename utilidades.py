import wx
import constantes

# --- FUNCION AYUDANTE --- "Sirve para crear las cajas de texto tipo nombre, dni o datos y mas..."
def crear_campo(padre, sizer, texto, multilinea=False, widget=None): # Funcion para crear etiquetas y cajas de texto rapido (Ahorra muchas lineas de codigo)
    lbl = wx.StaticText(padre, label=texto) # Crea el texto (la etiqueta)
    lbl.SetForegroundColour(constantes.C_TXT) # Le pone el color blanco definido en constantes
    sizer.Add(lbl, 0, wx.TOP | wx.LEFT, 5) # Añade la etiqueta al organizador visual (sizer) con 5px de margen
    # Si le pasamos un widget (ej. calendario) usa ese. Si no, crea una caja de texto normal (multilinea si se lo pedimos)
    ctrl = widget if widget else wx.TextCtrl(padre, style=wx.TE_MULTILINE if multilinea else 0)
    # Añade la caja de texto al organizador visual para que ocupe todo el ancho posible
    sizer.Add(ctrl, 1 if multilinea else 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
    return ctrl # Devuelve la caja creada para que la podamos guardar y leer despues