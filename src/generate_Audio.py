import os
import asyncio
from gtts import gTTS
import edge_tts
from moviepy import AudioFileClip, concatenate_audioclips

def generate_podcast(speaker_1_lines, speaker_2_lines, output_file="podcast_episode.mp3"):
    os.makedirs("audio", exist_ok=True)
    clips = []

    async def generate_edge_voice(text, filename):
        communicate = edge_tts.Communicate(text, voice="en-GB-RyanNeural")
        await communicate.save(filename)

    num_lines = min(len(speaker_1_lines), len(speaker_2_lines))

    for i in range(num_lines):
        # Speaker 1
        speaker1_path = f"audio/speaker1_{i}.mp3"
        gTTS(speaker_1_lines[i], lang='en').save(speaker1_path)
        clips.append(AudioFileClip(speaker1_path))

        # Speaker 2
        speaker2_path = f"audio/speaker2_{i}.mp3"
        asyncio.run(generate_edge_voice(speaker_2_lines[i], speaker2_path))
        clips.append(AudioFileClip(speaker2_path))

    final = concatenate_audioclips(clips)
    final.write_audiofile(output_file)
    print(f"✅ Podcast saved as {output_file}")
