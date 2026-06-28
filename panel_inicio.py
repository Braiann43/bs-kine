import wx 
import wx.grid # Importa el modulo para crear grillas tipo Excel
import constantes
import base_datos 

# --- PANTALLA INICIO ---
class PanelInicio(wx.Panel):
    def __init__(self, parent): # Constructor de la pantalla
        super().__init__(parent) # Inicializa el panel
        self.SetBackgroundColour(constantes.C_FONDO) # Pinta el fondo oscuro con los colores definidos en constantes
        sz = wx.BoxSizer(wx.VERTICAL) # Crea un organizador que apila las cosas de arriba hacia abajo
        
        lbl_t = wx.StaticText(self, label="Turnos para Hoy") # Título de la seccion
        lbl_t.SetForegroundColour(constantes.C_TXT) # Letra blanca
        # Pone la letra en tamaño 16 y en Negrita
        lbl_t.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sz.Add(lbl_t, 0, wx.ALL, 10) # Añade el título al organizador visual
        
        # --- GRILLA ESTILO EXCEL ---
        self.grilla = wx.grid.Grid(self) # Crea la grilla para los turnos de "HOY"
        self.grilla.CreateGrid(30, 5)  # Le da 30 filas y 5 columnas
        self.grilla.EnableEditing(False) # Bloquea la grilla para que el usuario no pueda borrar datos tipeando
        
        # Le pone los títulos a las 5 columnas usando un ciclo 'for'
        for i, col in enumerate(["Hora", "Paciente", "Tratamiento", "Valor", "Estado"]):
            self.grilla.SetColLabelValue(i, col)
            
        sz.Add(self.grilla, 1, wx.EXPAND | wx.ALL, 10) # Agrega la tabla para que ocupe el resto del espacio
        self.SetSizer(sz) # Le dice al panel que use este organizador
        self.Bind(wx.EVT_SHOW, self.on_mostrar)
        
        self.btn_estado = wx.Button(self, label="Cambiar Estado del Turno Seleccionado")
        self.btn_estado.SetBackgroundColour(constantes.C_BTN)
        self.btn_estado.SetForegroundColour(constantes.C_TXT)
        self.btn_estado.Bind(wx.EVT_BUTTON, self.on_cambiar_estado)
        sz.Add(self.btn_estado, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
        
        self.SetSizer(sz) 
        self.Bind(wx.EVT_SHOW, self.on_mostrar)
        
        # Lista oculta para saber qué paciente está en qué fila
        self.turnos_ids = []
        
    def on_mostrar(self, event):
        """Se activa cuando la pestaña se vuelve visible"""
        if event.IsShown(): # Si la pantalla realmente se esta mostrando...
            self.cargar_turnos() # Llama a la función que llena la grilla
        event.Skip()
        
    def cargar_turnos(self):
        import base_datos
        self.grilla.ClearGrid()
        turnos = base_datos.obtener_turnos_hoy()
        self.turnos_ids = [] # Vaciamos la lista cada vez que recargamos
        
        if turnos:
            # Desempaquetamos los 6 datos que envía la base de datos ahora
            for fila_idx, (p_id, hora, paciente, tratamiento, valor, estado) in enumerate(turnos):
                if fila_idx < self.grilla.GetNumberRows():
                    self.turnos_ids.append(p_id) # Guardamos el ID del paciente
                    
                    self.grilla.SetCellValue(fila_idx, 0, hora)        
                    self.grilla.SetCellValue(fila_idx, 1, paciente)    
                    self.grilla.SetCellValue(fila_idx, 2, tratamiento if tratamiento else "") 
                    self.grilla.SetCellValue(fila_idx, 3, valor if valor else "-")         
                    self.grilla.SetCellValue(fila_idx, 4, estado if estado else "Pendiente") 
        
        self.grilla.ForceRefresh()
    
    def on_cambiar_estado(self, event):
        # Averiguamos qué fila de la grilla tiene seleccionada el usuario
        fila_seleccionada = self.grilla.GetGridCursorRow()
        
        # Verificamos que la fila tocada realmente tenga un turno cargado
        if fila_seleccionada < len(self.turnos_ids):
            paciente_id = self.turnos_ids[fila_seleccionada]
            
            # Abre una ventanita nativa muy prolija para elegir opciones
            opciones = ["Pendiente", "Asistió", "Cancelado"]
            dlg = wx.SingleChoiceDialog(self, "Seleccione el nuevo estado:", "Actualizar Turno", opciones)
            
            if dlg.ShowModal() == wx.ID_OK:
                nuevo_estado = dlg.GetStringSelection()
                import base_datos
                base_datos.actualizar_estado_turno(paciente_id, nuevo_estado)
                self.cargar_turnos() # Recarga la grilla y el cambio se ve al instante
            dlg.Destroy()
        else:
            wx.MessageBox("Seleccioná una fila que contenga un turno válido.", "Atención", wx.ICON_WARNING)