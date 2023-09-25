import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')


class Video:
    service = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        """Инициализация видео по его ID"""
        self.video_response = self.service.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id).execute()
        self.video_id: str = video_id
        self.title: str = self.video_response['items'][0]['snippet']['title']
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        self.url = "https://www.youtube.com/channel/" + self.video_id

    def __str__(self):
        """Возвращает строковое представление видео в формате "<название_видео> (<ссылка_на_видео>)"."""
        return f"{self.title}"


class PLVideo(Video):
    """Класс для видео в плейлисте на YouTube"""

    def __init__(self, video_id, playlist_id):
        """Инициализация видео с указанием ID видео и ID плейлиста"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.service.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
