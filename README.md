# Gestor de Eventos e Invitados

Aplicación en Python para la gestión de eventos e invitados utilizando MongoDB como base de datos NoSQL.

## Descripción

Sistema de gestión de eventos que permite:
- Listar eventos e invitados
- Filtrar por empresa, categoría y estado
- Búsquedas con expresiones regulares
- Consultas en subdocumentos
- Agregaciones con $lookup
- Validación de acceso a eventos

## Tecnologías

- **Python 3.8+**
- **MongoDB**
- **PyMongo**
- **python-dotenv**

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/gestor-eventos-mongodb.git
cd gestor-eventos-mongodb
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar MongoDB

Asegúrate de que MongoDB esté ejecutándose:

```bash
mongod
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

## 🗂️ Estructura del Proyecto

```
gestor-eventos-mongodb/
├── app.py              # Aplicación principal
├── database.py         # Conexión a MongoDB
├── queries.py          # Consultas específicas
├── menu.py             # Menú de navegación
├── invitados.json      # Datos de invitados
├── eventos.json        # Datos de eventos
├── .env                # Variables de entorno
├── requirements.txt    # Dependencias
└── README.md           # Documentación
```

## Funcionalidades

### Actividad 1: Filtros y condiciones
- Listar todos los eventos
- Listar invitados activos
- Filtrar invitados por empresa
- Filtrar eventos por categoría

### Actividad 2: Expresiones Regulares
- Buscar invitados por nombre
- Buscar por dominio de correo
- Buscar eventos por palabra

### Actividad 3: Subdocumentos
- Eventos donde aparece un invitado
- Verificar confirmación en evento
- Contar confirmados por evento

### Actividad 4: $lookup y Agregaciones
- Eventos con detalles de invitados
- Top 3 eventos con más confirmados
- Validar acceso a evento

## Modelo de Datos

### Colección `invitados`
```json
{
  "rut": "11.009.876-3",
  "nombre": "Camila Herrera",
  "correo": "camila.herrera@empresa.cl",
  "empresa": "EmpresaX",
  "estado": "activo"
}
```

### Colección `eventos`
```json
{
  "codigo": "EVT-2025-001",
  "nombre": "Evento 1 - Datos",
  "fecha": "2025-12-25T20:00:00Z",
  "lugar": "Auditorio B",
  "categoria": "charla",
  "invitados": [
    {"rut": "11.118.512-6", "estado": "confirmado", "checkin": false}
  ]
}
```

## Variables de Entorno

Crear archivo `.env`:

```env
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=prueba3
```

## Evaluación

Este proyecto corresponde a la Evaluación Sumativa de la Unidad 3 de la asignatura **Bases de Datos No Estructuradas (TI3032)**.

### Criterios de Evaluación
- Selección de filtros y condiciones
- Uso de expresiones regulares
- Consultas en subdocumentos
- Agregaciones con $lookup
- Organización y seguridad

