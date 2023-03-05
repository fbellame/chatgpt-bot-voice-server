import os
import openai
import gradio as gr
#import IPython.display as ipd
from gtts import gTTS
import io

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("MY_ORGANISATION")
messages = [{"role": "system", "content": "Répond en faisant des réponses courtes."}]


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

    reponse_file = "reponse-gpt3.mp3"
    tts = gTTS(text=system_message["content"], lang= 'fr', slow=False, tld="fr")
    tts.save(reponse_file)

    chat_transcript = ""
    for message in messages:
        if message["role"] != "system":
            chat_transcript += message["role"] + ":" + message["content"] + "\n\n"

    return reponse_file, chat_transcript

if __name__ == "__main__":

    outputs = [gr.Audio(label="Output Audio", type="filepath"), "text"]
    
    ui = gr.Interface(fn=bot_ai, inputs=gr.Audio(source="microphone", type="filepath"), outputs=outputs )
    shared_url = ui.launch('share=True')
    print(shared_url)
