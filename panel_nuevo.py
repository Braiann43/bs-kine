import wx 
import wx.adv # Importa modulos extra (como calendarios y relojes)
import constantes # Importa las variables de colores y tamaños
import base_datos # Importa la base de datos para usarla en los eventos
from utilidades import crear_campo # Importa la función que sirve para crear las cajas de texto tipo nombre, dni o datos y mas

# --- PANTALLA NUEVO PACIENTE ---
class PanelNuevo(wx.Panel):
    def __init__(self, parent): 
        super().__init__(parent)
        self.SetBackgroundColour(constantes.C_FONDO) # Fondo oscuro
        sz_prin = wx.BoxSizer(wx.HORIZONTAL) # Organizador principal: divide en Izquierda y Derecha
        
        sz_izq = wx.BoxSizer(wx.VERTICAL) # Organizador columna izquierda (Datos)
        sz_der = wx.BoxSizer(wx.VERTICAL) # Organizador columna derecha (Historial)
        
        # --- IZQUIERDA: Datos y Turno ---
        self.txt_nombre = crear_campo(self, sz_izq, "Nombre y Apellido:") # Campo Nombre
        self.txt_dni = crear_campo(self, sz_izq, "Documento (D.N.I):") # Campo DNI
        self.fec_nacimiento = crear_campo(self, sz_izq, "Fecha de Nacimiento:", widget=wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)) # Campo de fecha de nacimiento usando el widget de calendario (DatePickerCtrl)
        self.txt_telefono = crear_campo(self, sz_izq, "Teléfono de Contacto:") # Campo Telefono
        self.txt_ocupacion = crear_campo(self, sz_izq, "Ocupación / Trabajo:") # Campo Ocupacion
        self.txt_valor = crear_campo(self, sz_izq, "Valor de la Sesión (Ej: $5000):")
        
        sz_izq.AddSpacer(15) # Deja un hueco de 15 píxeles para separar visualmente
        lbl_turno = wx.StaticText(self, label="Programar Primer Sesión:") # Titulo del turno
        lbl_turno.SetForegroundColour(constantes.C_BTN) # Pinta el título color fucsia
        lbl_turno.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)) # Letra negrita
        sz_izq.Add(lbl_turno, 0, wx.ALL, 5) # Lo añade a la columna izquierda
        
        sz_turno = wx.BoxSizer(wx.HORIZONTAL) # Organizador horizontal para poner Fecha y Hora lado a lado
        self.dia_turno = crear_campo(self, sz_turno, "Día:", widget=wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)) # Calendario turno
        self.hora_turno = crear_campo(self, sz_turno, "Hora:", widget=wx.adv.TimePickerCtrl(self)) # Reloj del turno
        sz_izq.Add(sz_turno, 0, wx.EXPAND | wx.ALL, 0) # Añade fecha y hora a la columna izquierda
        
        # --- DERECHA: Historial --- Aca use Multilinea para que el usuario pueda escribir mucho texto 
        self.txt_motivo = crear_campo(self, sz_der, "Motivo de la Consulta:", multilinea=True) # Campo Motivo grande
        self.txt_diagnostico = crear_campo(self, sz_der, "Diagnóstico Médico:", multilinea=True) # Campo Diagnóstico grande
        self.txt_antecedentes = crear_campo(self, sz_der, "Antecedentes Médicos Relevantes:", multilinea=True) # Campo Antecedentes grande
        self.txt_tratamiento = crear_campo(self, sz_der, "Tratamiento Propuesto:", multilinea=True) # Campo Tratamiento grande
        self.txt_alerta = crear_campo(self, sz_der, "Alertas / Contradicciones:", multilinea=True) # Campo Alertas grande
        self.txt_alerta.SetForegroundColour(constantes.C_ALERTA) # Pinta el texto de alertas en rojo
        
        
        btn = wx.Button(self, label="¡GUARDAR PACIENTE Y TURNO!") # Boton de guardar
        btn.SetBackgroundColour(constantes.C_BTN) # Boton fucsia
        btn.SetForegroundColour(constantes.C_TXT) # Letras blancas
        btn.Bind(wx.EVT_BUTTON, self.on_guardar) # Conecta el click del botón con la función 'on_guardar'
        sz_der.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 15) # Centra el botón abajo a la derecha
        
        sz_prin.Add(sz_izq, 1, wx.EXPAND | wx.ALL, 10) # Agrega la mitad izquierda a la pantalla
        sz_prin.Add(sz_der, 1, wx.EXPAND | wx.ALL, 10) # Agrega la mitad derecha a la pantalla
        self.SetSizer(sz_prin) # Aplica la organización a la pantalla

    def on_guardar(self, event): # Función que se ejecuta al apretar Guardar
        nom = self.txt_nombre.GetValue().strip() # Obtiene el nombre y borra espacios en blanco extra
        dni = self.txt_dni.GetValue().strip() # Obtiene el DNI y borra espacios extra
        
        if not nom or not dni: # Validacion: Si el nombre o dni están vacíos.
            wx.MessageBox("Nombre y DNI son obligatorios.", "Faltan datos", wx.ICON_WARNING) # Tira alerta
            return # Corta la función acá para no guardar datos vacíos
            
        # Extrae la fecha de los calendarios y las convierte a formato de texto ISO (AAAA-MM-DD)
        nac = self.fec_nacimiento.GetValue().FormatISODate() 
        dia = self.dia_turno.GetValue().FormatISODate()
        
        # Saca la hora del reloj en texto, pero el [:5] recorta los segundos (ej: "10:30:00" pasa a "10:30")
        hora = self.hora_turno.GetValue().FormatISOTime()[:5]
        
        # Junta todos los campos de texto en un "paquete" (tupla)
        datos = (nom, dni, nac, self.txt_telefono.GetValue(), self.txt_ocupacion.GetValue(),
                 self.txt_motivo.GetValue(), self.txt_diagnostico.GetValue(), self.txt_antecedentes.GetValue(), self.txt_tratamiento.GetValue(), self.txt_alerta.GetValue(), dia, hora, self.txt_valor.GetValue().strip())
                 
        import base_datos # Importa la Base de Datos para guardar
        if base_datos.guardar_paciente(datos): # Intenta guardar, si devuelve True es que funciono
            wx.MessageBox("¡Paciente y Turno guardados exitosamente!", "Éxito", wx.ICON_INFORMATION) # Cartel de exito
            
            # --- LIMPIEZA DEL FORMULARIO ---
            self.txt_nombre.SetValue("") # Borra el texto de nombre
            self.txt_dni.SetValue("") # Borra DNI
            self.txt_telefono.SetValue("") # Borra Teléfono
            self.txt_ocupacion.SetValue("") # Borra Ocupacion
            self.txt_motivo.SetValue("") # Borra Motivo
            self.txt_diagnostico.SetValue("") # Borra Diagnostico
            self.txt_antecedentes.SetValue("") # Borra Antecedentes
            self.txt_tratamiento.SetValue("") # Borra Tratamiento
            self.txt_alerta.SetValue("") # Borra Alertas
            self.txt_valor.SetValue("") # Borra Valor
            
            
            hoy = wx.DateTime.Now() # Consigue la fecha y hora exacta actual
            self.fec_nacimiento.SetValue(hoy) # Reinicia calendario de nacimiento
            self.dia_turno.SetValue(hoy) # Reinicia calendario de turno
            self.hora_turno.SetValue(hoy) # Reinicia reloj de turno
            
        else:
            wx.MessageBox("Ese DNI ya está registrado.", "Error", wx.ICON_ERROR) # Si devolvio False, tira error de DNI duplicado