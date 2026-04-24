from rpc import JellyfinRPC
import time
from pypresence.presence import Presence
from config import JellyfinSettings

settings = JellyfinSettings() # type: ignore[reportCallIssue]
def main() -> None:
    app = JellyfinRPC()
    while True:
        app.update_presence()
        time.sleep(settings.poll_rate)


if __name__ == "__main__":
    main()

