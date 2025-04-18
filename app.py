from flask import Flask, request, render_template, send_file
import os
from src.load_split_pdf import load_pdf, split_text

from src.clean_text import clean_text_with_groq
from src.convert_podcast_split import convert_to_podcast_dialogue, save_dialogue_to_files
from src.generate_Audio import generate_podcast
from src.prompt import final

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
OPEN_AI_KEY =os.getenv("OPEN_AI_KEY")


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# groq_api_key = "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"
# openai_api_key = "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"
system_prompt = final

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf = request.files["pdf"]
        if pdf:
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
            pdf.save(pdf_path)
            pdf_text = load_pdf("artifacts/paper.pdf")
            chunks = split_text(pdf_text)
            cleaned_text = clean_text_with_groq(chunks, GROQ_API_KEY)
           
            dialogue = convert_to_podcast_dialogue(cleaned_text, OPEN_AI_KEY, system_prompt)
            s1_lines, s2_lines = save_dialogue_to_files(dialogue)

            output_file = os.path.join("static", "output.mp3")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            generate_podcast(s1_lines, s2_lines, output_file)

            return render_template("index.html", audio_file="output.mp3")

    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
