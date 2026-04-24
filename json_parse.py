from config import JellyfinSettings
import requests


def get_duration(ticks):
    time_seconds = int(ticks / 10_000_000)
    if time_seconds < 60:
        seconds = time_seconds
        return {
            "seconds" : seconds
        }
    elif time_seconds > 60 and time_seconds < 60*60:
        minutes = time_seconds // 60
        seconds = time_seconds % 60
        return {
            "seconds" : seconds,
            "minutes" : minutes
        }        
    else:
        hours = time_seconds // 60**2
        minutes = (time_seconds - hours*60**2) // 60
        seconds = (time_seconds - hours*60**2) // 60
        return {
            "seconds" : seconds,
            "minutes" : minutes,
            "hours" : hours
        }        
def get_duration_seconds(ticks):
    time_seconds = int(ticks / 10_000_000)
    return time_seconds


class JellyfinApi:
    def __init__(self) -> None:
        settings = JellyfinSettings() # type: ignore[reportCallIssue]
        self.__api_key = settings.api_key.get_secret_value()
        self.__url = settings.url
        self.__username = settings.username
        self.__raw_json = None
    
    def get_session_json(self) ->  list[dict[str,dict]]:
        url = f"{self.__url}/Sessions"
        headers = {
            "Authorization": f"MediaBrowser Token={self.__api_key}",
            "X-Emby-Token": f"MediaBrowser Token={self.__api_key}"
            }
        request = requests.get(url, headers=headers)
        #print(request.status_code)
        return request.json()
    def init_json(self) -> None:
        self.__raw_json = self.get_session_json()


    def parse_session_json(self) -> dict[str,str]:   
        if not self.__raw_json:
            return {"error" : "Cannot connect to jellyfin server"}
            
        session = {}
        now_playing = {}
        for i in range(len(self.__raw_json)):
            if self.__raw_json[i].get("UserName") == self.__username:
                user_session_index = i
                session = self.__raw_json[user_session_index]
                now_playing = session.get("NowPlayingItem")
                break
        if not session:
            return {"error" : "Cannot find your jellyfin user session"}
        if not now_playing:
            return {"error" : "Nothing is playing"}
        data = {
            "username": session.get("UserName"),
            "duration": get_duration_seconds(now_playing.get("RunTimeTicks")),
            "time_passed": get_duration_seconds(session.get("PlayState", {}).get("PositionTicks")),
            "type": now_playing.get("Type"),
            #Path is here for debugging
            #"path": now_playing.get("Path"),
            "name": now_playing.get("Name"),
            "year": now_playing.get("ProductionYear")
        }   
        
        if now_playing.get("Type") == "Audio":
            data.update({
                "album": now_playing.get("Album"),
                "album_id": session.get("PlayState", {}).get("MediaSourceId"),
                "image_tag": now_playing.get("AlbumPrimaryImageTag"),
                "album_artist": now_playing.get("AlbumArtist"),
            })
            data.update({
                "image_url":  f"{self.__url}/Items/{data["album_id"]}/Images/Primary?tag={data['image_tag']}"
            })
        elif now_playing.get("Type") == "Movie":
            data.update({
                "movie_id": session.get("PlayState", {}).get("MediaSourceId"),
                "image_tag": now_playing.get("ImageTags")
            })
            data.update({
                "image_url":  f"{self.__url}/Items/{data["movie_id"]}/Images/Primary?tag={data['image_tag']}"
            })
        elif now_playing.get("Type") == "Episode":
            data.update({
                "image_tag": now_playing.get("ParentLogoImageTag"),
                "season_number": now_playing.get("ParentIndexNumber"),
                "episode_number": now_playing.get("IndexNumber"),
                "season_id": now_playing.get("SeasonId"),                
                "season_name": now_playing.get("SeasonName")
            })
            data.update({
                "image_url":  f"{self.__url}/Items/{data["season_id"]}/Images/Primary?tag={data['image_tag']}"
            }) 
            if int(data["season_number"]) <= 9:
                data["season_number"]= f"0{now_playing.get("ParentIndexNumber")}"
            if int(data["episode_number"]) <= 9:
                data["episode_number"]= f"0{now_playing.get("IndexNumber")}"                

        return data
    def set_raw_json(self, raw_json: list[dict]) -> None:
        self.__raw_json = raw_json    
