// Auto focus input box when page loads
window.onload = function () {
    document.getElementById("user-input").focus();
};

// Send message on Enter key
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Dark Mode Toggle
function toggleTheme() {
    document.body.classList.toggle("dark");
}

// Text To Speech
function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;
    speechSynthesis.speak(speech);
}

.time{
    font-size:11px;
    margin-top:5px;
    opacity:0.7;
}
// Voice Input
function startVoice() {

    if (!('webkitSpeechRecognition' in window)) {
        alert("Speech Recognition not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("user-input").value = transcript;
    };

    recognition.onerror = function(event) {
        console.log("Voice Error:", event.error);
    };
}

// Current Time
function getCurrentTime() {

    const now = new Date();

    return now.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Main Chat Function
async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    let message = input.value.trim();

    if (message === "") return;

    // User Message
    chatBox.innerHTML += `
        <div class="user-message">
            ${message}
            <div class="time">${getCurrentTime()}</div>
        </div>
    `;

    input.value = "";

    // Typing Indicator
    chatBox.innerHTML += `
        <div class="typing" id="typing">
            Assistant is typing<span>.</span><span>.</span><span>.</span>
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Remove Typing Indicator
        const typingElement = document.getElementById("typing");
        if (typingElement) {
            typingElement.remove();
        }

        // Bot Reply
        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.reply}
                <div class="time">${getCurrentTime()}</div>
            </div>
        `;

        speak(data.reply);

    } catch (error) {

        const typingElement = document.getElementById("typing");
        if (typingElement) {
            typingElement.remove();
        }

        chatBox.innerHTML += `
            <div class="bot-message">
                ⚠️ Server connection failed.
            </div>
        `;

        console.error(error);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}