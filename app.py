from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configura tu clave de API de OpenAI desde una variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)

    # Extraer la consulta del usuario
    user_query = req.get('queryResult').get('queryText')

    try:
        # Llamar a la API de OpenAI usando GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo GPT-3.5 Turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ],
            max_tokens=150,
            temperature=0.7
        )

        gpt_response = response['choices'][0]['message']['content'].strip()

        return jsonify({
            "fulfillmentText": gpt_response
        })
    except Exception as e:
        return jsonify({
            "fulfillmentText": "Lo siento, hubo un error al procesar tu solicitud."
        })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
