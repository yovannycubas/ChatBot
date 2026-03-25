import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar la API de Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY no encontrada en el archivo .env")

# Almacenamiento en memoria para la sesión de chat activa
active_session = {
    "chat": None,
    "model": None
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/configurar", methods=["POST"])
def configurar():
    """
    Recibe la instrucción de sistema y la temperatura; crea la sesión de chat.
    """
    data = request.json
    system_prompt = data.get("system_prompt", "Eres un entrenador personal certificado y nutriólogo. Preguntas primero los objetivos, nivel de condición física y equipamiento disponible del usuario. Propones rutinas detalladas con series, repeticiones y tiempos de descanso.")
    temperature = float(data.get("temperature", 0.6))

    try:
        # Configurar el modelo con la instrucción de sistema y temperatura
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt,
            generation_config={"temperature": temperature}
        )
        # Crear una nueva sesión de chat con historial vacío
        active_session["chat"] = model.start_chat(history=[])
        active_session["model"] = model
        
        return jsonify({
            "status": "success", 
            "message": "Sesión iniciada con éxito",
            "config": {"prompt_preview": system_prompt[:50] + "...", "temperature": temperature}
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """
    Recibe el mensaje del usuario y devuelve la respuesta de Gemini.
    """
    if active_session["chat"] is None:
        return jsonify({
            "status": "error", 
            "message": "No hay sesión activa. Por favor, aplica la configuración primero."
        }), 400
    
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"status": "error", "message": "El mensaje no puede estar vacío"}), 400
    
    try:
        # Enviar mensaje a la sesión activa
        response = active_session["chat"].send_message(user_message)
        return jsonify({
            "status": "success", 
            "response": response.text
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error de Gemini: {str(e)}"}), 500

@app.route("/reset", methods=["POST"])
def reset():
    """
    Elimina la sesión actual.
    """
    active_session["chat"] = None
    active_session["model"] = None
    return jsonify({"status": "success", "message": "Sesión reiniciada"})

if __name__ == "__main__":
    # Asegurarse de que el puerto sea el estándar de Flask (5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
