const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = statusIndicator.querySelector('.status-text');

let isProcessing = false;
let currentEventSource = null;

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const question = userInput.value.trim();
    if (!question || isProcessing) return;

    addMessage(question, 'user');

    userInput.value = '';
    userInput.style.height = 'auto';
    userInput.style.overflowY = 'hidden';
    autoResizeTextarea();

    setProcessing(true);
    await streamResponse(question);
    setProcessing(false);
});

function addMessage(content, type = 'user') {
    const messageDiv = document.createElement('div');
    messageDiv.style.display = 'flex';
    messageDiv.style.justifyContent = type === 'user' ? 'flex-end' : 'flex-start';

    const bubble = document.createElement('div');
    bubble.className = type === 'user' ? 'user-bubble' : 'bot-bubble';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    bubble.appendChild(contentDiv);
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);

    scrollToBottom();
}

function addInfoMessage(content) {
    const infoDiv = document.createElement('div');
    infoDiv.className = 'info-bubble';
    infoDiv.textContent = `INFO: ${content}`;
    chatMessages.appendChild(infoDiv);
    scrollToBottom();
}

function addCypherMessage(cypher) {
    const cypherDiv = document.createElement('div');
    cypherDiv.className = 'cypher-bubble';
    cypherDiv.textContent = cypher;
    chatMessages.appendChild(cypherDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const typingDiv = document.getElementById('typingIndicator');
    if (typingDiv) {
        typingDiv.remove();
    }
}

function createBotMessageBubble() {
    const messageDiv = document.createElement('div');
    messageDiv.style.display = 'flex';
    messageDiv.style.justifyContent = 'flex-start';
    messageDiv.id = 'streamingMessage';

    const bubble = document.createElement('div');
    bubble.className = 'bot-bubble';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.id = 'streamingContent';

    bubble.appendChild(contentDiv);
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);

    return contentDiv;
}

function addMetadata(data) {
    const streamingMessage = document.getElementById('streamingMessage');
    if (!streamingMessage) return;

    const bubble = streamingMessage.querySelector('.bot-bubble');

    if (bubble.querySelector('.metadata-info')) return;

    const metadataDiv = document.createElement('div');
    metadataDiv.className = 'metadata-info';

    if (data.sources && data.sources.length > 0) {
        const sourcesTag = document.createElement('div');
        sourcesTag.className = 'metadata-tag';
        sourcesTag.textContent = `Sumber: ${data.sources.join(', ')}`;
        metadataDiv.appendChild(sourcesTag);
    }

    if (data.confidence !== undefined) {
        const confidenceTag = document.createElement('div');
        confidenceTag.className = 'metadata-tag';
        confidenceTag.textContent = `Kepercayaan: ${(data.confidence * 100).toFixed(0)}%`;
        metadataDiv.appendChild(confidenceTag);
    }

    if (metadataDiv.children.length > 0) {
        bubble.appendChild(metadataDiv);
    }
}

async function streamResponse(question) {
    if (currentEventSource) {
        currentEventSource.close();
    }

    showTypingIndicator();

    let streamingContent = null;
    let hasStartedGeneration = false;

    const encodedQuestion = encodeURIComponent(question);
    currentEventSource = new EventSource(`/api/chat/stream?question=${encodedQuestion}`);

    currentEventSource.addEventListener('info', (e) => {
        removeTypingIndicator();
        addInfoMessage(e.data);
    });

    currentEventSource.addEventListener('cypher', (e) => {
        if (e.data !== 'Translating question to graph query...') {
            addCypherMessage(e.data);
        }
        updateStatus(e.data);
    });

    currentEventSource.addEventListener('retrieval', (e) => {
        updateStatus(e.data);
    });

    let generationLines = [];

    currentEventSource.addEventListener('generation', (e) => {
        if (!hasStartedGeneration) {
            removeTypingIndicator();
            streamingContent = createBotMessageBubble();
            hasStartedGeneration = true;
            generationLines = [];
        }

        if (streamingContent) {
            generationLines.push(e.data);
            streamingContent.textContent = generationLines.join('\n');
            scrollToBottom();
        }
    });

    currentEventSource.addEventListener('done', (e) => {
        const data = JSON.parse(e.data);

        addMetadata(data);

        const streamingMessage = document.getElementById('streamingMessage');
        if (streamingMessage) {
            streamingMessage.removeAttribute('id');
        }

        streamingContent = null;
        currentEventSource.close();
        currentEventSource = null;
        updateStatus('Siap');

        scrollToBottom();
    });

    currentEventSource.addEventListener('error', (e) => {
        removeTypingIndicator();

        let errorMessage = 'Terjadi kesalahan saat memproses permintaan Anda.';
        if (e.data) {
            errorMessage = e.data;
        }

        addMessage(`Error: ${errorMessage}`, 'bot');

        if (currentEventSource) {
            currentEventSource.close();
            currentEventSource = null;
        }

        updateStatus('Error', 'error');
        setTimeout(() => updateStatus('Siap'), 3000);
    });

    currentEventSource.onerror = (error) => {
        console.error('EventSource error:', error);

        if (currentEventSource && currentEventSource.readyState === EventSource.CLOSED) {
            return;
        }

        removeTypingIndicator();
        addMessage('Kesalahan koneksi. Silakan coba lagi.', 'bot');

        if (currentEventSource) {
            currentEventSource.close();
            currentEventSource = null;
        }

        updateStatus('Kesalahan Koneksi', 'error');
        setTimeout(() => updateStatus('Siap'), 3000);
    };
}

function updateStatus(message, type = 'processing') {
    statusText.textContent = message;
    statusIndicator.className = 'status-indicator';

    if (type === 'processing') {
        statusIndicator.classList.add('processing');
    } else if (type === 'error') {
        statusIndicator.classList.add('error');
    }
}

function setProcessing(processing) {
    isProcessing = processing;
    sendButton.disabled = processing;
    userInput.disabled = processing;

    if (processing) {
        updateStatus('Memproses...', 'processing');
    } else {
        updateStatus('Siap');
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function autoResizeTextarea() {
    userInput.style.height = 'auto';

    const scrollHeight = userInput.scrollHeight;
    const newHeight = Math.min(Math.max(scrollHeight, 48), 150);

    userInput.style.height = newHeight + 'px';

    if (scrollHeight > 150) {
        userInput.style.overflowY = 'auto';
    } else {
        userInput.style.overflowY = 'hidden';
    }
}

userInput.addEventListener('input', autoResizeTextarea);

window.addEventListener('load', () => {
    userInput.focus();
    autoResizeTextarea();
});

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

