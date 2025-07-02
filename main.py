import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Educativa de Inglés",
    description="API para evaluar respuestas en inglés y dar retroalimentación pedagógica",
    version="1.0.0"
)

# Cargar el dataset de preguntas y respuestas
try:
    df = pd.read_csv('dataset_chatbot_ingles.csv')
except Exception as e:
    print("Error al cargar el dataset:", e)
    df = pd.DataFrame(columns=['pregunta', 'respuesta_correcta', 'tipo_error', 'retroalimentacion'])

# Definir la estructura de los datos de entrada
class RespuestaEstudiante(BaseModel):
    question: str  # Pregunta en inglés
    answer: str    # Respuesta del estudiante

# Definir la estructura de la respuesta
class RespuestaAPI(BaseModel):
    is_correct: bool      # Indica si la respuesta es correcta
    error_type: str = None  # Tipo de error (si existe)
    feedback: str         # Retroalimentación para el estudiante

def limpiar_texto(texto: str) -> str:
    """
    Limpia el texto para hacer comparaciones más precisas:
    - Convierte a minúsculas
    - Elimina espacios extra
    - Normaliza puntuación
    """
    texto = texto.lower().strip()
    texto = texto.replace("''", "'").replace('""', "'")
    texto = " ".join(texto.split())
    return texto

@app.post("/evaluate")
async def evaluar_respuesta(respuesta: RespuestaEstudiante):
    """
    Evalúa la respuesta del estudiante y proporciona retroalimentación educativa
    """
    try:
        # Limpiar textos para comparación
        pregunta = limpiar_texto(respuesta.question)
        respuesta_estudiante = limpiar_texto(respuesta.answer)
        
        # Buscar la pregunta en el dataset
        pregunta_encontrada = df[df['pregunta'].apply(limpiar_texto) == pregunta]
        
        if pregunta_encontrada.empty:
            return RespuestaAPI(
                is_correct=False,
                error_type="pregunta_no_encontrada",
                feedback="Lo siento, esta pregunta no está en nuestra base de datos."
            )
        
        # Verificar si la respuesta es correcta
        for _, fila in pregunta_encontrada.iterrows():
            if limpiar_texto(fila['respuesta_correcta']) == respuesta_estudiante:
                return RespuestaAPI(
                    is_correct=True,
                    error_type="ninguno",
                    feedback="¡Excelente trabajo! 🎉 Tu respuesta es correcta."
                )
            elif limpiar_texto(fila['respuesta_estudiante']) == respuesta_estudiante:
                # Si encontramos esta respuesta como una respuesta incorrecta conocida
                return RespuestaAPI(
                    is_correct=False,
                    error_type=fila['tipo_error'],
                    feedback=fila['retroalimentacion']
                )
        
        # Si llegamos aquí, la respuesta no coincide con ninguna conocida
        return RespuestaAPI(
            is_correct=False,
            error_type="error_general",
            feedback=f"Tu respuesta no es correcta. La respuesta correcta es: {pregunta_encontrada.iloc[0]['respuesta_correcta']}"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def inicio():
    """
    Página de inicio con instrucciones de uso
    """
    return {
        "mensaje": "¡Bienvenido al Sistema de Evaluación de Inglés!",
        "instrucciones": [
            "1. Envía una pregunta y respuesta en inglés al endpoint /evaluate",
            "2. Recibirás retroalimentación sobre tu respuesta",
            "3. Si hay errores, se te explicará cómo mejorar"
        ],
        "ejemplo": {
            "question": "How are you?",
            "answer": "I am fine, thank you"
        }
    }

# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
