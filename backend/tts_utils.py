from gtts import gTTS
from googletrans import Translator
import os


def translate_text(text, dest='en'):
    tr = Translator()
    res = tr.translate(text, dest=dest)
    return res.text


def tts_to_file(text, lang, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tts = gTTS(text=text, lang=lang)
    tts.save(out_path)
    return out_path
