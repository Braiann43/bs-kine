# BS-Kine - Sistema de Gestión para Kinesiología

**BS-Kine** es una aplicación de escritorio versión 1.0 diseñada específicamente para optimizar la gestión de pacientes, turnos e historias clínicas en consultorios de kinesiología. 

Este proyecto fue desarrollado como parte de mi formación académica y profesional, en parte para la materia de Programación Orientada a Objetos. Construido con Python, proporciona una interfaz gráfica intuitiva y un sistema de almacenamiento de datos local seguro.

## 🚀 Características Principales

* **Panel de Inicio (Turnos del Día):** Visualización rápida de los turnos programados para la fecha actual mediante una grilla estilo Excel, permitiendo actualizar el estado del turno a "Pendiente", "Asistió" o "Cancelado".
* **Registro de Pacientes:** Formulario completo para ingresar datos personales y programar la primera sesión con fecha y hora.
* **Historia Clínica Digital:** Seguimiento detallado del motivo de consulta, diagnóstico médico, antecedentes relevantes, tratamiento propuesto y alertas o contraindicaciones visualizadas en rojo para mayor seguridad.
* **Gestión de Sesiones:** Módulo para cargar el detalle de cada nueva sesión realizada, manteniendo un historial cronológico inalterable por paciente.
* **Administración Total:** Capacidad para editar la ficha clínica completa, programar próximos turnos o eliminar registros de manera definitiva.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica (GUI):** `wxPython`
* **Base de Datos:** `SQLite3` para almacenamiento local y ligero.

## 📂 Estructura del Proyecto

* `main.py`: Punto de entrada de la aplicación que inicializa la base de datos y la interfaz.
* `interfaz.py`: Configuración de la ventana principal y el menú lateral.
* `base_datos.py`: Consultas SQL para la creación de tablas y operaciones CRUD.
* `constantes.py`: Definición de colores, dimensiones y metadatos.
* `utilidades.py`: Funciones reutilizables para la generación de campos.
* `panel_inicio.py`, `panel_nuevo.py`, `panel_pacientes.py`: Controladores de las vistas.

## ⚙️ Instalación y Uso

1. Clonar este repositorio.
2. Instalar la librería requerida ejecutando: `pip install wxPython`
3. Ejecutar el archivo principal: `python main.py`
4. Al abrirse por primera vez, el sistema creará automáticamente el archivo `bs_kine_datos.db`.

## 👨‍💻 Autor y Licencia

**Braian Nicolas Videla** 
Estudiante de la Tecnicatura Universitaria en Desarrollo de Software en la Universidad Nacional de Pilar (UNPilar).

Este proyecto es de código abierto y se distribuye bajo los términos de la [Licencia MIT](LICENSE). Eres libre de utilizar y modificar este software, siempre y cuando se mantenga el reconocimiento al autor original.
