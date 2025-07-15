from flask import Flask, request, render_template
from elevenlabs import save, play
from elevenlabs.client import ElevenLabs
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
import uuid
load_dotenv()
app = Flask(__name__, static_folder="static1")

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = ""

    # Handle PDF upload
    if 'pdf' in request.files:
        file = request.files['pdf']
        if file.filename.endswith('.pdf'):
            reader = PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                print(f"🔍 Page {page_num + 1} text:", repr(page_text))  # Debug log
                if page_text:
                    text += page_text + "\n"

    # Handle text input
    if not text and 'text' in request.form:
        text = request.form['text']

    if text:  # This should run whether the source was PDF or text input
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="uju3wxzG5OhpWcoi3SMy",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            voice_settings={
                "stability": 0.6,
                "similarity_boost": 0.85
            }
        )

        absolute_folder = os.path.join(app.root_path, 'static1')
        os.makedirs(absolute_folder, exist_ok=True)
        filename = os.path.join(absolute_folder, f"{uuid.uuid4().hex}.mp3")
        save(audio, filename)
        basename = os.path.basename(filename)

        return render_template("download.html", filename=basename)

    return "No text found."


if __name__ == '__main__':
    app.run(debug=True)
