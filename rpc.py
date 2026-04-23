from config import JellyfinSettings
from json_parse import JellyfinApi
from pypresence.presence import Presence
from pypresence.types import ActivityType, StatusDisplayType

import time
def init_time():
    return  int(time.time())
class JellyfinRPC:
    def __init__(self) -> None:
        self.settings = JellyfinSettings()  # type: ignore[reportCallIssue]
        self.rpc = Presence(self.settings.client_id)
        self.rpc.connect()
        self.data = {}
        self.last_name = None
        self.intiial_time = 0
 
    def time_passed(self) -> tuple[int, int]:
        now = self.intiial_time 
        start = now - int(self.data.get("time_passed", 0))
        end = start + int(self.data.get("duration", 0))
        return start, end
    def refresh_data(self) -> dict[str, str]:
        self.data = {}
        data = JellyfinApi().parse_session_json()
        return data
    def audio_rpc(self) -> None:
        self.rpc.update(
            activity_type=ActivityType.LISTENING,  
            status_display_type=StatusDisplayType.DETAILS,  
            large_text=f"{self.data.get("year")}",
            state=f"{self.data.get("album_artist", None)}",
            details= f"{self.data.get("name", "Unknown media")}",
            large_image="server",
            start=self.time_passed()[0],
            end=self.time_passed()[1],
        )
    def movie_rpc(self) -> None:
        self.rpc.update(
            activity_type=ActivityType.WATCHING,   
            status_display_type=StatusDisplayType.DETAILS,   
            large_text=f"{self.data.get("year")}",
            details= f"{self.data.get("name", "Unknown media")}",
            large_image="server",
            start=self.time_passed()[0],
            end=self.time_passed()[1],
        )
    def show_rpc(self) -> None:
        self.rpc.update(
            activity_type=ActivityType.WATCHING,  
            status_display_type=StatusDisplayType.DETAILS,   
            large_text=f"{self.data.get("year")}",
            details= f"{self.data.get("name", "Unknown media")}",
            state=f"{self.data.get("album_artist", None)}",
            large_image="server",
            start=self.time_passed()[0],
            end=self.time_passed()[1],
        )        
    def find_type(self) -> None:
        if self.data.get("type") == "Audio":
            self.audio_rpc()
            print("AUDIO")
        elif self.data.get("type") == "Movie":
            self.movie_rpc()        
        elif self.data.get("type") == "Show":
            self.show_rpc()             
        else:
            print("Type of Media Not Found")  
  

    def update_presence(self) -> str | None:
        self.data = self.refresh_data()
        if "error" in self.data:
            self.rpc.clear()
            print(f"Jellyfin error: {self.data.get("error")}")
            return None
 
        print(f"Media: {self.data}")
        self.intiial_time = init_time()
        self.find_type()


       
               

 