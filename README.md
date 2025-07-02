# API de Retroalimentación para Aprendizaje de Inglés

## Descripción

Esta API está diseñada para empresas de educación como academias de idiomas, plataformas e-learning y colegios. Automatiza parte de la corrección docente utilizando inteligencia artificial para evaluar respuestas de inglés básico (nivel A1-A2).

### Funcionalidades

- ✅ Detecta si una respuesta es correcta o incorrecta
- 🔍 Clasifica tipos de errores (concordancia, preposiciones, tiempo verbal, etc.)
- 💬 Proporciona retroalimentación pedagógica específica
- 🎉 Envía mensajes de felicitación para respuestas correctas

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Scikit-learn**: Machine Learning (LinearSVC + TF-IDF)
- **Pandas**: Manejo de datos
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**
```bash
cd chatbot
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Verificar que el dataset existe**
Asegúrate de que el archivo `dataset_chatbot_ingles.csv` esté en el directorio del proyecto.

## Ejecución

### Iniciar el servidor de desarrollo
```bash
uvicorn main:app --reload
```

### Iniciar el servidor de producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## Documentación de la API

### Endpoints Disponibles

#### 1. Endpoint de Bienvenida
- **URL**: `GET /`
- **Descripción**: Mensaje de bienvenida y guía de uso
- **Respuesta**:
```json
{
    "message": "Bienvenido a la API de Retroalimentación de Inglés",
    "usage": "Envía una solicitud POST a /evaluate con la pregunta y respuesta del estudiante"
}
```

#### 2. Endpoint de Evaluación
- **URL**: `POST /evaluate`
- **Descripción**: Evalúa la respuesta del estudiante y proporciona retroalimentación
- **Content-Type**: `application/json`

**Estructura de la petición:**
```json
{
    "question": "string",
    "answer": "string"
}
```

**Estructura de la respuesta:**
```json
{
    "is_correct": true/false,
    "error_type": "string",
    "feedback": "string"
}
```

## Casos de Prueba

### 1. Respuesta Correcta
**Petición:**
```json
{
    "question": "Complete: 'I ___ happy today'",
    "answer": "I am happy today"
}
```

**Respuesta Esperada:**
```json
{
    "is_correct": true,
    "error_type": "ninguno",
    "feedback": "¡Excelente trabajo! Tu respuesta es correcta. 🎉"
}
```

### 2. Error de Concordancia
**Petición:**
```json
{
    "question": "Complete: 'I ___ happy today'",
    "answer": "I are happy today"
}
```

**Respuesta Esperada:**
```json
{
    "is_correct": false,
    "error_type": "error_concordancia",
    "feedback": "Con 'I' se usa 'am': I am happy today."
}
```

### 3. Error de Tiempo Verbal
**Petición:**
```json
{
    "question": "Translate: 'She goes to school'",
    "answer": "She going to school"
}
```

**Respuesta Esperada:**
```json
{
    "is_correct": false,
    "error_type": "error_tiempo_verbal",
    "feedback": "Usa el presente simple, no el continuo: She goes to school."
}
```

### 4. Más Ejemplos de Prueba

#### Error con "You"
```json
{
    "question": "Complete: 'You ___ my friend'",
    "answer": "You is my friend"
}
```

#### Error con "They"
```json
{
    "question": "Fill in the blank: 'They ___ at home'",
    "answer": "They am at home"
}
```

#### Traducción Correcta
```json
{
    "question": "Translate: 'The dog is under the table'",
    "answer": "The dog is under the table"
}
```

## Guía de Pruebas

### Con Postman

1. **Configurar petición GET**
   - Método: GET
   - URL: `http://localhost:8000/`
   - Enviar petición

2. **Configurar petición POST**
   - Método: POST
   - URL: `http://localhost:8000/evaluate`
   - Headers: `Content-Type: application/json`
   - Body: Seleccionar "raw" y "JSON", luego pegar uno de los ejemplos

### Con cURL

```bash
# Endpoint de bienvenida
curl -X GET http://localhost:8000/

# Evaluación de respuesta
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Complete: '\''I ___ happy today'\''",
    "answer": "I am happy today"
  }'
```

### Con la interfaz Swagger

1. Abrir navegador y ir a: `http://localhost:8000/docs`
2. Explorar los endpoints disponibles
3. Hacer clic en "Try it out" en el endpoint `/evaluate`
4. Ingresar los datos de prueba
5. Hacer clic en "Execute"

## Tipos de Errores Clasificados

El sistema puede identificar los siguientes tipos de errores:

- `error_concordancia`: Errores en la concordancia sujeto-verbo
- `error_tiempo_verbal`: Uso incorrecto de tiempos verbales
- `error_preposicion`: Uso incorrecto de preposiciones
- `error_tercera_persona`: Errores específicos de tercera persona
- `ninguno`: Respuesta correcta

## Estructura del Proyecto

```
chatbot/
├── main.py                     # Aplicación principal
├── dataset_chatbot_ingles.csv  # Dataset de entrenamiento
├── requirements.txt            # Dependencias
├── README.md                   # Esta documentación
└── .venv/                      # Entorno virtual (generado)
```

## Solución de Problemas

### Error "Method Not Allowed"
- Verificar que estés usando POST para `/evaluate` y GET para `/`

### Error "Module not found"
- Verificar que el entorno virtual esté activado
- Reinstalar dependencias: `pip install -r requirements.txt`

### Error al cargar dataset
- Verificar que el archivo `dataset_chatbot_ingles.csv` esté en el directorio correcto
- Verificar que el archivo tenga las columnas correctas

### Puerto en uso
- Cambiar el puerto: `uvicorn main:app --port 8001`
- O detener otros procesos que usen el puerto 8000

## Contacto y Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contacta al equipo de desarrollo.

---

**Versión**: 1.0.0  
**Fecha**: Junio 2025
