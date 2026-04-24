import json

from json_parse import JellyfinApi
def test_parse_playig_audio_session(monkeypatch):
    # Set env vars for test

    monkeypatch.setenv("JELLYFIN_USER", "test_user")

    api = JellyfinApi()

    with open("tests/audio_playing.json") as f:
        sample = json.load(f)

    api.set_raw_json(sample)

    result = api.parse_session_json()

    assert result["username"] == "test_user"
    assert result["type"] == "Audio"
    assert result["name"] == "Test Song"
    assert result["album"] == "Test Album"
    assert result["album_artist"] == "Test Artist"

def test_parse_playig_movie_session(monkeypatch):
    monkeypatch.setenv("JELLYFIN_USER", "test_user")

    api = JellyfinApi()

    with open("tests/movie_playing.json") as f:
        sample = json.load(f)

    api.set_raw_json(sample)

    result = api.parse_session_json()

    assert result["username"] == "test_user"
    assert result["type"] == "Movie"
    assert result["name"] == "Test Movie"
    assert result["year"] == 2024
    assert result["movie_id"] == "fake-movie-id"

def test_parse_playing_show_session(monkeypatch):
    import json
    from json_parse import JellyfinApi

    monkeypatch.setenv("JELLYFIN_USER", "test_user")

    api = JellyfinApi()

    with open("tests/show_playing.json") as f:
        sample = json.load(f)

    api.set_raw_json(sample)

    result = api.parse_session_json()

    assert result["username"] == "test_user"
    assert result["type"] == "Episode"
    assert result["name"] == "Test Episode"
    assert result["season_name"] == "Season 1"
    assert result["season_number"] == "01"
    assert result["episode_number"] == "01"

def test_parse_playing_show2_session(monkeypatch):
    import json
    from json_parse import JellyfinApi

    monkeypatch.setenv("JELLYFIN_USER", "test_user")

    api = JellyfinApi()

    with open("tests/show2_playing.json") as f:
        sample = json.load(f)

    api.set_raw_json(sample)

    result = api.parse_session_json()

    assert result["username"] == "test_user"
    assert result["type"] == "Episode"
    assert result["name"] == "Test Episode"
    assert result["season_name"] == "Season 12"
    assert result["season_number"] == 12
    assert result["episode_number"] == 10


def test_parse_nothing_playing_session(monkeypatch):
    import json
    from json_parse import JellyfinApi

    monkeypatch.setenv("JELLYFIN_USER", "test_user")

    api = JellyfinApi()

    with open("tests/not_playing.json") as f:
        sample = json.load(f)

    api.set_raw_json(sample)

    result = api.parse_session_json()

    assert result["error"] == "Nothing is playing"