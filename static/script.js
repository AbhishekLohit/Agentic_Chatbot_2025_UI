async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const userText = inputField.value.trim();
    if (!userText) return;

    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class='message user-msg'>${userText}</div>`;
    inputField.value = "";
    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        const response = await fetch("/get", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ msg: userText })  // <-- Send JSON now
        });

        const data = await response.json();
        chatbox.innerHTML += `<div class='message bot-msg'>${data.response}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    } catch (error) {
        chatbox.innerHTML += `<div class='message bot-msg'>Error contacting server.</div>`;
    }
}
