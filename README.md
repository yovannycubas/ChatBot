# 🌃 CyberChat 2099: Neon's Bar

¡Bienvenido a Ciudad Nueva! `CyberChat 2099` es una aplicación web interactiva que utiliza la potencia de **Google Gemini** para dar vida a **Neon**, un barman cínico pero sabio de un futuro distópico.

Este proyecto ha sido diseñado para demostrar la integración de modelos de lenguaje avanzados con un frontend moderno y altamente estético (Cyberpunk).

![Vista Previa](static/css/screenshot.png) <!-- Reemplázame con una captura si gustas! -->

## 🚀 Características

- **Personalidad Configurable**: Cambia la "instrucción de sistema" en tiempo real desde el panel lateral.
- **Control de Creatividad**: Ajusta la temperatura (0.0 - 2.0) para obtener respuestas precisas o narrativas salvajes.
- **Interfaz Cyberpunk Premium**:
  - Efectos de neón y glitch.
  - Diseño Glassmorphism.
  - Tipografía futurista.
  - Animaciones de carga y scroll automático.
- **Backend Flask**: Gestión robusta de sesiones de chat en memoria utilizando el SDK de Gemini.

## 🛠️ Requisitos Técnico

### Tecnologías
- **Backend**: Python 3.x, Flask.
- **AI**: Google Generative AI (Gemini Pro/Flash).
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+).

### Dependencias
- `flask`
- `google-generativeai`
- `python-dotenv`

## ⚙️ Instalación y Uso

1. **Clona el repositorio**:
   ```bash
   git clone <tu-url-de-github>
   cd ChatBot
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura tu API Key**:
   - Crea un archivo `.env` en la raíz (ya existe una plantilla).
   - Agrega tu clave de API de Google Gemini:
     ```env
     GEMINI_API_KEY=tu_clave_aqui
     ```
   *Nota: El archivo `.env` está protegido por el `.gitignore` incluido.*

4. **Inicia el servidor**:
   ```bash
   python app.py
   ```

5. **Abre tu navegador**:
   Visita `http://localhost:5000`.

## 📂 Estructura del Proyecto

```text
ChatBot/
├── static/
│   ├── css/
│   │   └── style.css      # Estilos Cyberpunk
│   └── js/
│       └── main.js       # Lógica de chat y API
├── templates/
│   └── index.html         # Estructura principal
├── .env                   # Variables sensibles (No subido a Git)
├── .gitignore             # Protección de archivos
├── app.py                 # Servidor Flask e integración Gemini
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🔒 Seguridad
Este proyecto incluye un archivo `.gitignore` configurado para evitar la filtración accidental de claves de API. **Nunca compartas tu clave de API ni subas el archivo `.env` a repositorios públicos.**

---
*Desarrollado para la materia de Programación Web / Inteligencia Artificial.*
