import streamlit as st
from openai import OpenAI
import os
import base64
import requests
from dotenv import load_dotenv
import uuid
import streamlit.components.v1 as components

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def stt_util(audio):

    transcript = ''

    if audio:
        transcript = client.audio.transcriptions.create(
            model = "whisper-1",
            file = audio
        )

    return transcript.text

def llm_completion(input_text):

    output_text = ''

    response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [{"role": "user", "content": input_text}],
                temperature = 0,
            )

    output_text = response.choices[0].message.content

    return output_text

def tts_util(input_text):
    speech_file_path = "answer.mp3"

    # Check if the file exists, then remove it
    if os.path.exists(speech_file_path):
        os.remove(speech_file_path)

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=input_text
        ) as response:
    
        response.stream_to_file(speech_file_path)

    return speech_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        
        audio_html = f"""
                <audio id="player" controls autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                <script>
                    var audio = document.getElementById("player");
                    audio.play();
                </script>
                """
        components.html(audio_html, height=100)

def main():
    audio_value = st.audio_input("Record a voice message")

    if audio_value:
        with st.spinner("Speech to Text task..."):
            transcript = stt_util(audio_value)

        with st.spinner("Generating text answer..."):
            prompt = f"Instructions: You are a voice assistant answering shortly to the question a in a simple manner as a conversation. Answer in plain text as in a conversation. \nQuestion: {transcript}\nAnswer:"
            answer = llm_completion(prompt)

        with st.spinner("Text to Speech..."):
            answer_file = tts_util(answer)

        # st.audio(answer_file)
        autoplay_audio(answer_file)
        
if __name__ == '__main__':
    main()