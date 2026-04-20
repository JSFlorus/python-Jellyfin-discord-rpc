from config import JellyfinSettings
import requests
from pydantic import BaseModel, Json, ValidationError
import json



class JellyfinApi(JellyfinSettings):
    def __init__(self, settings: JellyfinSettings) -> None:
        self.__api_key = settings.api_key.get_secret_value()
        self.__url = settings.url
        self.__username = settings.username
        self.__raw_json = None
    
    def get_session_json(self) ->  None:
        url = f"{self.__url}/Sessions"
        headers = {
            "Authorization": f"MediaBrowser Token={self.__api_key}",
            "X-Emby-Token": f"MediaBrowser Token={self.__api_key}"
            }
        request = requests.get(url, headers=headers)
        print(request.status_code)
        #print(request.json())
        self.__raw_json = request.json()

        with open("sessions.json", "w") as f:
            json.dump(self.__raw_json, f, indent=2)

        #Music
        # print(self.__raw_json[0]["NowPlayingItem"]["Type"])
        # print(self.__raw_json[0]["NowPlayingItem"]["Path"])
        # print(self.__raw_json[0]["PlayState"]["PositionTicks"])
        # print(self.__raw_json[0]["UserName"])
        # print(self.__raw_json[0]["NowPlayingItem"]["Name"])
        # print(self.__raw_json[0]["NowPlayingItem"]["ProductionYear"])
        # print(self.__raw_json[0]["NowPlayingItem"]["RunTimeTicks"])
        # print(self.__raw_json[0]["NowPlayingItem"]["Album"])
        # print(self.__raw_json[0]["NowPlayingItem"]["AlbumId"])
        # print(self.__raw_json[0]["NowPlayingItem"]["AlbumPrimaryImageTag"])
        # print(self.__raw_json[0]["NowPlayingItem"]["AlbumArtist"])
        # print(self.__raw_json[0]["NowPlayingItem"]["Path"])
        # image_url = f"{self.__url}/Items/{self.__raw_json[0]["NowPlayingItem"]["AlbumId"]}/Images/Primary?tag={self.__raw_json[0]["NowPlayingItem"]["AlbumPrimaryImageTag"]}"
        # print(image_url)

        #Movie
        # print(self.__raw_json[0]["NowPlayingItem"]["Type"])
        # print(self.__raw_json[0]["NowPlayingItem"]["Path"])
        # print(self.__raw_json[0]["PlayState"]["PositionTicks"])
        # print(self.__raw_json[0]["UserName"])
        # print(self.__raw_json[0]["NowPlayingItem"]["Name"])
        # print(self.__raw_json[0]["NowPlayingItem"]["ProductionYear"])
        # print(self.__raw_json[0]["NowPlayingItem"]["RunTimeTicks"])
        # print(self.__raw_json[0]["NowPlayingItem"]["ImageTags"])
        # print(self.__raw_json[0]["NowPlayingQueue"][0]["Id"])
        # image_url = f"{self.__url}/Items/{self.__raw_json[0]["NowPlayingQueue"][0]["Id"]}/Images/Primary?tag={self.__raw_json[0]["NowPlayingItem"]["ImageTags"]["Primary"]}"
        # print(image_url)

        #Episode
        print(self.__raw_json[0]["NowPlayingItem"]["Type"])
        print(self.__raw_json[0]["NowPlayingItem"]["Path"])
        print(self.__raw_json[0]["PlayState"]["PositionTicks"])
        print(self.__raw_json[0]["UserName"])
        print(self.__raw_json[0]["NowPlayingItem"]["Name"])
        print(self.__raw_json[0]["NowPlayingItem"]["ProductionYear"])
        print(self.__raw_json[0]["NowPlayingItem"]["RunTimeTicks"])
        print(self.__raw_json[0]["NowPlayingItem"]["ParentLogoImageTag"])
        print(self.__raw_json[0]["NowPlayingItem"]["SeasonId"])
        print(self.__raw_json[0]["NowPlayingItem"]["SeriesId"])
        print(self.__raw_json[0]["NowPlayingItem"]["SeasonName"])
        image_url = f"{self.__url}/Items/{self.__raw_json[0]["NowPlayingItem"]["SeasonId"]}/Images/Primary?tag={self.__raw_json[0]["NowPlayingItem"]["ImageTags"]["Primary"]}"
        print(image_url)

    def parse_session_json(self) -> None:
        pass


settings = JellyfinSettings() # type: ignore
JellyfinApi(settings).get_session_json()
