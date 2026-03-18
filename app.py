from flask import Flask, request, jsonify
from openai import OpenAI
import json
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    with open("memoria.json", "r") as f:
        memoria = json.load(f)
except:
    memoria = []

def guardar_memoria():
    with open("memoria.json", "w") as f:
        json.dump(memoria, f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("mensaje", "")

    if "recuerda" in user_input.lower():
        memoria.append(user_input)
        guardar_memoria()
        return jsonify({"respuesta": "Lo guardaré."})

    if "mis tareas" in user_input.lower():
        return jsonify({"respuesta": memoria})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente personal útil y organizado."},
            {"role": "user", "content": user_input}
        ]
    )

    return jsonify({"respuesta": response.choices[0].message.content})

app.run(host="0.0.0.0", port=3000)
