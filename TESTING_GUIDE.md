# Ejemplos de Pruebas para la API

## Colección de Postman

### Request 1: Endpoint de Bienvenida
```
GET http://localhost:8000/
```

### Request 2: Respuesta Correcta - "I am"
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
    "question": "Complete: 'I ___ happy today'",
    "answer": "I am happy today"
}
```

### Request 3: Error de Concordancia - "I are"
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
    "question": "Complete: 'I ___ happy today'",
    "answer": "I are happy today"
}
```

### Request 4: Error de Concordancia - "You is"
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
    "question": "Complete: 'You ___ my friend'",
    "answer": "You is my friend"
}
```

### Request 5: Respuesta Correcta - "You are"
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
    "question": "Complete: 'You ___ my friend'",
    "answer": "You are my friend"
}
```

### Request 6: Error de Concordancia - "They am"
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
    "question": "Fill in the blank: 'They ___ at home'",
    "answer": "They am at home"
}
```

### Request 7: Error de Tiempo Verbal
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
    "question": "Translate: 'She goes to school'",
    "answer": "She going to school"
}
```

### Request 8: Traducción Correcta
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
    "question": "Translate: 'The dog is under the table'",
    "answer": "The dog is under the table"
}
```

## Scripts de Prueba con Python

### Script básico para pruebas
```python
import requests
import json

# URL base de la API
base_url = "http://localhost:8000"

# Función para hacer peticiones
def test_api(question, answer):
    url = f"{base_url}/evaluate"
    data = {
        "question": question,
        "answer": answer
    }
    
    response = requests.post(url, json=data)
    print(f"Pregunta: {question}")
    print(f"Respuesta: {answer}")
    print(f"Resultado: {response.json()}")
    print("-" * 50)

# Casos de prueba
test_cases = [
    ("Complete: 'I ___ happy today'", "I am happy today"),
    ("Complete: 'I ___ happy today'", "I are happy today"),
    ("Complete: 'You ___ my friend'", "You are my friend"),
    ("Complete: 'You ___ my friend'", "You is my friend"),
    ("Translate: 'She goes to school'", "She goes to school"),
    ("Translate: 'She goes to school'", "She going to school")
]

# Ejecutar pruebas
for question, answer in test_cases:
    test_api(question, answer)
```

## Comandos cURL para Pruebas Rápidas

### Prueba de endpoint principal
```bash
curl -X GET http://localhost:8000/
```

### Prueba respuesta correcta
```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Complete: '\''I ___ happy today'\''",
    "answer": "I am happy today"
  }'
```

### Prueba error de concordancia
```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Complete: '\''I ___ happy today'\''",
    "answer": "I are happy today"
  }'
```

### Prueba error de tiempo verbal
```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Translate: '\''She goes to school'\''",
    "answer": "She going to school"
  }'
```

## Resultados Esperados

### Para respuestas correctas:
```json
{
    "is_correct": true,
    "error_type": "ninguno",
    "feedback": "¡Excelente trabajo! Tu respuesta es correcta. 🎉"
}
```

### Para errores de concordancia:
```json
{
    "is_correct": false,
    "error_type": "error_concordancia",
    "feedback": "Con 'I' se usa 'am': I am happy today."
}
```

### Para errores de tiempo verbal:
```json
{
    "is_correct": false,
    "error_type": "error_tiempo_verbal",
    "feedback": "Usa el presente simple, no el continuo: She goes to school."
}
```

## Verificaciones de Estado

### Verificar que el servidor esté corriendo
```bash
curl -I http://localhost:8000/
```
Debería devolver: `HTTP/1.1 200 OK`

### Verificar documentación automática
Abrir en navegador: `http://localhost:8000/docs`

### Verificar esquema OpenAPI
```bash
curl http://localhost:8000/openapi.json
```
