from flask import Flask, render_template, request
from googletrans import Translator
from gtts import gTTS
import pygame
from io import BytesIO

app = Flask(__name__)

def translate_text(text, target_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang)
    return translated_text.text

def play_audio(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

@app.route('/')
def index():
    return render_template('index.html', translated_text='')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    target_lang = request.form['target_lang']
    translated_text = translate_text(text, target_lang)
    play_audio(translated_text, target_lang)
    return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
