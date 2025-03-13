import os
import logging
import concurrent.futures
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import cohere
from cohere import ClassifyExample
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import copy

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)

# Inicializar Cohere
CO_API_KEY = os.getenv("CO_API_KEY")
if not CO_API_KEY:
    raise ValueError("❌ ERROR: No se encontró la clave API de Cohere en las variables de entorno.")

co = cohere.Client(CO_API_KEY)

# Inicializar AWS Translate
translate_client = boto3.client(
    'translate',
    region_name=os.getenv('AWS_REGION', 'eu-east-2')
)

# Función para cargar ejemplos desde CSV
def load_examples_from_csv(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')
    return [ClassifyExample(text=row['text'], label=row['is_toxic']) for _, row in df.iterrows()]

# Cargar ejemplos
csv_path = 'toxicity_es2.csv'
examples = load_examples_from_csv(csv_path)

# Función para clasificar texto con Cohere
def classify_text(text):
    try:
        response = co.classify(
            model='embed-multilingual-light-v3.0',
            inputs=[text],
            examples=examples,
        )
        classification_result = response.classifications[0]
        return classification_result.predictions[0], classification_result.confidences[0]
    except Exception as e:
        logger.error(f"Error en clasificación de texto: {e}")
        return "error", 0.0

# Función para resumir texto
def summarize_text(text):
    if len(text) < 250:
        return "Texto demasiado corto para resumir. Se requieren al menos 250 caracteres."

    query = f"Genera un resumen conciso de este chat:\n{text}"
    response = co.chat(
        model="command-r-plus-08-2024",
        message=query
    )
    return response.text

# Función para traducir texto
def translate_text(text, target_language="es"):
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
    except (BotoCoreError, ClientError) as error:
        logger.error(f"Error en traducción: {error}")
        return None

# 📌 **ENDPOINT: Analizar un solo mensaje de texto**
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

# 📌 **ENDPOINT: Analizar una conversación**
@app.route('/analyze-chat', methods=['POST'])
def analyze_chat():
    data = request.get_json()
    if 'chat_id' not in data or 'messages' not in data:
        return jsonify({"error": "❌ Se requiere 'chat_id' y 'messages'."}), 400

    messages = data['messages']
    results = {}
    total_messages = 0
    total_toxic_messages = 0
    all_content = ""

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(classify_text, msg['content']): (msg['sender'], msg) for msg in messages}

        for future in concurrent.futures.as_completed(futures):
            sender, msg = futures[future]
            prediction, confidence = future.result()
            msg.update({"prediction": prediction, "confidences": confidence})

            if sender not in results:
                results[sender] = {"messages": [], "toxic_messages_count": 0, "total_messages_count": 0}

            results[sender]["messages"].append(msg)
            results[sender]["toxic_messages_count"] += 1 if prediction == "toxico" else 0
            results[sender]["total_messages_count"] += 1
            total_messages += 1
            total_toxic_messages += 1 if prediction == "toxico" else 0
            all_content += msg['content'] + " "

    global_summary = summarize_text(all_content)

    return jsonify({
        "messages": results,
        "global_summary": global_summary
    })

# 📌 **ENDPOINT: Traducir respuestas**
@app.route('/translate-response', methods=['POST'])
def translate_response():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided."}), 400

    try:
        translated_data = copy.deepcopy(data)

        if 'global_summary' in translated_data:
            translated_data['global_summary'] = translate_text(translated_data['global_summary']) or translated_data['global_summary']

        if 'messages' in translated_data:
            for sender, sender_data in translated_data['messages'].items():
                if 'summary' in sender_data:
                    sender_data['summary'] = translate_text(sender_data['summary']) or sender_data['summary']

                for msg in sender_data['messages']:
                    if 'content' in msg:
                        msg['content'] = translate_text(msg['content']) or msg['content']

        return jsonify(translated_data), 200
    except Exception as e:
        logger.error(f"Error en traducción de respuesta: {e}")
        return jsonify({"error": "Error al traducir la respuesta."}), 500

# 📌 **INICIAR SERVIDOR**
if __name__ == '__main__':
    app.run(debug=True)
