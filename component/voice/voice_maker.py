from gtts import gTTS
import os
import pyttsx3 as pyt

class VoiceMaker:

    
    def speech_text(self, text, file_name):
        tts = gTTS(text=text, lang='en-GB')
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        tts.save(file_name)

        
       


    
    