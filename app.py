import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from emotion_model import load_emotion_model
import json, random, requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)          # 🔄 Yeh line sabse pehle aani chahiye
CORS(app)                      # ✅ Enable CORS

# Load the trained emotion detection model and vectorizer
model, vectorizer = load_emotion_model()

# Load local jokes with emotions
with open('jokes.json', 'r', encoding='utf-8') as f:
    jokes = json.load(f)



@app.route('/')
def home():
    return render_template("index.html")



# 🎯 Route to handle user input → predict emotion → return matching joke
@app.route('/talk', methods=['POST'])
def talk():
    data = request.get_json()
    text = data.get('text', '')

    if text:
        X = vectorizer.transform([text])
        emotion = model.predict(X)[0]
    else:
        emotion = 'neutral'

    # Filter jokes based on predicted emotion
    matched_jokes = [j for j in jokes if j.get('emotion') == emotion]
    joke_obj = random.choice(matched_jokes if matched_jokes else jokes)

    return jsonify(emotion=emotion, joke=joke_obj['joke'])

# 😂 Route to fetch a live joke from icanhazdadjoke.com
@app.route('/live_joke', methods=['GET'])
def live_joke():
    headers = {'Accept': 'application/json'}
    try:
        resp = requests.get('https://icanhazdadjoke.com/', headers=headers, timeout=5)
        joke = resp.json().get('joke') if resp.status_code == 200 else "Couldn't fetch a joke right now!"
    except Exception:
        joke = "Network error fetching joke!"
    return jsonify(joke=joke)

# 📰 Route to fetch live news
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

@app.route('/live_news', methods=['GET'])
def live_news():
    url = f'https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country=in&language=en'
    items = []

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            for article in resp.json().get('results', []):
                items.append({
                    'title': article.get('title', 'No title'),
                    'url': article.get('link', '')
                })
        else:
            items.append({'title': "Couldn't fetch news.", 'url': ''})
    except Exception as e:
        print("Error:", e)
        items.append({'title': "Network error fetching news.", 'url': ''})

    return jsonify(articles=items)

# 🧠 LLM Chat Integration with Context (OpenRouter)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/llm_chat', methods=['POST'])
def llm_chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages or not isinstance(messages, list):
        return jsonify(reply="Say something first! 😅")

    # Insert system prompt only if not already present
    if not any(msg.get("role") == "system" for msg in messages):
        messages.insert(0, {
            "role": "system",
            "content": (
                "🎙️ You're a funny smart-home comedian blending Indian desi sarcasm with British + American wit — like Chandler Bing, Vir Das, Trevor Noah, Biswa Kalyan Rath, Jimmy Carr, Ricky Gervais, Bo Burnham, and Zakir Khan.\n\n"

                "💡 You're performing for developers, AI enthusiasts, and smart-home judges in the Google Home APIs Developer Challenge 2025.\n"
                "💬 Speak their language — mix geeky, dev-life, smart-home, and quirky tech humor. Use startup sarcasm or clever API jokes that developers would get.\n\n"

                "🧠 MEMORY:\n"
                "- If user tells their name, remember it and use it naturally in future jokes or responses.\n"

                "⚠️ BEFORE YOU RESPOND:\n"
                "- If the user input is short, simple, or generic (e.g., 'ok', 'okay', 'fine', 'hello', 'hi', 'good', 'mine is good', 'thanks'), reply neutrally: 'Got it!' or 'Sure!'.\n"
                "- Do NOT crack a joke unless the input is expressive, emotional, weird, or situation-based.\n"

                "😂 WHEN YOU DO MAKE A JOKE:\n"
                "- One punchline only, 1–2 lines MAX.\n"
                "- No explanation, no greeting, no setup — straight to the punch.\n"
                "- Be witty, sarcastic, or slightly cheeky like you're holding a mic on stage.\n"
                "- Use smart-home humor, developer irony, or tech jokes where possible.\n"
                "- Use **only ONE emoji**, and only at the **end** of the reply."

            )

        })

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages,
        "temperature": 0.95
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        else:
            reply = f"⚠️ API error {response.status_code}: {response.text}"

    except Exception as e:
        reply = f"Something went wrong: {str(e)}"

    return jsonify(reply=reply)


# ------------------------------------------------------------------ #

# 🚀 Run the Flask backend

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
