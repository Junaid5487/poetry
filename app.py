from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_poem', methods=['POST'])
def generate_poem():
    data = request.get_json()
    theme = data.get('theme')
    language = data.get('language', 'English')

    prompt = f"Write a beautiful, meaningful poem in {language} about: {theme}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=250
        )
        poem = response['choices'][0]['message']['content']
        return jsonify({'poem': poem})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
