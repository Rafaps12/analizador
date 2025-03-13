import os
import select
import logging
import concurrent.futures
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import cohere
from cohere import ClassifyExample

# 📌 Solución para evitar problemas de `epoll` en Windows
if not hasattr(select, "epoll"):
    select.epoll = select.poll

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)

# Obtener la clave API de Cohere
CO_API_KEY = os.getenv("CO_API_KEY")
if not CO_API_KEY:
    raise ValueError("❌ ERROR: No se encontró la clave API de Cohere en las variables de entorno.")

co = cohere.Client(CO_API_KEY)

# Función para cargar ejemplos desde CSV
def load_examples_from_csv(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')  # Ajustar si hay errores en Windows
    examples = [ClassifyExample(text=row['text'], label=row['is_toxic']) for _, row in df.iterrows()]
    return examples

# Cargar ejemplos
csv_path = 'toxicity_es2.csv'
examples = load_examples_from_csv(csv_path)

# Función para clasificar texto con Cohere
def classify_text(text):
    response = co.classify(
        model='embed-multilingual-light-v3.0',
        inputs=[text],
        examples=examples,
    )
    classification_result = response.classifications[0]
    return classification_result.predictions[0], classification_result.confidences[0]

# 📌 ENDPOINT: Analizar un solo mensaje de texto
@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "❌ No se proporcionó el campo 'text'."}), 400

    input_text = data['text']
    prediction, confidence = classify_text(input_text)
    
    response_data = {
        'input': input_text,
        'predictions': prediction,
        'confidences': confidence
    }

    # Si la confianza es baja y se clasifica como tóxico, dar una respuesta neutra
    if float(confidence) <= 0.54 and prediction == "toxico":
        response_data['predictions'] = "no puedo decir"

    return jsonify(response_data)

# 📌 ENDPOINT: Analizar una conversación
@app.route('/analyze-chat', methods=['POST'])
def analyze_chat():
    data = request.get_json()
    if 'chat_id' not in data or 'messages' not in data:
        return jsonify({"error": "❌ Se requiere 'chat_id' y 'messages'."}), 400

    messages = data['messages']
    results = {}
    total_messages = 0
    total_toxic_messages = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(classify_text, msg['content']): (msg['sender'], msg) for msg in messages}

        for future in concurrent.futures.as_completed(futures):
            sender, msg = futures[future]
            try:
                prediction, confidence = future.result()
                msg.update({"prediction": prediction, "confidences": confidence})

                if sender not in results:
                    results[sender] = {"messages": [], "toxic_messages_count": 0, "total_messages_count": 0}

                results[sender]["messages"].append(msg)
                results[sender]["toxic_messages_count"] += 1 if prediction == "toxico" else 0
                results[sender]["total_messages_count"] += 1
                total_messages += 1
                total_toxic_messages += 1 if prediction == "toxico" else 0

            except Exception as e:
                logger.error(f"Error procesando mensaje: {e}")
                return jsonify({"error": f"Error en el análisis del mensaje: {str(e)}"}), 500

    # Calcular índice de toxicidad global
    global_toxicity_index = total_toxic_messages / total_messages if total_messages > 0 else 0

    return jsonify({
        "messages": results,
        "global_toxicity_index": global_toxicity_index
    })

# 📌 INICIAR SERVIDOR (Windows no necesita `host='0.0.0.0'`)
if __name__ == '__main__':
    app.run(debug=True)
