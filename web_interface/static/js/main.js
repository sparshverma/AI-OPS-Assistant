const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');

function appendMessage(role, text) {
    const isUser = role === 'User';
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;

    // Convert newlines to <br> for basic formatting
    const formattedText = text.replace(/\n/g, '<br>');

    messageDiv.innerHTML = `
        <div class="avatar">${isUser ? 'You' : 'AI'}</div>
        <div class="content">${formattedText}</div>
    `;

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Clear input
    userInput.value = '';

    // Show user message
    appendMessage('User', text);

    // Show loading state
    const loadingId = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message ai-message';
    loadingDiv.id = loadingId;
    loadingDiv.innerHTML = `
        <div class="avatar">AI</div>
        <div class="content"><i>Thinking...</i></div>
    `;
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();

        // Remove loading
        document.getElementById(loadingId).remove();

        // Show AI response
        appendMessage('AI', data.response);

    } catch (error) {
        document.getElementById(loadingId).remove();
        appendMessage('AI', "Sorry, I encountered an error connecting to the server.");
        console.error(error);
    }
}
