import os
import ast
import re
import google.generativeai as genai
from dotenv import load_dotenv
from src.prompt import final

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def convert_to_podcast_dialogue(cleaned_text: str) -> list:
    if not GOOGLE_API_KEY:
        raise ValueError("Google API key not found")

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-1.5-pro')

    # Combine system prompt + user input into a single string
    full_prompt = f"{final}\n\n{cleaned_text}"

    # No roles, just plain string
    response = model.generate_content(full_prompt)

    content = response.text.strip()
    print("==== MODEL RAW OUTPUT ====")
    print(content)
    print("==========================")


    try:
        return ast.literal_eval(content)
    except Exception:
        match = re.search(r"\[\s*\(.*?\)\s*\]", content, re.DOTALL)
        if match:
            try:
                return ast.literal_eval(match.group(0))
            except Exception as e:
                raise ValueError(f"Regex matched but eval failed: {e}")
        raise ValueError("Could not parse model output into list of tuples")


# # save_dialogue.py
def save_dialogue_to_files(dialogue: list, s1_path="speaker_1.txt", s2_path="speaker_2.txt"):
    speaker_1_lines, speaker_2_lines = [], []

    for speaker, line in dialogue:
        if speaker == "Speaker 1":
            speaker_1_lines.append(line)
        elif speaker == "Speaker 2":
            speaker_2_lines.append(line)

    with open(s1_path, "w", encoding="utf-8") as f1:
        f1.writelines([line + "\n" for line in speaker_1_lines])

    with open(s2_path, "w", encoding="utf-8") as f2:
        f2.writelines([line + "\n" for line in speaker_2_lines])

    return speaker_1_lines, speaker_2_lines


