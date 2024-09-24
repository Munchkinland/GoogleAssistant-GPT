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
        # Llamar a la API de OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",  # Puedes usar otro modelo si lo deseas
            prompt=user_query,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )

        gpt_response = response.choices[0].text.strip()

        return jsonify({
            "fulfillmentText": gpt_response
        })
    except Exception as e:
        return jsonify({
            "fulfillmentText": "Lo siento, hubo un error al procesar tu solicitud."
        })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
