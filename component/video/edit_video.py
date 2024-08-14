import os, datetime

import moviepy.editor as edit

from .background_video_downloader import BackgroundVideoDownloader
from ..image_text.content_creator import ContentCreator
from ..image_text.process_image import ProcessImage
from ..voice.voice_maker import VoiceMaker


class EditVideo(ContentCreator):

    FINAL_PATH_ONE = os.path.join(r"C:/Users/{}/Documents/".format(os.getlogin()))
    FINAL_PATH_TWO = os.path.join(r"C:/Users/{}/OneDrive/Documents/".format(os.getlogin()))
    FINAL_FILE_NAME = f"video/final_video_{datetime.datetime.today().strftime('[%Y-%m-%d]_[%I-%M]')}.mp4"

    FINAL_VIDEO_PATH = os.path.join("video/")
    PROGRAM_FOLDER = 'VideoCreation/'

    VIDEO_FILE = os.path.join("source/video/", "bg.mp4")
    VOICE_FILE = os.path.join("source/voice/", "voice.mp3")
    IMAGE_FILE = os.path.join("source/image/", "img.png")

    NEW_VIDEO_FILE_PATH = None
    NEW_VOICE_FILE_PATH = None
    NEW_IMAGE_FILE_PATH = None

    NEW_FINAL_FOLDER_PATH = None

    __text = None

    def __create_source_folder(self):
        if os.path.isdir(self.FINAL_PATH_TWO) and os.path.isdir(self.FINAL_PATH_TWO + self.PROGRAM_FOLDER) == False:
            path = os.path.join(self.FINAL_PATH_TWO + self.PROGRAM_FOLDER)
            os.makedirs(path, exist_ok=True)

        elif os.path.isdir(self.FINAL_PATH_ONE + self.PROGRAM_FOLDER) == False:
            path = os.path.join(self.FINAL_PATH_ONE + self.PROGRAM_FOLDER)
            os.makedirs(path, exist_ok=True)
        
        if os.path.isdir(self.FINAL_PATH_TWO):
            self.NEW_FINAL_FOLDER_PATH = os.path.join(self.FINAL_PATH_TWO + self.PROGRAM_FOLDER)
            os.makedirs(self.NEW_FINAL_FOLDER_PATH + self.FINAL_VIDEO_PATH, exist_ok=True)

        elif os.path.isdir(self.FINAL_PATH_ONE):
            self.NEW_FINAL_FOLDER_PATH = os.path.join(self.FINAL_PATH_ONE + self.PROGRAM_FOLDER)
            os.makedirs(self.NEW_FINAL_FOLDER_PATH + self.FINAL_VIDEO_PATH, exist_ok=True)

        

    def __add_text(self):
        self.__text = self.choice_content()
        return self.__text


    def __add_background_video(self):
        back = BackgroundVideoDownloader()
        self.NEW_VIDEO_FILE_PATH = os.path.join(self.NEW_FINAL_FOLDER_PATH + self.VIDEO_FILE)
        back.downloadSave(self.NEW_VIDEO_FILE_PATH)
    
    def __add_voice(self):
        voice = VoiceMaker()
        self.NEW_VOICE_FILE_PATH = os.path.join(self.NEW_FINAL_FOLDER_PATH + self.VOICE_FILE)
        voice.speech(self.__text["quote"], self.NEW_VOICE_FILE_PATH)

    def __add_image(self):
        self.NEW_IMAGE_FILE_PATH = os.path.join(self.NEW_FINAL_FOLDER_PATH + self.IMAGE_FILE)
        process_image = ProcessImage(self.__text["quote"], self.NEW_IMAGE_FILE_PATH)
        process_image.save_image()

    def mixing_video(self):

        self.__create_source_folder()
        
        self.__add_text()
        self.__add_background_video()
        self.__add_voice()
        self.__add_image()
        video = edit.VideoFileClip(self.NEW_VIDEO_FILE_PATH)
        video_cropped = video.crop(width=video.w, height=int(video.w * 16 / 9), x_center=video.w / 2, y_center=video.h / 2)

        video_resized = video_cropped.resize((1080, 1920))


        audio = edit.AudioFileClip(self.NEW_VOICE_FILE_PATH)
        video_final = video_resized.subclip(0, audio.duration)
        image_clip = edit.ImageClip(self.NEW_IMAGE_FILE_PATH).set_position('center').set_duration(audio.duration)

    
        video_final.audio = edit.CompositeAudioClip([audio])

        final_mix = edit.CompositeVideoClip([video_final, image_clip])
        final_mix.write_videofile(os.path.join(self.NEW_FINAL_FOLDER_PATH, self.FINAL_FILE_NAME), codec="libx264", audio_codec="aac", audio_bitrate="192k", bitrate="1000k")
        



