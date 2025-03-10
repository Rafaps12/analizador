# from flask import Flask, request, jsonify
# import cohere
# import pandas as pd
# from cohere.responses.classify import Example
# # Load .env file using:
# from dotenv import load_dotenv
# load_dotenv()

# import os
# # CO_API_KEY = os.getenv("CO_API_KEY")
# # print(CO_API_KEY)

# app = Flask(__name__)

# # Initialize the Cohere client with your API key
# # co = cohere.Client('<<apiKey>>')
# co = cohere.Client(os.getenv("CO_API_KEY")) # This is your trial API key

# # # Read the CSV file to populate the examples for classification
# # def load_examples_from_csv(csv_path):
# #     df = pd.read_csv(csv_path)
# #     examples = []
# #     for index, row in df.iterrows():
# #         examples.append(Example(
# #             text=row['text'],
# #             label=row['is_toxic']
# #         ))
# #     return examples

# def load_examples_from_csv(csv_path):
#     df = pd.read_csv(csv_path, encoding='ISO-8859-1')  # or try 'latin1' or 'windows-1252' if ISO-8859-1 doesn't work
#     examples = []
#     for index, row in df.iterrows():
#         examples.append(Example(
#             text=row['text'],
#             label=row['is_toxic']
#         ))
#     return examples

# csv_path = 'toxicity_es2.csv'
# examples = load_examples_from_csv(csv_path)
# # print(examples)

# @app.route('/analyze-sentiment', methods=['POST'])
# def analyze_sentiment():
#     data = request.get_json()
    
#     # Check if 'text' is in the provided JSON data
#     if 'text' not in data:
#         return jsonify({"error": "No text field provided. Please specify a 'text' key."}), 400

#     input_text = data['text']
    
#     # Classify the input text using Cohere's classify endpoint
#     response = co.classify(
#         model='embed-multilingual-light-v3.0', # replace with your chosen model
#         inputs=[input_text],
#         examples=examples,
#     )

#     # Process the response to return a JSON object with the classification
#     classification_result = response.classifications[0]

#     input = classification_result.input
#     prediction = classification_result.predictions[0]
#     confidence = classification_result.confidences[0]
#     low_confidence = 0.54

#     if float(confidence) <= low_confidence and prediction == "toxico":
#         return jsonify({
#         'input': input,
#         'predictions': "no puedo decir",
#         'confidences': confidence
#     })

#     return jsonify({
#         'input': input,
#         'predictions': prediction,
#         'confidences': confidence
#     })

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, jsonify
# import cohere
# import pandas as pd
# from cohere.responses.classify import Example
# from dotenv import load_dotenv
# import os
# import concurrent.futures

# load_dotenv()

# app = Flask(__name__)

# co = cohere.Client(os.getenv("CO_API_KEY"))

# def load_examples_from_csv(csv_path):
#     df = pd.read_csv(csv_path, encoding='ISO-8859-1')
#     examples = []
#     for index, row in df.iterrows():
#         examples.append(Example(
#             text=row['text'],
#             label=row['is_toxic']
#         ))
#     return examples

# csv_path = 'toxicity_es2.csv'
# examples = load_examples_from_csv(csv_path)

# def classify_text(text):
#     response = co.classify(
#         model='embed-multilingual-light-v3.0',
#         inputs=[text],
#         examples=examples,
#     )
#     classification_result = response.classifications[0]
#     prediction = classification_result.predictions[0]
#     confidence = classification_result.confidences[0]
#     return prediction, confidence

# @app.route('/analyze-sentiment', methods=['POST'])
# def analyze_sentiment():
#     data = request.get_json()
#     if 'text' not in data:
#         return jsonify({"error": "No text field provided. Please specify a 'text' key."}), 400

#     input_text = data['text']
#     prediction, confidence = classify_text(input_text)
#     low_confidence = 0.54

#     if float(confidence) <= low_confidence and prediction == "toxico":
#         return jsonify({
#             'input': input_text,
#             'predictions': "no puedo decir",
#             'confidences': confidence
#         })

#     return jsonify({
#         'input': input_text,
#         'predictions': prediction,
#         'confidences': confidence
#     })

# @app.route('/analyze-chat', methods=['POST'])
# def analyze_chat():
#     data = request.get_json()

#     if 'chat_id' not in data or 'messages' not in data:
#         return jsonify({"error": "Invalid request format. Please specify 'chat_id' and 'messages' keys."}), 400

#     messages = data['messages']
#     senders = {}
#     for message in messages:
#         sender = message['sender']
#         if sender not in senders:
#             senders[sender] = []
#         senders[sender].append(message)

#     results = {}
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = {executor.submit(classify_text, msg['content']): (sender, msg) for sender in senders for msg in senders[sender]}
#         for future in concurrent.futures.as_completed(futures):
#             sender, msg = futures[future]
#             prediction, confidence = future.result()
#             toxicity_score = 0.0 if prediction == "no es toxico" else 1.0
#             msg.update({
#                 "prediction": prediction,
#                 "confidences": confidence
#             })
#             if sender not in results:
#                 results[sender] = {
#                     "messages": [],
#                     "toxic_messages_count": 0
#                 }
#             results[sender]["messages"].append(msg)
#             results[sender]["toxic_messages_count"] += 1 if prediction == "toxico" else 0

#     return jsonify({"messages": results})

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, jsonify
# import cohere
# import pandas as pd
# from cohere.responses.classify import Example
# from dotenv import load_dotenv
# import os
# import concurrent.futures

# load_dotenv()

# app = Flask(__name__)

# co = cohere.Client(os.getenv("CO_API_KEY"))

# def load_examples_from_csv(csv_path):
#     df = pd.read_csv(csv_path, encoding='ISO-8859-1')
#     examples = []
#     for index, row in df.iterrows():
#         examples.append(Example(
#             text=row['text'],
#             label=row['is_toxic']
#         ))
#     return examples

# csv_path = 'toxicity_es2.csv'
# examples = load_examples_from_csv(csv_path)

# def classify_text(text):
#     response = co.classify(
#         model='embed-multilingual-light-v3.0',
#         inputs=[text],
#         examples=examples,
#     )
#     classification_result = response.classifications[0]
#     prediction = classification_result.predictions[0]
#     confidence = classification_result.confidences[0]
#     return prediction, confidence


# def summarize_text(text):
#     if len(text) < 250:
#         return "Text too short to summarize. Minimum 250 characters required."

#     response = co.summarize(
#         model='summarize-xlarge',
#         text=text,
#         length='short',
#         additional_command='', 
#         temperature=0.3
#     )
#     summary = response.summary
#     return summary

# @app.route('/analyze-sentiment', methods=['POST'])
# def analyze_sentiment():
#     data = request.get_json()
#     if 'text' not in data:
#         return jsonify({"error": "No text field provided. Please specify a 'text' key."}), 400

#     input_text = data['text']
#     prediction, confidence = classify_text(input_text)
#     low_confidence = 0.54

#     if float(confidence) <= low_confidence and prediction == "toxico":
#         return jsonify({
#             'input': input_text,
#             'predictions': "no puedo decir",
#             'confidences': confidence
#         })

#     return jsonify({
#         'input': input_text,
#         'predictions': prediction,
#         'confidences': confidence
#     })

# # @app.route('/analyze-chat', methods=['POST'])
# # def analyze_chat():
# #     data = request.get_json()

# #     if 'chat_id' not in data or 'messages' not in data:
# #         return jsonify({"error": "Invalid request format. Please specify 'chat_id' and 'messages' keys."}), 400

# #     messages = data['messages']
# #     senders = {}
# #     for message in messages:
# #         sender = message['sender']
# #         if sender not in senders:
# #             senders[sender] = []
# #         senders[sender].append(message)

# #     results = {}
# #     total_messages = 0
# #     total_toxic_messages = 0
# #     all_content = "" # To store all the messages for global summary
# #     with concurrent.futures.ThreadPoolExecutor() as executor:
# #         futures = {executor.submit(classify_text, msg['content']): (sender, msg) for sender in senders for msg in senders[sender]}
# #         for future in concurrent.futures.as_completed(futures):
# #             sender, msg = futures[future]
# #             prediction, confidence = future.result()
# #             msg.update({
# #                 "prediction": prediction,
# #                 "confidences": confidence
# #             })
# #             if sender not in results:
# #                 results[sender] = {
# #                     "messages": [],
# #                     "toxic_messages_count": 0,
# #                     "total_messages_count": 0
# #                 }
# #             results[sender]["messages"].append(msg)
# #             results[sender]["toxic_messages_count"] += 1 if prediction == "toxico" else 0
# #             results[sender]["total_messages_count"] += 1
# #             total_messages += 1
# #             total_toxic_messages += 1 if prediction == "toxico" else 0
# #             all_content += msg['content'] + " " # Add message content to all_content

# #     # Compile messages and add summaries
# #     for sender, data in results.items():
# #         all_messages_content = " ".join([msg['content'] for msg in data['messages']])
# #         summary = summarize_text(all_messages_content)
# #         data['summary'] = summary
# #         sender_toxicity = "toxico" if data['toxic_messages_count'] / data['total_messages_count'] > 0.2 else "no toxico"
# #         data['overall_toxicity'] = sender_toxicity

# #     # Global toxicity summary using the summarizer model
# #     global_summary = summarize_text(all_content)
    
# #     return jsonify({"messages": results, "global_summary": global_summary})
# @app.route('/analyze-chat', methods=['POST'])
# def analyze_chat():
#     data = request.get_json()

#     if 'chat_id' not in data or 'messages' not in data:
#         return jsonify({"error": "Invalid request format. Please specify 'chat_id' and 'messages' keys."}), 400

#     messages = data['messages']
#     senders = {}
#     for message in messages:
#         sender = message['sender']
#         if sender not in senders:
#             senders[sender] = []
#         senders[sender].append(message)

#     results = {}
#     total_messages = 0
#     total_toxic_messages = 0
#     all_content = ""  # To store all the messages for global summary
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = {executor.submit(classify_text, msg['content']): (sender, msg) for sender in senders for msg in senders[sender]}
#         for future in concurrent.futures.as_completed(futures):
#             sender, msg = futures[future]
#             prediction, confidence = future.result()
#             msg.update({
#                 "prediction": prediction,
#                 "confidences": confidence
#             })
#             if sender not in results:
#                 results[sender] = {
#                     "messages": [],
#                     "toxic_messages_count": 0,
#                     "total_messages_count": 0
#                 }
#             results[sender]["messages"].append(msg)
#             results[sender]["toxic_messages_count"] += 1 if prediction == "toxico" else 0
#             results[sender]["total_messages_count"] += 1
#             total_messages += 1
#             total_toxic_messages += 1 if prediction == "toxico" else 0
#             all_content += msg['content'] + " "  # Add message content to all_content

#     # Compile messages and add summaries
#     for sender, data in results.items():
#         sender_messages_content = " ".join([msg['content'] for msg in data["messages"]])
#         summary = summarize_text(sender_messages_content)
#         data["summary"] = summary
#         sender_toxicity = "toxico" if data["toxic_messages_count"] / data["total_messages_count"] > 0.2 else "no toxico"
#         data["overall_toxicity"] = sender_toxicity

#     # Global toxicity summary using the summarizer model
#     global_summary = summarize_text(all_content)

#     return jsonify({"messages": results, "global_summary": global_summary})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)


# # app.py
# from flask import Flask, request, jsonify
# import cohere
# import pandas as pd
# from cohere.responses.classify import Example
# from dotenv import load_dotenv
# import os
# import concurrent.futures
# import boto3
# from botocore.exceptions import BotoCoreError, ClientError

# load_dotenv()

# app = Flask(__name__)

# # Initialize Cohere client
# co = cohere.Client(os.getenv("CO_API_KEY"))

# # Initialize AWS Translate client
# translate_client = boto3.client('translate',
#                                 region_name=os.getenv('AWS_REGION', 'eu-west-2'))  # Default region if not set

# def load_examples_from_csv(csv_path):
#     df = pd.read_csv(csv_path, encoding='ISO-8859-1')
#     examples = []
#     for index, row in df.iterrows():
#         examples.append(Example(
#             text=row['text'],
#             label=row['is_toxic']
#         ))
#     return examples

# csv_path = 'toxicity_es2.csv'
# examples = load_examples_from_csv(csv_path)

# def classify_text(text):
#     response = co.classify(
#         model='embed-multilingual-light-v3.0',
#         inputs=[text],
#         examples=examples,
#     )
#     classification_result = response.classifications[0]
#     prediction = classification_result.predictions[0]
#     confidence = classification_result.confidences[0]
#     return prediction, confidence

# def summarize_text(text):
#     if len(text) < 250:
#         return "Text too short to summarize. Minimum 250 characters required."

#     response = co.summarize(
#         model='summarize-xlarge',
#         text=text,
#         length='short',
#         additional_command='', 
#         temperature=0.3
#     )
#     summary = response.summary
#     return summary

# @app.route('/analyze-sentiment', methods=['POST'])
# def analyze_sentiment():
#     data = request.get_json()
#     if 'text' not in data:
#         return jsonify({"error": "No text field provided. Please specify a 'text' key."}), 400

#     input_text = data['text']
#     prediction, confidence = classify_text(input_text)
#     low_confidence = 0.54

#     if float(confidence) <= low_confidence and prediction == "toxico":
#         return jsonify({
#             'input': input_text,
#             'predictions': "no puedo decir",
#             'confidences': confidence
#         })

#     return jsonify({
#         'input': input_text,
#         'predictions': prediction,
#         'confidences': confidence
#     })

# @app.route('/analyze-chat', methods=['POST'])
# def analyze_chat():
#     data = request.get_json()

#     if 'chat_id' not in data or 'messages' not in data:
#         return jsonify({"error": "Invalid request format. Please specify 'chat_id' and 'messages' keys."}), 400

#     messages = data['messages']
#     senders = {}
#     for message in messages:
#         sender = message['sender']
#         if sender not in senders:
#             senders[sender] = []
#         senders[sender].append(message)

#     results = {}
#     total_messages = 0
#     total_toxic_messages = 0
#     all_content = ""  # To store all the messages for global summary
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = {executor.submit(classify_text, msg['content']): (sender, msg) for sender in senders for msg in senders[sender]}
#         for future in concurrent.futures.as_completed(futures):
#             sender, msg = futures[future]
#             try:
#                 prediction, confidence = future.result()
#             except Exception as e:
#                 return jsonify({"error": f"Error processing message: {str(e)}"}), 500
#             msg.update({
#                 "prediction": prediction,
#                 "confidences": confidence
#             })
#             if sender not in results:
#                 results[sender] = {
#                     "messages": [],
#                     "toxic_messages_count": 0,
#                     "total_messages_count": 0
#                 }
#             results[sender]["messages"].append(msg)
#             results[sender]["toxic_messages_count"] += 1 if prediction == "toxico" else 0
#             results[sender]["total_messages_count"] += 1
#             total_messages += 1
#             total_toxic_messages += 1 if prediction == "toxico" else 0
#             all_content += msg['content'] + " "  # Add message content to all_content

#     # Compile messages and add summaries
#     for sender, data in results.items():
#         sender_messages_content = " ".join([msg['content'] for msg in data["messages"]])
#         summary = summarize_text(sender_messages_content)
#         data["summary"] = summary
#         sender_toxicity = "toxico" if data["toxic_messages_count"] / data["total_messages_count"] > 0.2 else "no toxico"
#         data["overall_toxicity"] = sender_toxicity

#     # Global toxicity summary using the summarizer model
#     global_summary = summarize_text(all_content)

#     return jsonify({"messages": results, "global_summary": global_summary})

# def translate_text(text, target_language="es"):
#     try:
#         response = translate_client.translate_text(
#             Text=text,
#             SourceLanguageCode="auto",
#             TargetLanguageCode=target_language
#         )
#         return response['TranslatedText']
#     except (BotoCoreError, ClientError) as error:
#         app.logger.error(f"Translation error: {error}")
#         return None

# @app.route('/translate-response', methods=['POST'])
# def translate_response():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No JSON data provided."}), 400

#     translated_data = data.copy()

#     # Translate global_summary if it exists
#     if 'global_summary' in translated_data and translated_data['global_summary']:
#         translated_text = translate_text(translated_data['global_summary'])
#         if translated_text:
#             translated_data['global_summary'] = translated_text
#         else:
#             return jsonify({"error": "Failed to translate global_summary."}), 500

#     # Translate summaries and message contents for each sender
#     if 'messages' in translated_data:
#         for sender, sender_data in translated_data['messages'].items():
#             # Translate sender's summary
#             if 'summary' in sender_data and sender_data['summary']:
#                 translated_summary = translate_text(sender_data['summary'])
#                 if translated_summary:
#                     sender_data['summary'] = translated_summary
#                 else:
#                     return jsonify({"error": f"Failed to translate summary for sender {sender}."}), 500

#             # Translate each message's content
#             if 'messages' in sender_data:
#                 for msg in sender_data['messages']:
#                     if 'content' in msg and msg['content']:
#                         translated_content = translate_text(msg['content'])
#                         if translated_content:
#                             msg['content'] = translated_content
#                         else:
#                             return jsonify({"error": f"Failed to translate message content for sender {sender}."}), 500

#     return jsonify(translated_data)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)


# app.py
from flask import Flask, request, jsonify
import cohere
import pandas as pd
# from cohere.responses.classify import Example
from cohere import ClassifyExample
from dotenv import load_dotenv
import os
import concurrent.futures
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import copy
import logging

load_dotenv()

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cohere client
co = cohere.Client(os.getenv("CO_API_KEY"))

# Initialize AWS Translate client
translate_client = boto3.client(
    'translate',
    region_name=os.getenv('AWS_REGION', 'eu-east-2')  # Default region if not set
)


def load_examples_from_csv(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')
    examples = []
    for index, row in df.iterrows():
        examples.append(ClassifyExample(
            text=row['text'],
            label=row['is_toxic']
        ))
    return examples


csv_path = 'toxicity_es2.csv'
examples = load_examples_from_csv(csv_path)


def classify_text(text):
    response = co.classify(
        model='embed-multilingual-light-v3.0',
        inputs=[text],
        examples=examples,
    )
    classification_result = response.classifications[0]
    prediction = classification_result.predictions[0]
    confidence = classification_result.confidences[0]
    return prediction, confidence


def summarize_text(text):
    # if len(text) < 250:
    #     return "Text too short to summarize. Minimum 250 characters required."

    # response = co.summarize(
    #     model='summarize-xlarge',
    #     text=text,
    #     length='short',
    #     additional_command='',
    #     temperature=0.3
    # )

    query = f"Generate a concise summary of this text of this chat\n{text}"
    response = co.chat(
        # model="command-r-plus-08-2024",
        # messages=[{"role": "user", "content": message}]
        model="command-r-plus-08-2024",
        message=query
        
    )
    # summary = response.message.content[0].text
    summary = response.text
    return summary


def translate_text(text, target_language="es"):
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
    except (BotoCoreError, ClientError) as error:
        logger.error(f"Translation error: {error}")
        return None

def analyze_chat_internal(payload):
    """
    Analyze the chat data by classifying messages and summarizing per sender and globally.
    
    The summaries are structured in a chat-like format (e.g., "Sender: message") to help
    the summarizer model understand the conversation context.
    """
    chat_id = payload.get('chat_id')
    messages = payload.get('messages', [])

    if not isinstance(messages, list):
        raise ValueError("'messages' should be a list of message objects.")

    senders = {}
    results = {}
    total_messages = 0
    total_toxic_messages = 0
    all_content_lines = []  # To store all messages in "Sender: message" format for global summary

    # Prepare data per sender
    for message in messages:
        sender = message.get('sender')
        content = message.get('content', "").strip()
        if not sender or not content:
            continue  # Skip messages without a sender or content

        if sender not in senders:
            senders[sender] = []
        senders[sender].append(message)

    # Analyze messages concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a future for each message classification
        futures = {
            executor.submit(classify_text, msg['content']): (sender, msg)
            for sender, msgs in senders.items()
            for msg in msgs
        }

        for future in concurrent.futures.as_completed(futures):
            sender, msg = futures[future]
            try:
                prediction, confidence = future.result()
            except Exception as e:
                logger.error(f"Error classifying text: {e}")
                prediction, confidence = "error", 0.0

            # Update the message with classification results
            msg.update({
                "prediction": prediction,
                "confidences": confidence
            })

            # Initialize sender's data in results if not already present
            if sender not in results:
                results[sender] = {
                    "messages": [],
                    "toxic_messages_count": 0,
                    "total_messages_count": 0
                }

            # Append the message to the sender's list
            results[sender]["messages"].append(msg)
            # Update toxicity counts
            if prediction == "toxico":
                results[sender]["toxic_messages_count"] += 1
                total_toxic_messages += 1
            results[sender]["total_messages_count"] += 1
            total_messages += 1
            # Append to global content with "Sender: message" format
            all_content_lines.append(f"{sender}: {msg['content']}")

    # Compile summaries for each sender
    for sender, data in results.items():
        # Create a chat-like string for the sender's messages
        sender_content_lines = [
            f"{msg['sender']}: {msg['content']}" for msg in data["messages"]
        ]
        sender_messages_content = "\n".join(sender_content_lines)
        # Generate summary using the chat-like structure
        summary = summarize_text(sender_messages_content)
        data["summary"] = summary
        # Determine overall toxicity based on threshold (e.g., 20%)
        toxicity_ratio = data["toxic_messages_count"] / data["total_messages_count"]
        sender_toxicity = "toxico" if toxicity_ratio > 0.2 else "no toxico"
        data["overall_toxicity"] = sender_toxicity

    # Generate global summary using the chat-like structure
    all_content = "\n".join(all_content_lines)
    global_summary = summarize_text(all_content)

    analyzed_data = {
        "chat_id": chat_id,
        "global_summary": global_summary,
        "messages": results,
        "total_messages": total_messages,
        "total_toxic_messages": total_toxic_messages
    }

    return analyzed_data
# def analyze_chat_internal(payload):
#     """
#     Analyze the chat data by classifying messages and summarizing per sender and globally.
#     """
#     chat_id = payload.get('chat_id')
#     messages = payload.get('messages', [])

#     if not isinstance(messages, list):
#         raise ValueError("'messages' should be a list of message objects.")

#     senders = {}
#     results = {}
#     total_messages = 0
#     total_toxic_messages = 0
#     all_content = ""  # To store all the messages for global summary

#     # Prepare data per sender
#     for message in messages:
#         sender = message.get('sender')
#         if not sender:
#             continue  # Skip messages without a sender

#         if sender not in senders:
#             senders[sender] = []
#         senders[sender].append(message)

#     # Analyze messages concurrently
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = {
#             executor.submit(classify_text, msg['content']): (sender, msg)
#             for sender in senders
#             for msg in senders[sender]
#         }
#         for future in concurrent.futures.as_completed(futures):
#             sender, msg = futures[future]
#             try:
#                 prediction, confidence = future.result()
#             except Exception as e:
#                 logger.error(f"Error classifying text: {e}")
#                 prediction, confidence = "error", 0.0

#             msg.update({
#                 "prediction": prediction,
#                 "confidences": confidence
#             })

#             if sender not in results:
#                 results[sender] = {
#                     "messages": [],
#                     "toxic_messages_count": 0,
#                     "total_messages_count": 0
#                 }

#             results[sender]["messages"].append(msg)
#             results[sender]["toxic_messages_count"] += 1 if prediction == "toxico" else 0
#             results[sender]["total_messages_count"] += 1
#             total_messages += 1
#             total_toxic_messages += 1 if prediction == "toxico" else 0
#             all_content += msg['content'] + " "

#     # Compile summaries
#     for sender, data in results.items():
#         sender_messages_content = " ".join([msg['content'] for msg in data["messages"]])
#         summary = summarize_text(sender_messages_content)
#         data["summary"] = summary
#         sender_toxicity = "toxico" if data["toxic_messages_count"] / data["total_messages_count"] > 0.2 else "no toxico"
#         data["overall_toxicity"] = sender_toxicity

#     # Global toxicity summary using the summarizer model
#     global_summary = summarize_text(all_content)

#     analyzed_data = {
#         "chat_id": chat_id,
#         "global_summary": global_summary,
#         "messages": results
#     }

#     return analyzed_data


def translate_data_internal(data):
    """
    Translate the analyzed data into Spanish.
    """
    translated_data = copy.deepcopy(data)

    # Translate global_summary if it exists
    if 'global_summary' in translated_data and translated_data['global_summary']:
        translated_text = translate_text(translated_data['global_summary'])
        if translated_text:
            translated_data['global_summary'] = translated_text
        else:
            raise RuntimeError("Failed to translate 'global_summary'.")

    # Translate summaries and message contents for each sender
    if 'messages' in translated_data:
        for sender, sender_data in translated_data['messages'].items():
            # Translate sender's summary
            if 'summary' in sender_data and sender_data['summary']:
                translated_summary = translate_text(sender_data['summary'])
                if translated_summary:
                    sender_data['summary'] = translated_summary
                else:
                    raise RuntimeError(f"Failed to translate summary for sender {sender}.")

            # Translate each message's content
            if 'messages' in sender_data:
                for msg in sender_data['messages']:
                    if 'content' in msg and msg['content']:
                        translated_content = translate_text(msg['content'])
                        if translated_content:
                            msg['content'] = translated_content
                        else:
                            raise RuntimeError(f"Failed to translate message content for sender {sender}.")

    return translated_data


@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "No text field provided. Please specify a 'text' key."}), 400

    input_text = data['text']
    prediction, confidence = classify_text(input_text)
    low_confidence = 0.54

    if float(confidence) <= low_confidence and prediction == "toxico":
        return jsonify({
            'input': input_text,
            'predictions': "no puedo decir",
            'confidences': confidence
        })

    return jsonify({
        'input': input_text,
        'predictions': prediction,
        'confidences': confidence
    })


@app.route('/analyze-chat', methods=['POST'])
def analyze_chat():
    data = request.get_json()

    if 'chat_id' not in data or 'messages' not in data:
        return jsonify({"error": "Invalid request format. Please specify 'chat_id' and 'messages' keys."}), 400

    try:
        analyzed_data = analyze_chat_internal(data)
        return jsonify(analyzed_data), 200
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error analyzing chat: {e}")
        return jsonify({"error": "An error occurred while analyzing the chat."}), 500


@app.route('/translate-response', methods=['POST'])
def translate_response():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided."}), 400

    try:
        translated_data = translate_data_internal(data)
        return jsonify(translated_data), 200
    except RuntimeError as re:
        logger.error(f"RuntimeError: {re}")
        return jsonify({"error": str(re)}), 500
    except Exception as e:
        logger.error(f"Error translating response: {e}")
        return jsonify({"error": "An error occurred while translating the response."}), 500


@app.route('/analyze-and-translate-chat', methods=['POST'])
def analyze_and_translate_chat():
    data = request.get_json()
    if 'chat_id' not in data or 'messages' not in data:
        return jsonify({"error": "Invalid request format. Please specify 'chat_id' and 'messages' keys."}), 400

    try:
        # Step 1: Analyze the chat
        analyzed_data = analyze_chat_internal(data)

        # Step 2: Translate the analyzed data
        translated_data = translate_data_internal(analyzed_data)

        return jsonify(translated_data), 200

    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except RuntimeError as re:
        logger.error(f"RuntimeError: {re}")
        return jsonify({"error": str(re)}), 500
    except Exception as e:
        logger.error(f"Error in analyze_and_translate_chat: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@app.route('/analyze-and-translate-sample', methods=['GET'])
def analyze_and_translate_sample():
    """
    Optional: A sample endpoint to demonstrate the combined analysis and translation.
    Useful for testing purposes.
    """
    sample_payload = {
        "chat_id": 853920461278430,
        "messages": [
        {
        "sender": "john",
        "content": "Hey Lisa, did you check the new project brief?",
        "timestamp": "2023-10-20T11:00:00Z"
        },
        {
        "sender": "lisa",
        "content": "Yeah, I did. Looks like a lot of work.",
        "timestamp": "2023-10-20T11:01:00Z"
        },
        {
        "sender": "john",
        "content": "Stop complaining, just do your job.",
        "timestamp": "2023-10-20T11:02:00Z"
        },
        {
        "sender": "lisa",
        "content": "That's pretty rude, John.",
        "timestamp": "2023-10-20T11:03:00Z"
        },
        {
        "sender": "john",
        "content": "Oh, please. Toughen up.",
        "timestamp": "2023-10-20T11:04:00Z"
        },
        {
        "sender": "lisa",
        "content": "I'm reporting this to HR.",
        "timestamp": "2023-10-20T11:05:00Z"
        },
        {
        "sender": "john",
        "content": "Do whatever you want. Like I care. Idiot",
        "timestamp": "2023-10-20T11:06:00Z"
        },
        {
        "sender": "lisa",
        "content": "This is unacceptable behavior.",
        "timestamp": "2023-10-20T11:07:00Z"
        },
        {
        "sender": "john",
        "content": "By the way, do you have the updated financials for the last quarter? We need to present them in the meeting tomorrow. Also, make sure to include the new projections for the upcoming quarter. We need everything to be accurate and up-to-date. Thanks.",
        "timestamp": "2023-10-20T11:08:00Z"
        },
        {
        "sender": "lisa",
        "content": "Sure, I will get them ready by EOD. But John, you really need to change your attitude. It's not OK to talk to your colleagues this way. We all have a lot on our plates, and mutual respect is key to a productive work environment.",
        "timestamp": "2023-10-20T11:09:00Z"
        },
        {
        "sender": "john",
        "content": "I understand, Lisa. But sometimes, deadlines are tight, and we don’t have time for complaints. Let’s just focus on getting the job done. We can talk about this in the team meeting.",
        "timestamp": "2023-10-20T11:10:00Z"
        },
        {
        "sender": "lisa",
        "content": "Alright, I'll see you at the meeting. But seriously, John, consider how you come across. It’s one thing to push for results and another to be disrespectful.",
        "timestamp": "2023-10-20T11:11:00Z"
        },
        {
        "sender": "john",
        "content": "Noted, Lisa. I’ll try to work on it. Let’s just make sure we’re all on the same page for tomorrow’s presentation. We can’t afford any slip-ups.",
        "timestamp": "2023-10-20T11:12:00Z"
        },
        {
        "sender": "lisa",
        "content": "Got it. I'll double-check everything and ensure it’s smooth. By the way, have you received the feedback from our recent campaign? We need to incorporate it into our next strategy session.",
        "timestamp": "2023-10-20T11:13:00Z"
        },
        {
        "sender": "john",
        "content": "Yes, I have. I'll share it with you before the end of the day. Let's regroup at 4 PM to go over it. We should be prepared for any questions from the higher-ups.",
        "timestamp": "2023-10-20T11:14:00Z"
        },
        {
        "sender": "lisa",
        "content": "Perfect. I'll see you at 4 PM then. Thanks, John.",
        "timestamp": "2023-10-20T11:15:00Z"
        },
        {
        "sender": "john",
        "content": "Thank you, Lisa. See you soon.",
        "timestamp": "2023-10-20T11:16:00Z"
        }
        ]
    }

    try:
        analyzed_data = analyze_chat_internal(sample_payload)
        translated_data = translate_data_internal(analyzed_data)
        return jsonify(translated_data), 200
    except Exception as e:
        logger.error(f"Error in sample endpoint: {e}")
        return jsonify({"error": "Failed to process sample data."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)