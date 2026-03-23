document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const systemPrompt = document.getElementById('system-prompt');
    const temperature = document.getElementById('temperature');
    const tempVal = document.getElementById('temp-val');
    const applyConfigBtn = document.getElementById('apply-config');
    const resetChatBtn = document.getElementById('reset-chat');
    const loadingIndicator = document.getElementById('loading-indicator');

    // Actualizar valor de temperatura en tiempo real
    temperature.addEventListener('input', () => {
        tempVal.textContent = temperature.value;
    });

    // Función para añadir mensajes al chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = text;
        
        messageDiv.appendChild(bubble);
        chatMessages.appendChild(messageDiv);
        
        // Scroll automático al último mensaje
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Configurar / Aplicar cambios
    async function configureChatbot() {
        const prompt = systemPrompt.value;
        const temp = parseFloat(temperature.value);

        applyConfigBtn.disabled = true;
        applyConfigBtn.textContent = 'Configurando...';

        try {
            const response = await fetch('/configurar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ system_prompt: prompt, temperature: temp })
            });
            const data = await response.json();

            if (data.status === 'success') {
                // Limpiar mensajes y mostrar mensaje de sistema
                chatMessages.innerHTML = '';
                addMessage(`--- Sistema reiniciado con nueva directiva ---`, 'bot');
                addMessage(`Neon está listo. ¿Qué hay en tu mente, glitch?`, 'bot');
            } else {
                alert('Error: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error de conexión al configurar.');
        } finally {
            applyConfigBtn.disabled = false;
            applyConfigBtn.textContent = 'Aplicar Configuración';
        }
    }

    // Enviar mensaje
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Mostrar mensaje del usuario
        addMessage(message, 'user');
        userInput.value = '';
        
        // Mostrar indicador de carga
        loadingIndicator.classList.remove('hidden');
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();

            if (data.status === 'success') {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Error: ' + data.message, 'bot');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Error de conexión al servidor.', 'bot');
        } finally {
            loadingIndicator.classList.add('hidden');
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Reiniciar sesión
    async function resetSession() {
        if (!confirm('¿Estás seguro de que quieres reiniciar la conversación?')) return;

        try {
            const response = await fetch('/reset', { method: 'POST' });
            const data = await response.json();
            if (data.status === 'success') {
                chatMessages.innerHTML = '';
                addMessage('Sesión borrada de la memoria. Configura de nuevo para empezar.', 'bot');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Event Listeners
    applyConfigBtn.addEventListener('click', configureChatbot);
    resetChatBtn.addEventListener('click', resetSession);
    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Configuración inicial automática al cargar
    configureChatbot();
});
