import openai
import requests
from flask import Flask, request, jsonify

# Configurar a chave da OpenAI
openai.api_key = "SUA_API_KEY_AQUI"

# Configurar o Flask para criar o webhook
app = Flask(__name__)

# URL do webhook Make
MAKE_WEBHOOK_URL = "SUA_WEBHOOK_URL_AQUI"

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get("prompt", "Escreva um texto padrão.")
    
    try:
        # Gerar texto com a OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        text = response.choices[0].text.strip()
        
        # Enviar para o Webhook do Make
        payload = {"text": text}
        requests.post(MAKE_WEBHOOK_URL, json=payload)
        
        return jsonify({"status": "success", "generated_text": text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "Descreva uma imagem padrão.")
    
    try:
        # Gerar imagem com a OpenAI
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        
        # Enviar para o Webhook do Make
        payload = {"image_url": image_url}
        requests.post(MAKE_WEBHOOK_URL, json=payload)
        
        return jsonify({"status": "success", "image_url": image_url})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/search_web', methods=['POST'])
def search_web():
    data = request.json
    query = data.get("query", "Faça uma busca padrão.")
    
    try:
        # Fazer busca na web usando a OpenAI (ou outra API de busca)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Faça uma busca: {query}"}]
        )
        result = response['choices'][0]['message']['content'].strip()
        
        # Enviar para o Webhook do Make
        payload = {"search_result": result}
        requests.post(MAKE_WEBHOOK_URL, json=payload)
        
        return jsonify({"status": "success", "search_result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
