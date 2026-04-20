from config import JellyfinSettings
import requests



class JellyfinApi(JellyfinSettings):
    def __init__(self, settings: JellyfinSettings) -> None:
        self.__api_key = settings.api_key.get_secret_value()
        self.__url = settings.url
        self.__username = settings.username
    
    def get_session_json(self) ->  None:
        url = f"{self.__url}/Sessions"
        headers = {
            "Authorization": f"MediaBrowser Token={self.__api_key}",
            "X-Emby-Token": f"MediaBrowser Token={self.__api_key}"
            }
        request = requests.get(url, headers=headers)
        print(request.status_code)
        print(request.json())


settings = JellyfinSettings() # type: ignore
JellyfinApi(settings).get_session_json()
