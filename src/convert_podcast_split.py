
import ast
import re
from openai import OpenAI
from src.prompt import final


def convert_to_podcast_dialogue(cleaned_text: str, api_key: str, system_prompt: str) -> list:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick:free",
        messages=[
            {"role": "system", "content": final},
            {"role": "user", "content": cleaned_text}
        ]
    )

    content = response.choices[0].message.content.strip()

    # Try parsing directly first
    try:
        return ast.literal_eval(content)
    except (SyntaxError, ValueError):
        # Fallback: extract only list using regex
        match = re.search(r"\[\s*\(.*?\)\s*\]", content, re.DOTALL)
        if match:
            try:
                return ast.literal_eval(match.group(0))
            except Exception as e:
                raise ValueError(f"Regex matched, but eval failed: {e}")
        else:
            raise ValueError("Could not find valid list of tuples in model response.")



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
