import requests
import random
import os
from tqdm import tqdm

class BackgroundVideoDownloader:

    __API_KEY = "kQzKaSbKOr8itUi4jcXyJKXDaKJvL7kTj5D5NbCnTJV0kT0M8sOjNLIw"
    __URL = "https://api.pexels.com/videos/search"
    __QUERY = "boxing sport"
    __PER_PAGE = 5

    __headers = {
        'Authorization': __API_KEY
    }

    def __fetch_videos(self, query, per_page):
        params = {
            'query': query,
            'per_page': per_page
        }

        # access the api and get response from the web
        response = requests.get(self.__URL, headers=self.__headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def __download_video(self, video_url, file_name):
        response = requests.get(video_url, stream=True) # get response
        response.raise_for_status() # check is there any error
        total_size = int(response.headers.get('content-length', 0)) # response size
        
        # write the file and show loading bar
        with open(file_name, 'wb') as file, tqdm(
            desc=file_name, 
            total=total_size, 
            unit='iB', 
            unit_scale=True, 
            unit_divisor=1024) as bar:

            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        
        print(f"Downloaded {file_name}")

    
    def downloadSave(self, file_name):

        # get the random video link and make dir 
        videos = self.__fetch_videos(self.__QUERY, self.__PER_PAGE)
        video = random.choice(videos['videos'])
        video_url = video['video_files'][0]['link']
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        self.__download_video(video_url, file_name)

    

