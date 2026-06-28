# BS-Kine - Gestión de Pacientes
# Creado por: Braian Nicolas Videla (2026)
# Distribuido bajo la Licencia MIT.


import sqlite3 

def ejecutar(query, parametros=(), fetch=False): # Esto sirve para no repetir la conexión cada vez
    """Función para interactuar con SQLite"""
    conn = sqlite3.connect("bs_kine_datos.db") # Abre (o crea) el archivo de la base de datos
    cur = conn.cursor() # Crea un "cursor" que es el intermediario que ejecuta las consultas
    cur.execute(query, parametros) # Manda la orden SQL reemplazando los parámetros de forma segura
    if fetch: # Pregunta si 'fetch' es True (es decir, si estamos PIDIENDO informacion)
        resultado = cur.fetchall() # Obtiene todos los resultados encontrados
        conn.close() # Cierra la conexión
        return resultado # Devuelve la información a quien la pidió
    conn.commit() # Si 'fetch' es False (es un INSERT/UPDATE), confirma y guarda los cambios
    conn.close() # Cierra la conexión

def inicializar(): # Prepara la base de datos la primera vez que se abre el programa
    """Crea la tabla con todos los campos necesarios si no existe"""
    # Ejecuta código SQL para crear la estructura de columnas. "dni TEXT UNIQUE" impide DNIs repetidos
    ejecutar('''CREATE TABLE IF NOT EXISTS pacientes 
                (id INTEGER PRIMARY KEY, nombre TEXT, dni TEXT UNIQUE,
                 nacimiento TEXT, telefono TEXT, ocupacion TEXT,
                 motivo TEXT, diagnostico TEXT, antecedentes TEXT, 
                 tratamiento TEXT, alertas TEXT,
                 fecha_turno TEXT, hora_turno TEXT, valor TEXT, estado_turno TEXT)''')
    
    # Tabla para guardar el historial de sesiones infinitas
    ejecutar('''CREATE TABLE IF NOT EXISTS sesiones
                (id INTEGER PRIMARY KEY, 
                 paciente_id INTEGER, 
                 fecha TEXT, 
                 detalle TEXT,
                 FOREIGN KEY(paciente_id) REFERENCES pacientes(id))''')

def guardar_paciente(datos): # Función que recibe la información del formulario
    """Recibe la tupla de datos desde la interfaz y la guarda"""
    try: # Intenta ejecutar lo siguiente (previniendo que falle)
        # Inserta los datos. Los signos de interrogación se reemplazan por lo que hay en 'datos'
        ejecutar('''INSERT INTO pacientes (nombre, dni, nacimiento, telefono, ocupacion, 
                    motivo, diagnostico, antecedentes, tratamiento, alertas, fecha_turno, hora_turno, valor, estado_turno) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pendiente')''', datos)
        return True # Si se guardó bien, devuelve Verdadero
    except sqlite3.IntegrityError: # Si el DNI ya está en la base de datos, SQLite tira este error
        return False # Falla si el DNI ya existe, devuelve Falso para que la interfaz muestre el cartelito de error

def obtener_nombres(): # Busca a todos los pacientes para llenar el menú desplegable
    """Devuelve solo la lista de nombres para rellenar el ListBox""" 
    # Pide solo la columna 'nombre' y los ordena alfabéticamente (ASC)
    filas = ejecutar("SELECT nombre FROM pacientes ORDER BY nombre ASC", fetch=True) 
    # Convierte el formato crudo de la base de datos a una lista de Python simple. Si está vacía devuelve []
    return [f[0] for f in filas] if filas else []

def obtener_datos_paciente(nombre): # Busca todo el historial de un paciente usando su nombre
    """Trae toda la información de un paciente específico""" 
    # Selecciona todas las columnas (*) donde el nombre coincida con el que le pasamos
    filas = ejecutar("SELECT * FROM pacientes WHERE nombre = ?", (nombre,), fetch=True)
    return filas[0] if filas else None # Devuelve solo el primer resultado (los datos del paciente), o Nada si no existe

# Guarda la session de un paciente específico
def guardar_sesion(paciente_id, detalle):
    import datetime
    # Obtiene la fecha de hoy automaticamente
    fecha_hoy = datetime.date.today().strftime("%Y-%m-%d") 
    ejecutar("INSERT INTO sesiones (paciente_id, fecha, detalle) VALUES (?, ?, ?)", 
             (paciente_id, fecha_hoy, detalle))

# Trae todas las sesiones de un paciente ordenadas de la más nueva a la mas vieja
def obtener_sesiones(paciente_id):
    return ejecutar("SELECT fecha, detalle FROM sesiones WHERE paciente_id = ? ORDER BY id DESC", 
                    (paciente_id,), fetch=True)
    
    
def obtener_turnos_hoy():
    """Busca en la base de datos los turnos que coincidan con la fecha de hoy"""
    import datetime
    # Consigue la fecha de hoy de la computadora
    hoy = datetime.date.today().strftime("%Y-%m-%d") 
    
    # Pide la hora, el nombre, el tratamiento y el valor propuesto de los turnos de hoy, ordenados por hora
    query = """
        SELECT id, hora_turno, nombre, tratamiento, valor, estado_turno
        FROM pacientes 
        WHERE fecha_turno = ? 
        ORDER BY hora_turno ASC
    """
    return ejecutar(query, (hoy,), fetch=True)

def actualizar_paciente(paciente_id, telefono, ocupacion, motivo, diagnostico, antecedentes, tratamiento, alertas, valor, fecha, hora):
    query = """
        UPDATE pacientes 
        SET telefono = ?, ocupacion = ?, motivo = ?, diagnostico = ?, antecedentes = ?, tratamiento = ?, alertas = ?, valor = ?, fecha_turno = ?, hora_turno = ?, estado_turno = 'Pendiente'
        WHERE id = ?
    """
    ejecutar(query, (telefono, ocupacion, motivo, diagnostico, antecedentes, tratamiento, alertas, valor, fecha, hora, paciente_id))

def actualizar_estado_turno(paciente_id, nuevo_estado):
    ejecutar("UPDATE pacientes SET estado_turno = ? WHERE id = ?", (nuevo_estado, paciente_id))
    
def eliminar_paciente(paciente_id):
    """Elimina un paciente y todas sus sesiones."""
    
    # Primero elimina todas las sesiones que pertenecen al paciente
    # Esto evita dejar registros sin un paciente asociado en la tabla de sesiones
    ejecutar("DELETE FROM sesiones WHERE paciente_id = ?", (paciente_id,))
    
    # Despues elimina el paciente de la tabla principal
    ejecutar("DELETE FROM pacientes WHERE id = ?", (paciente_id,))