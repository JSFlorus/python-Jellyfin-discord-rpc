from rpc import JellyfinRPC
import time
from pypresence.presence import Presence
from config import JellyfinSettings


def main() -> None:
    app = JellyfinRPC()
    while True:
        app.update_presence()
        time.sleep(10)


if __name__ == "__main__":
    main()

