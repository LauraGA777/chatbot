import pandas as pd  # Para manejo de datos
from fastapi import FastAPI, HTTPException  # Para crear la API
from pydantic import BaseModel  # Para validar datos de entrada
from sklearn.feature_extraction.text import TfidfVectorizer  # Para procesar texto
from sklearn.svm import LinearSVC  # Modelo de clasificación
from sklearn.pipeline import Pipeline  # Para crear flujo de procesamiento
import uvicorn  # Servidor web para la API

# Cargar el dataset desde el archivo CSV
df = pd.read_csv('dataset_chatbot_ingles.csv')

# Crear y entrenar el modelo de clasificación de errores
# Este modelo ayudará a identificar el tipo de error en las respuestas incorrectas
modelo_clasificador = Pipeline([
    ('procesador_texto', TfidfVectorizer()),  # Convierte texto a números
    ('clasificador', LinearSVC())             # Modelo de clasificación
])

# Preparar los datos para entrenar el modelo
# Combinamos pregunta y respuesta para dar más contexto al modelo
X = df['pregunta'] + ' | ' + df['respuesta_estudiante']  # Datos de entrada
y = df['tipo_error']                                     # Tipos de error a predecir
modelo_clasificador.fit(X, y)  # Entrenamos el modelo

# Configurar la aplicación FastAPI
app = FastAPI(
    title="API de Aprendizaje de Inglés",
    description="API para evaluar respuestas en inglés y dar retroalimentación",
    version="1.0.0"
)

# Definir la estructura de los datos que recibiremos
class RespuestaEstudiante(BaseModel):
    question: str  # Pregunta en inglés
    answer: str    # Respuesta del estudiante

# Definir la estructura de la respuesta que enviaremos
class RespuestaAPI(BaseModel):
    is_correct: bool      # Indica si la respuesta es correcta
    error_type: str = None  # Tipo de error (si existe)
    feedback: str         # Retroalimentación para el estudiante

def obtener_retroalimentacion(datos):
    """
    Busca la retroalimentación apropiada para una respuesta
    basándose en ejemplos similares en el dataset
    """
    # Buscar retroalimentación exacta
    retroalimentacion_igual = df[
        (df['pregunta'] == datos['pregunta']) & 
        (df['respuesta_estudiante'] == datos['respuesta_estudiante'])
    ]
    
    if not retroalimentacion_igual.empty:
        return retroalimentacion_igual.iloc[0]['retroalimentacion']
    
    # Si no hay coincidencia exacta, buscar por tipo de error
    errores_similares = df[df['tipo_error'] == datos['tipo_error']]
    if not errores_similares.empty:
        return errores_similares.iloc[0]['retroalimentacion']
    
    return "Revisa tu respuesta. Hay un error en la estructura de la oración."

def limpiar_texto(texto: str) -> str:
    """
    Limpia y normaliza el texto para hacer comparaciones más precisas
    """
    # Convertir a minúsculas y quitar espacios al inicio/final
    texto = texto.lower().strip()
    # Normalizar las comillas
    texto = texto.replace("''", "'").replace('""', "'")
    # Asegurar un solo espacio entre palabras
    texto = " ".join(texto.split())
    return texto

@app.post("/evaluate")
async def evaluar_respuesta(respuesta: RespuestaEstudiante):
    """
    Endpoint principal que evalúa la respuesta del estudiante
    y proporciona retroalimentación
    """
    try:
        # Paso 1: Limpiar el texto de la pregunta y respuesta
        pregunta_limpia = limpiar_texto(respuesta.question)
        respuesta_limpia = limpiar_texto(respuesta.answer)
        
        # Paso 2: Verificar si la respuesta es correcta
        es_correcta = False
        for _, fila in df.iterrows():
            if (limpiar_texto(fila['pregunta']) == pregunta_limpia and 
                limpiar_texto(fila['respuesta_correcta']) == respuesta_limpia):
                es_correcta = True
                break
        
        # Paso 3: Si es correcta, devolver mensaje de éxito
        if es_correcta:
            return RespuestaAPI(
                is_correct=True,
                error_type="ninguno",
                feedback="¡Excelente trabajo! Tu respuesta es correcta. 🎉"
            )
        
        # Paso 4: Si es incorrecta, clasificar el tipo de error
        texto_entrada = f"{pregunta_limpia} | {respuesta_limpia}"
        tipo_error = modelo_clasificador.predict([texto_entrada])[0]
        
        # Paso 5: Obtener retroalimentación específica
        retroalimentacion = obtener_retroalimentacion({
            'pregunta': pregunta_limpia,
            'respuesta_estudiante': respuesta_limpia,
            'tipo_error': tipo_error
        })
        
        return RespuestaAPI(
            is_correct=False,
            error_type=tipo_error,
            feedback=retroalimentacion
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Página de inicio
@app.get("/")
async def inicio():
    return {
        "mensaje": "Bienvenido a la API de Retroalimentación de Inglés",
        "uso": "Envía una solicitud POST a /evaluate con la pregunta y respuesta del estudiante"
    }

# Iniciar el servidor cuando se ejecuta el archivo
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
