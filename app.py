import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar el cliente de Google GenAI usando el nuevo SDK (V1+)
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key:
    try:
        # Usar el SDK oficial actualizado
        client = genai.Client(api_key=api_key)
        print("INFO: Cliente de Google GenAI configurado correctamente.")
    except Exception as e:
        print(f"ERROR: No se pudo configurar el cliente: {str(e)}")
else:
    print("WARNING: GEMINI_API_KEY no encontrada en el archivo .env")

# Almacenamiento en memoria para la sesión activa de chat (usando un diccionario global)
active_chat_session = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/configurar", methods=["POST"])
def configurar():
    """
    Inicializa una nueva sesión de chat con el nuevo SDK.
    """
    global active_chat_session, client
    
    if client is None:
        return jsonify({"status": "error", "message": "API Key no configurada o cliente no iniciado."}), 500
        
    data = request.json
    system_prompt = data.get("system_prompt", "Eres un barman cyberpunk.")
    temperature = float(data.get("temperature", 0.7))

    try:
        # En el nuevo SDK genai, creamos el chat directamente con la configuración inicial
        # El modelo estable 'gemini-1.5-flash' es el más recomendado para cuotas gratuitas.
        active_chat_session = client.chats.create(
            model="gemini-1.5-flash",
            config={
                'system_instruction': system_prompt,
                'temperature': temperature,
            }
        )
        
        return jsonify({
            "status": "success", 
            "message": "Sesión iniciada correctamente con el nuevo motor genai",
            "config": {"model": "gemini-1.5-flash", "temperature": temperature}
        })
    except Exception as e:
        error_msg = str(e)
        # Manejo simple para errores comunes
        if "404" in error_msg:
            error_msg = "Error 404: No se encontró el modelo. Verifica que tu API Key sea vigente y el modelo exista."
        elif "429" in error_msg:
            error_msg = "Error 429: Límite de cuota excedido. Por favor, espera un minuto antes de reintentar."
            
        print(f"Error en /configurar: {error_msg}")
        return jsonify({"status": "error", "message": error_msg}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """
    Gestiona el envío de mensajes dentro de la sesión de chat activa.
    """
    global active_chat_session
    
    if active_chat_session is None:
        return jsonify({
            "status": "error", 
            "message": "No hay sesión activa. Por favor, 'Aplica la configuración' primero para iniciar/reiniciar el chat."
        }), 400
    
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"status": "error", "message": "El mensaje no puede estar vacío"}), 400
    
    try:
        # Envío de mensaje usando el nuevo método send_message del objeto Chat
        response = active_chat_session.send_message(user_message)
        return jsonify({
            "status": "success", 
            "response": response.text
        })
    except Exception as e:
        print(f"Error en /chat: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": f"Error al procesar el chat: {str(e)}"
        }), 500

@app.route("/reset", methods=["POST"])
def reset():
    """
    Borra la sesión de chat de la memoria.
    """
    global active_chat_session
    active_chat_session = None
    return jsonify({"status": "success", "message": "Sesión de chat cerrada. Lista para nueva configuración."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Inicia el servidor
    app.run(host="0.0.0.0", port=port, debug=True)
