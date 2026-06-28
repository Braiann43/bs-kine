import wx 
import wx.adv
import constantes 
import base_datos 
from utilidades import crear_campo 

# --- PANTALLA HISTORIAL PACIENTES ---
class PanelPacientes(wx.Panel): # Clase para buscar el historial
    def __init__(self, parent): 
        super().__init__(parent)
        self.SetBackgroundColour(constantes.C_FONDO) # Fondo oscuro
        sz_prin = wx.BoxSizer(wx.HORIZONTAL) # Organizador Izquierda/Derecha
        
        # --- IZQUIERDA: Lista ---
        sz_izq = wx.BoxSizer(wx.VERTICAL) # Columna izquierda
        lbl_lista = wx.StaticText(self, label="Seleccione un paciente de la lista:")
        lbl_lista.SetForegroundColour(constantes.C_TXT)
        sz_izq.Add(lbl_lista, 0, wx.ALL, 5)
        
        self.lista = wx.ListBox(self, choices=[]) # Crea la lista vacia donde iran los nombres
        self.lista.Bind(wx.EVT_LISTBOX, self.on_seleccionar) # Conecta el click en la lista a la funcion 'on_seleccionar' creada mas abajo
        sz_izq.Add(self.lista, 1, wx.EXPAND | wx.ALL, 5) # Añade la lista a la columna
        
        # --- DERECHA: Visor de Historial ---
        sz_der = wx.BoxSizer(wx.VERTICAL) # Columna derecha (HISTORIAL GENERAL, SESIONES ANTERIORES, DETALLES DE LA NUEVA SESION Y GUARDAR SESION)
        
        self.lbl_nom = wx.StaticText(self, label="SELECCIONE UN PACIENTE") # Título gigante inicial
        self.lbl_nom.SetForegroundColour(constantes.C_TXT)
        self.lbl_nom.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)) # Negrita, tamaño 14
        sz_der.Add(self.lbl_nom, 0, wx.ALL, 5) # Añade el título
        
        # Caja gigante para el historial. Se crea y se bloquea (Editable=False) para que no la borren por accidente
        self.txt_historial_general = crear_campo(self, sz_der, "Historial General (Motivo, Diagnóstico, Antecedentes, Tratamiento y Alertas):", multilinea=True)
        self.txt_historial_general.SetEditable(False)
        
        # Caja gigante para sesiones. TambiEn bloqueada.
        self.txt_sesiones_anteriores = crear_campo(self, sz_der, "Sesiones Anteriores:", multilinea=True)
        self.txt_sesiones_anteriores.SetEditable(False)
        
        # Caja para anotar que se le hizo hoy al pacidente
        self.txt_nueva_sesion = crear_campo(self, sz_der, "Detalle de Nueva Sesión Realizada:", multilinea=True)
        
        # Organizador horizontal para los dos botones
        sz_botones = wx.BoxSizer(wx.HORIZONTAL)
        
        # BOTON EDITAR FICHA
        self.btn_editar = wx.Button(self, label="EDITAR FICHA")
        self.btn_editar.SetBackgroundColour("#4A3B6B") # Un color violeta oscuro para diferenciarlo
        self.btn_editar.SetForegroundColour(constantes.C_TXT)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar_paciente) # Lo vinculamos a su función
        sz_botones.Add(self.btn_editar, 0, wx.RIGHT, 10) # 10px de separación con el otro botón
        
        # BOTON ELIMINAR PACIENTE
        self.btn_eliminar = wx.Button(self, label="ELIMINAR PACIENTE")
        self.btn_eliminar.SetBackgroundColour(constantes.C_ALERTA) # Color rojo para alertar al usuario
        self.btn_eliminar.SetForegroundColour(constantes.C_TXT)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar_paciente)
        sz_botones.Add(self.btn_eliminar, 0, wx.RIGHT, 10)
        
        
        # BOTON GUARDAR SESION
        self.btn_guardar_sesion = wx.Button(self, label="GUARDAR SESIÓN") 
        self.btn_guardar_sesion.SetBackgroundColour(constantes.C_BTN) 
        self.btn_guardar_sesion.SetForegroundColour(constantes.C_TXT) 
        self.btn_guardar_sesion.Bind(wx.EVT_BUTTON, self.on_guardar_sesion)
        sz_botones.Add(self.btn_guardar_sesion, 0) 
        
        sz_der.Add(sz_botones, 0, wx.ALIGN_RIGHT | wx.ALL, 5) # Añadimos el grupo de botones abajo a la derecha
        sz_prin.Add(sz_izq, 1, wx.EXPAND | wx.ALL, 10) 
        sz_prin.Add(sz_der, 2, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sz_prin)
        
        self.Bind(wx.EVT_SHOW, self.on_mostrar) 
        
        # Variable oculta para saber a qué ID le estamos agregando la sesión
        self.paciente_actual_id = None

    def on_mostrar(self, event): # Sirve para recargar la lista de pacientes cada vez que tocamos la seccion "PACIENTES"
        if event.IsShown(): # Verifica que la pestaña realmente se este mostrando
            nombres = base_datos.obtener_nombres() # Pide todos los nombres a la base de datos
            self.lista.Set(nombres) # Rellena la lista con los nombres obtenidos
            
            # Limpieza total de la pantalla al entrar a la pestaña
            self.lbl_nom.SetLabel("SELECCIONE UN PACIENTE")
            self.txt_historial_general.SetValue("")
            self.txt_sesiones_anteriores.SetValue("")
            self.txt_nueva_sesion.SetValue("")
            self.paciente_actual_id = None # Reseteamos el ID activo
        event.Skip()
        
    # La funcion guarda el texto en la base de datos
    def on_guardar_sesion(self, event):
        if not self.paciente_actual_id: # Si intentan guardar sin elegir paciente
            wx.MessageBox("Primero seleccioná un paciente de la lista.", "Atención", wx.ICON_WARNING)
            return
            
        detalle = self.txt_nueva_sesion.GetValue().strip()
        if not detalle: # Si aprietan guardar pero la caja esta vacia
            wx.MessageBox("No escribiste ningún detalle para la sesión.", "Faltan datos", wx.ICON_WARNING)
            return
            
        import base_datos
        base_datos.guardar_sesion(self.paciente_actual_id, detalle)
        wx.MessageBox("¡Sesión guardada con éxito!", "Éxito", wx.ICON_INFORMATION)
        
        self.txt_nueva_sesion.SetValue("") # Limpiamos la caja para que quede vacía
        self.on_seleccionar(None) # Refrescamos la pantalla para que la sesión aparezca arriba al instante
    
    
    def on_editar_paciente(self, event):
        """Abre la ventana flotante para editar los datos clínicos del paciente"""
        if not self.paciente_actual_id:
            wx.MessageBox("Primero seleccioná un paciente de la lista para editar.", "Atención", wx.ICON_WARNING)
            return
            
        # Volvemos a pedir los datos frescos del paciente a la base de datos
        nombre_sel = self.lista.GetStringSelection()
        datos_paciente = base_datos.obtener_datos_paciente(nombre_sel)
        
        # Instanciamos y abrimos la ventana flotante pasandole los datos actuales
        dlg = DialogEditar(self, datos_paciente)
        if dlg.ShowModal() == wx.ID_OK:
            wx.MessageBox("¡Ficha del paciente actualizada con éxito!", "Éxito", wx.ICON_INFORMATION)
            self.on_seleccionar(None) # Refrescamos el visor del historial para ver los cambios en pantalla inmediatamente
        dlg.Destroy() # Destruimos la ventana flotante al cerrar para liberar memoria
        
    def on_eliminar_paciente(self, event):
        """Elimina definitivamente un paciente."""
        
        # Verifica que el usuario haya seleccionado un paciente antes de intentar eliminarlo
        if not self.paciente_actual_id:
            wx.MessageBox(
                "Primero seleccioná un paciente.",
                "Atención",
                wx.ICON_WARNING
            )
            return  # Sale de la funcion porque no hay ningun paciente seleccionado
        
        # Muestra una ventana de confirmacion para evitar borrados accidentales
        respuesta = wx.MessageBox(
            "¿Estás seguro de eliminar este paciente?\n\n"
            "También se eliminarán todas sus sesiones.\n\n"
            "Esta acción NO se puede deshacer.",
            "Confirmar eliminación",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING
        )
        # Si el usuario eligio "No" termina la funcion sin borrar nada
        if respuesta != wx.YES:
            return
        # Llama a la base de datos para eliminar el paciente y todas sus sesiones
        base_datos.eliminar_paciente(self.paciente_actual_id)
        
        # Muestra un mensaje informando que la eliminación fue exitosa
        wx.MessageBox(
            "Paciente eliminado correctamente.",
            "Éxito",
            wx.ICON_INFORMATION
        )

        # Vuelve a pedir la lista actualizada de pacientes
        nombres = base_datos.obtener_nombres()
        
        # Actualiza el ListBox para que desaparezca el paciente eliminado
        self.lista.Set(nombres)

        # Limpia toda la informacion que estaba mostrando el panel
        self.lbl_nom.SetLabel("SELECCIONE UN PACIENTE")
        self.txt_historial_general.SetValue("")
        self.txt_sesiones_anteriores.SetValue("")
        self.txt_nueva_sesion.SetValue("")
        
        # Borra el ID guardado para indicar que ya no hay ningun paciente seleccionado
        self.paciente_actual_id = None

    def on_seleccionar(self, event): # Esta funcion se ejeuta al tocar un nomre de la lista (Y PROCEDE A MOSTRAR SU HISTORIAL)
        nombre_seleccionado = self.lista.GetStringSelection() # Obtiene el texto exacto del nombre tocado
        datos = base_datos.obtener_datos_paciente(nombre_seleccionado) # Pide todo el historial a la Base de Datos usando ese nombre
        
        if datos: # Si la base de datos encontró los datos
            self.paciente_actual_id = datos[0] # Guardamos el ID real de la base de datos
            # Cambia el título grande por el Nombre y DNI reales del paciente
            self.lbl_nom.SetLabel(f"PACIENTE: {datos[1]} (DNI: {datos[2]})")
            
            # Formateo de fecha: Agarra "YYYY-MM-DD" y lo parte en los guiones
            partes_fecha = datos[11].split("-")
            if len(partes_fecha) == 3: # Si se partió bien en 3 pedazos
                anio, mes, dia = partes_fecha[0], partes_fecha[1], partes_fecha[2] # Los asigna a variables
                fecha_formateada = f"{dia}-{mes}-{anio}" # Los rearma en un formato más amigable
            else:
                fecha_formateada = datos[11] # Si algo falló, deja la fecha original

            # Agrupa todo el historial "HISTORIAL GENERAL" en una sola gran cadena de texto con espacios 
            texto_armado = (
                f"MOTIVO DE CONSULTA:\n{datos[6]}\n\n"
                f"DIAGNÓSTICO:\n{datos[7]}\n\n"
                f"ANTECEDENTES:\n{datos[8]}\n\n"
                f"TRATAMIENTO PROPUESTO:\n{datos[9]}\n\n"
                f"ALERTAS / CONTRADICCIONES:\n{datos[10]}\n\n"
                f"FECHA DE PRIMER CONSULTA: {fecha_formateada}\n"
                f"HORA: {datos[12]}"
            )
            
            self.txt_historial_general.SetValue(texto_armado) # Inyecta todo el texto gigante en la caja bloqueada
            
            sesiones = base_datos.obtener_sesiones(self.paciente_actual_id)
            if sesiones:
                texto_sesiones = ""
                for fecha, detalle in sesiones:
                    texto_sesiones += f"[{fecha}] - {detalle}\n{'-'*40}\n" # Separa cada sesion con rayitas
                self.txt_sesiones_anteriores.SetValue(texto_sesiones)
            else:
                self.txt_sesiones_anteriores.SetValue("Aún no hay registro de sesiones previas en el sistema.")

# --- VENTANA EMERGENTE PARA EDITAR PACIENTE ---
class DialogEditar(wx.Dialog):
    def __init__(self, parent, datos):
        # Crea un cuadro de dialogo flotante
        super().__init__(parent, title=f"Editar Ficha Clínica: {datos[1]}", size=(500, 750))
        self.SetBackgroundColour(constantes.C_FONDO)
        self.paciente_id = datos[0] # Guardamos el ID único del paciente
        
        sz_scroll = wx.BoxSizer(wx.VERTICAL)
        
        # --- ACÁ AGREGAMOS LOS FILTROS DE SEGURIDAD ---
        self.txt_tel = crear_campo(self, sz_scroll, "Teléfono de Contacto:")
        self.txt_tel.SetValue(datos[4] if datos[4] is not None else "")
        
        self.txt_ocupacion = crear_campo(self, sz_scroll, "Ocupación / Trabajo:")
        self.txt_ocupacion.SetValue(datos[5] if datos[5] is not None else "")
        
        self.txt_motivo = crear_campo(self, sz_scroll, "Motivo de la Consulta:", multilinea=True)
        self.txt_motivo.SetValue(datos[6] if datos[6] is not None else "")
        
        self.txt_diag = crear_campo(self, sz_scroll, "Diagnóstico Médico:", multilinea=True)
        self.txt_diag.SetValue(datos[7] if datos[7] is not None else "")
        
        self.txt_ant = crear_campo(self, sz_scroll, "Antecedentes Médicos Relevantes:", multilinea=True)
        self.txt_ant.SetValue(datos[8] if datos[8] is not None else "")
        
        self.txt_trat = crear_campo(self, sz_scroll, "Tratamiento Propuesto:", multilinea=True)
        self.txt_trat.SetValue(datos[9] if datos[9] is not None else "")
        
        self.txt_alerta = crear_campo(self, sz_scroll, "Alertas / Contraindicaciones:", multilinea=True)
        self.txt_alerta.SetValue(datos[10] if datos[10] is not None else "")
        self.txt_alerta.SetForegroundColour(constantes.C_ALERTA)
        
        self.txt_valor = crear_campo(self, sz_scroll, "Valor de la Sesión:")
        self.txt_valor.SetValue(datos[13] if len(datos) > 13 and datos[13] is not None else "")
        
        sz_scroll.AddSpacer(15)
        
        # --- PROGRAMAR PROXIMO TURNO ---
        lbl_turno = wx.StaticText(self, label="Programar Próximo Turno:")
        lbl_turno.SetForegroundColour(constantes.C_BTN)
        lbl_turno.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sz_scroll.Add(lbl_turno, 0, wx.ALL, 5)
        
        sz_turno = wx.BoxSizer(wx.HORIZONTAL)
        self.dia_turno = crear_campo(self, sz_turno, "Día:", widget=wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN))
        self.hora_turno = crear_campo(self, sz_turno, "Hora:", widget=wx.adv.TimePickerCtrl(self))
        sz_scroll.Add(sz_turno, 0, wx.EXPAND | wx.ALL, 0)

        # Botones de la ventana emergente
        sz_btn = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(self, label="Guardar Cambios y Turno")
        btn_ok.SetBackgroundColour(constantes.C_BTN)
        btn_ok.SetForegroundColour(constantes.C_TXT)
        btn_ok.Bind(wx.EVT_BUTTON, self.on_guardar)
        btn_cancel = wx.Button(self, label="Cancelar")
        btn_cancel.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CANCEL))
        
        sz_btn.Add(btn_ok, 0, wx.ALL, 5)
        sz_btn.Add(btn_cancel, 0, wx.ALL, 5)
        sz_scroll.Add(sz_btn, 0, wx.ALIGN_CENTER | wx.ALL, 15)
        
        self.SetSizer(sz_scroll)
        self.Layout()
        
    
    def on_guardar(self, event):
        """Agarra los textos modificados y los manda a la base de datos"""
        import base_datos
        
        dia_prox = self.dia_turno.GetValue().FormatISODate()
        hora_prox = self.hora_turno.GetValue().FormatISOTime()[:5]
        
        base_datos.actualizar_paciente(
            self.paciente_id,
            self.txt_tel.GetValue().strip(),
            self.txt_ocupacion.GetValue().strip(),
            self.txt_motivo.GetValue().strip(),
            self.txt_diag.GetValue().strip(),
            self.txt_ant.GetValue().strip(),
            self.txt_trat.GetValue().strip(),
            self.txt_alerta.GetValue().strip(),
            self.txt_valor.GetValue().strip(),
            dia_prox,
            hora_prox
        )

        self.EndModal(wx.ID_OK) # Cierra la ventana devolviendo el estado de "Exito"