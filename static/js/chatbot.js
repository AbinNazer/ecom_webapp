// Chatbot toggle & close
const toggle = document.getElementById("chatbot-toggle");
const chatbot = document.getElementById("chatbot-container");
const closeBtn = document.getElementById("close-chat");
const sendBtn = document.getElementById("chatbot-send");
const input = document.getElementById("chatbot-input");
const messages = document.getElementById("chatbot-messages");

toggle.onclick = () => (chatbot.style.display = "flex");
closeBtn.onclick = () => (chatbot.style.display = "none");

// Send message function
function sendMessage() {
  const userText = input.value.trim();
  if (!userText) return;

  // Append user message
  const userDiv = document.createElement("div");
  userDiv.className = "user-msg";
  userDiv.textContent = userText;
  messages.appendChild(userDiv);
  messages.scrollTop = messages.scrollHeight;

  // Clear input
  input.value = "";

  // Send to backend
  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userText })
  })
    .then(res => res.json())
    .then(data => {
      const botDiv = document.createElement("div");
      botDiv.className = "bot-msg";
      botDiv.textContent = data.reply;
      messages.appendChild(botDiv);
      messages.scrollTop = messages.scrollHeight;
    })
    .catch(() => {
      const botDiv = document.createElement("div");
      botDiv.className = "bot-msg";
      botDiv.textContent = ⚠️ Sorry, something went wrong.";
      messages.appendChild(botDiv);
      messages.scrollTop = messages.scrollHeight;
    });
}

sendBtn.onclick = sendMessage;
input.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});
