from config import JellyfinSettings
from json_parse import JellyfinApi
from pypresence.presence import Presence
from pypresence.types import ActivityType, StatusDisplayType
from pypresence.exceptions import DiscordNotFound, InvalidPipe, PipeClosed, ResponseTimeout, ConnectionTimeout
import time
from collections import deque


def init_time():
    return  int(time.time())

class JellyfinRPC:
    def __init__(self) -> None:
        self.settings = JellyfinSettings()  # type: ignore[reportCallIssue]
        self.rpc = Presence(self.settings.client_id)
        self.data = {}
        self.last_name = None
        self.intiial_time = 0
        self.discord_connected = False
        self.connect_rpc()     
        self.data_history = deque(maxlen=5)           
        self.rpc_cleared = False        

    def connect_rpc(self) -> bool:
        try:
            self.rpc.connect()
            self.discord_connected = True
            print("Connected to Discord RPC")
            return True
        except (DiscordNotFound, InvalidPipe, PipeClosed, ConnectionTimeout, ResponseTimeout) as e:
            self.discord_connected = False
            print(f"Discord RPC unavailable: {e}")
            return False 
    def safe_rpc_update(self, **kwargs) -> None:
        if not self.discord_connected and not self.connect_rpc():
            return

        try:
            self.rpc.update(**kwargs)
        except (PipeClosed, InvalidPipe, ResponseTimeout, ConnectionTimeout, DiscordNotFound) as e:
            self.discord_connected = False
            print(f"Discord RPC disconnected: {e}")

    def safe_rpc_clear(self) -> None:
        if not self.discord_connected:
            return 
        if self.rpc_cleared:
            return 
        try:
            self.rpc.clear()
            self.rpc_cleared = True        
        except (PipeClosed, InvalidPipe, ResponseTimeout, ConnectionTimeout, DiscordNotFound):
            self.discord_connected = False        
    def time_passed(self) -> tuple[int, int]:
        now = self.intiial_time 
        start = now - int(self.data.get("time_passed", 0))
        end = start + int(self.data.get("duration", 0))
        return start, end
    def refresh_data(self) -> dict[str, str]:
        self.data = {}
        data = JellyfinApi()
        data.init_json()
        return data.parse_session_json()

    def audio_rpc(self) -> None:
        self.safe_rpc_update(
            activity_type=ActivityType.LISTENING,  
            status_display_type=StatusDisplayType.DETAILS,  
            large_text=f"{self.data.get("year")}",
            state=f"{self.data.get("album_artist", None)}",
            details= f"{self.data.get("name", "Unknown media")}",
            large_image=self.data.get("image_url"),
            start=self.time_passed()[0],
            end=self.time_passed()[1],
        )
    def movie_rpc(self) -> None:
        self.safe_rpc_update(
            activity_type=ActivityType.WATCHING,   
            status_display_type=StatusDisplayType.DETAILS,   
            state=f"{self.data.get("year", "")}",
            details= f"{self.data.get("name", "Unknown media")}",
            large_image=self.data.get("image_url"),
            start=self.time_passed()[0],
            end=self.time_passed()[1],
        )
    def show_rpc(self) -> None:
        self.safe_rpc_update(
            activity_type=ActivityType.WATCHING,
            status_display_type=StatusDisplayType.DETAILS,
            details=self.data.get("show_name", "Unknown Show"),
            state=(
                f"S{self.data.get('season_number')}"
                f"E{self.data.get('episode_number')} • "
                f"{self.data.get('name')}"
            ),
            large_image=self.data.get("image_url"),
            large_text=f"{self.data.get('year')}",            
            start=self.time_passed()[0],
            end=self.time_passed()[1],
        )
    def find_type(self) -> None:
        if self.data.get("type"):
            self.rpc_cleared = False
        if self.data.get("type") == "Audio":
            self.audio_rpc()
            print("AUDIO")
        elif self.data.get("type") == "Movie":
            self.movie_rpc()        
        elif self.data.get("type") == "Episode":
            self.show_rpc()             
        else:
            print("Type of Media Not Found")  
  
    def data_is_stale(self) -> bool:
        if len(self.data_history) < 5:
            return False

        return all(item == self.data_history[0] for item in self.data_history)

    def update_presence(self) -> str | None:
        self.data = self.refresh_data()
        self.data_history.append(self.data)

        if "error" in self.data:
            self.safe_rpc_clear()
            print(f"Error: {self.data.get("error")}")
            return None
 
        if self.data_is_stale():
            self.safe_rpc_clear()
            print("Session data unchanged for 5 checks, RPC cleared")
            return None
        
        print(f"Media: {self.data}")
        self.intiial_time = init_time()
        self.find_type()


       
               

 