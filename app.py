from flask import Flask, request, render_template
import os
from src.load_split_pdf import text_split,pdfloader

from src.clean_text import clean_text_with_groq
from src.convert_podcast_split import convert_to_podcast_dialogue, save_dialogue_to_files
from src.generate_Audio import generate_podcast
from src.prompt import final

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")




app = Flask(__name__)
UPLOAD_FOLDER = "artifacts"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# groq_api_key = "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"
# openai_api_key = "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"
system_prompt = final

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf = request.files["pdf"]
        if pdf:
            # Save the uploaded PDF into the artifacts folder with its original name
            artifacts_path = os.path.join("artifacts", pdf.filename)
            os.makedirs("artifacts", exist_ok=True)
            pdf.save(artifacts_path)

            # Load and process the uploaded PDF
            pdf_text = pdfloader(artifacts_path)
            chunks = text_split(pdf_text)
            cleaned_text = clean_text_with_groq(GROQ_API_KEY, chunks)


            dialogue = convert_to_podcast_dialogue(cleaned_text)
            s1_lines, s2_lines = save_dialogue_to_files(dialogue)

            # Generate audio
            output_file = os.path.join("static", "output.mp3")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            generate_podcast(s1_lines, s2_lines, output_file)

            return render_template("index.html", audio_file="output.mp3")

    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
