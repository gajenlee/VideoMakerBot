import requests
from bs4 import BeautifulSoup
import random, re
import time
from tqdm import tqdm
from PIL import ImageFont

from moviepy.editor import TextClip 

class ContentCreator:
    
    __content_text = None
    __content_list = []
    __URL = "https://www.oberlo.com/blog/motivational-quotes"

    def __init__(self):
        self.__gather_content()
        self.__get_content_text()


    def __gather_content(self):
        try:

            print("The content gather it from web... ")
            response = requests.get(self.__URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find(id='article-content')
            content = content.find_all('li', {'aria-level': 1})
            self.__content_text = content

        except requests.ConnectionError() as e:
            print("Network Conntection Error")

        

    
    def __get_content_text(self):
        content = []
        for txt, _ in zip(self.__content_text, tqdm(self.__content_text, desc="Gathering...", ascii=False, ncols=75)):
            content.append(txt.get_text(strip=True))
        self.__content_list = content

    
    def choice_content(self):
        get_content = random.choice(self.__content_list)
        match = re.match(r'“(.*?)” ―(.*)', get_content)
        if match:
            sentence = match.group(1).strip()
            author = match.group(2).strip()
        else:
            sentence = get_content.strip()
            author = ""
        
        return {
            "quote" : sentence,
            "author": author
        }
        
        
