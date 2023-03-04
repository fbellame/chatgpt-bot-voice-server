import os
import openai
import gradio as gr
import subprocess

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("MY_ORGANISATION")
messages = [{"role": "system", "content": "Tu es un assistant. Répond à la manière d'un thérapeute."}]


def bot_ai(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    messages.append({"role": "user", "content": transcript["text"]})

    # chatGPT3.5 new API
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                    )
    
    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    subprocess.call(["say", system_message["content"]])

    chat_transcript = ""
    for message in messages:
        if message["role"] != "system":
            chat_transcript += message["role"] + ":" + message["content"] + "\n\n"

    return chat_transcript

if __name__ == "__main__":
    ui = gr.Interface(fn=bot_ai, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
