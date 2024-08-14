from gtts import gTTS
import os
import pyttsx3 as pyt

import edge_tts, asyncio

class VoiceMaker:

    
    def speech_text(self, text, file_name):
        tts = gTTS(text=text, lang='en-GB')
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        tts.save(file_name)
    
    def speech(self, text, file_name):
        voice = "es-GT-AndresNeural"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        communicate = edge_tts.Communicate(
            text, 
            voice=voice,
            rate="-15%",
        )
        asyncio.run(communicate.save(file_name))
        


        

        
       


    
    