let chatHistory = [];  // 🧠 Chat memory

function sendToBackend() {
  const text = document.getElementById('textInput').value;

  fetch('https://funnyfriend.onrender.com/talk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  })
  .then(response => response.json())
  .then(data => {
    const responseBox = document.getElementById('responseBox');
    const message = `Emotion: ${data.emotion}. Joke: ${data.joke}`;
    responseBox.innerHTML += `
      <p><strong>Emotion:</strong> ${data.emotion}</p>
      <p><strong>Joke:</strong> ${data.joke}</p>
    `;
    speak(message);  // 🔊 Speak emotion + joke
    responseBox.scrollTop = responseBox.scrollHeight;
  })
  .catch(err => {
    console.error('Error talking to server:', err);
    alert("Error talking to server. Is your backend running?");
  });
}

async function getLiveJoke() {
  try {
    const resp = await fetch('https://funnyfriend.onrender.com/live_joke');
    const data = await resp.json();

    const joke = data.joke;
    const box = document.getElementById('responseBox');
    box.innerHTML += `<p><strong>😂 Live Joke:</strong> ${joke}</p>`;
    speak(joke);
    box.scrollTop = box.scrollHeight;
  } catch (err) {
    console.error("Live joke fetch error:", err);
    alert("Couldn't fetch live joke.");
  }
}

async function getLiveNews() {
  try {
    const resp = await fetch('https://funnyfriend.onrender.com/live_news');
    const data = await resp.json();

    const box = document.getElementById('responseBox');
    let msg = "📰 Latest news:<br>";

    data.articles.slice(0, 5).forEach(a => {
      msg += `• ${a.title}<br>`;
    });

    box.innerHTML += `<p>${msg}</p>`;
    speak(msg.replace(/<br>/g, '. '));
    box.scrollTop = box.scrollHeight;
  } catch (err) {
    console.error("Live news fetch error:", err);
    alert("Couldn't fetch live news.");
  }
}

function startVoiceInput() {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Sorry, your browser doesn't support speech recognition.");
    return;
  }

  const recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.start();

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("textInput").value = transcript;
    sendToBackend(); // For emotion-based joke
  };

  recognition.onerror = function (event) {
    alert("Speech recognition error: " + event.error);
  };
}

function speak(text) {
  if ('speechSynthesis' in window && text.trim() !== "") {
    const cleanedText = text
      .replace(/[\p{Emoji_Presentation}\p{Extended_Pictographic}]/gu, '')
      .replace(/#[^\s#]+/g, '')
      .replace(/\*/g, '')
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanedText);
    utterance.lang = "en-US";
    utterance.rate = 1;

    window.speechSynthesis.speak(utterance);
  } else {
    alert("Sorry, speech synthesis not supported or text is empty.");
  }
}

function askLLMText() {
  const text = document.getElementById("textInput").value.trim();
  if (!text) {
    alert("Please type something to ask the funny assistant!");
    return;
  }
  sendLLMRequest(text);
}

function askLLMSpeak() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = function (event) {
    const spokenText = event.results[0][0].transcript.trim();

    // 🟡 Add this line for debugging
    console.log("Captured voice:", spokenText);

    if (!spokenText) {
      alert("Mic didn't catch anything.");
      return;
    }

    document.getElementById("textInput").value = spokenText;

    // 🔁 Small delay to ensure textInput updates visually
    setTimeout(() => sendLLMRequest(spokenText), 100);
  };

  recognition.onerror = function (event) {
    console.error("Speech error:", event.error);
    alert("Speech recognition error: " + event.error);
  };
}

function sendLLMRequest(text) {
  const responseBox = document.getElementById("responseBox");

  // Add user message to history
  chatHistory.push({ role: "user", content: text });

  fetch("https://funnyfriend.onrender.com/llm_chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages: chatHistory })
  })
  .then(res => res.json())
  .then(data => {
    // Add assistant reply to history
    chatHistory.push({ role: "assistant", content: data.reply });

    // Show both in chat window
    responseBox.innerHTML += `<p><strong>You:</strong> ${text}</p>`;
    responseBox.innerHTML += `<p><strong>🤖 Funny Friend:</strong> ${data.reply}</p>`;

    speak(data.reply);
    responseBox.scrollTop = responseBox.scrollHeight;
  })
  .catch(err => {
    console.error("LLM chat error:", err);
    alert("Could not reach the funny assistant.");
  });
}
