import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import uvicorn

# Load and preprocess the dataset
df = pd.read_csv('dataset_chatbot_ingles.csv')

# Create the model pipeline for error classification
error_classifier = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', LinearSVC())
])

# Train the model on the dataset
# We'll combine question and student answer for better context
X = df['pregunta'] + ' | ' + df['respuesta_estudiante']
y = df['tipo_error']
error_classifier.fit(X, y)

# Create FastAPI app
app = FastAPI(
    title="English Learning Feedback API",
    description="API para evaluar respuestas en inglés y proporcionar retroalimentación pedagógica",
    version="1.0.0"
)

class StudentResponse(BaseModel):
    question: str
    answer: str

class FeedbackResponse(BaseModel):
    is_correct: bool
    error_type: str = None
    feedback: str

def get_feedback(row):
    """Get appropriate feedback based on the dataset"""
    matching_feedback = df[
        (df['pregunta'] == row['pregunta']) & 
        (df['respuesta_estudiante'] == row['respuesta_estudiante'])
    ]
    
    if not matching_feedback.empty:
        return matching_feedback.iloc[0]['retroalimentacion']
    
    # If no exact match, get feedback based on error type
    similar_errors = df[df['tipo_error'] == row['tipo_error']]
    if not similar_errors.empty:
        return similar_errors.iloc[0]['retroalimentacion']
    
    return "Revisa tu respuesta. Hay un error en la estructura de la oración."

@app.post("/evaluate", response_model=FeedbackResponse)
async def evaluate_answer(response: StudentResponse):
    try:
        # Check if the answer matches any correct answer in our dataset
        is_correct = False
        correct_answers = df[df['pregunta'] == response.question]['respuesta_correcta'].values
        
        if len(correct_answers) > 0:
            is_correct = response.answer.lower().strip() == correct_answers[0].lower().strip()
        
        if is_correct:
            return FeedbackResponse(
                is_correct=True,
                error_type="ninguno",
                feedback="¡Excelente trabajo! Tu respuesta es correcta. 🎉"
            )
        
        # If incorrect, classify the error
        input_text = f"{response.question} | {response.answer}"
        error_type = error_classifier.predict([input_text])[0]
        
        # Get appropriate feedback
        feedback = get_feedback({
            'pregunta': response.question,
            'respuesta_estudiante': response.answer,
            'tipo_error': error_type
        })
        
        return FeedbackResponse(
            is_correct=False,
            error_type=error_type,
            feedback=feedback
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Retroalimentación de Inglés",
        "usage": "Envía una solicitud POST a /evaluate con la pregunta y respuesta del estudiante"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
