from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini AI securely
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing API key. Set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Allowed topics
ALLOWED_TOPICS = ["meditation", "exercise", "fitness", "mindfulness", "yoga", "workout", "relaxation", "stress relief"]

def is_relevant(message):
    message = message.lower()
    return any(topic in message for topic in ALLOWED_TOPICS)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not is_relevant(user_input):
        return jsonify({"response": "I'm here to help with meditation and exercise only. Please ask related questions!"})

    prompt = f"""
    You are a meditation and fitness assistant. Respond only with helpful information about meditation, relaxation, fitness, yoga, and mindfulness. 
    If the question is unrelated, politely refuse to answer.
    
    User: {user_input}
    Bot:
    """
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")  
        return jsonify({"response": "An error occurred. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
