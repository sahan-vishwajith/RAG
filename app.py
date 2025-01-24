import google.generativeai as genai
import gradio as gr
from flask import Flask, request, jsonify
import os
import threading

# Configure the Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

# Chatbot function
def chatbot(prompt):
    try:
        # Generate a response using the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = "give me the response assuming I am Sahan: " + prompt
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio Interface (UI)
def run_gradio():
    interface = gr.Interface(
        fn=chatbot,
        inputs=gr.Textbox(lines=5, placeholder="Enter your question here..."),
        outputs="text",
        title="Gemini AI Chatbot",
        description="A chatbot powered by Google's Gemini API."
    )
    # Use default Gradio behavior for Hugging Face Spaces
    interface.launch(enable_queue=True)

# Flask API (for programmatic access)
app = Flask(__name__)

@app.route("/api/generate", methods=["POST"])
def generate():
    # Parse the input prompt from the request
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Use the chatbot function to generate a response
    response = chatbot(prompt)
    return jsonify({"response": response})

# Run both Gradio and Flask servers
if __name__ == "__main__":
    # Start Gradio in a separate thread
    threading.Thread(target=run_gradio, daemon=True).start()

    # Run Flask server
    app.run(host="0.0.0.0", port=7860)
