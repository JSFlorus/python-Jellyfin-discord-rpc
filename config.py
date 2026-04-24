from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class JellyfinSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    url: str = Field(alias="JELLYFIN_URL")
    api_key: SecretStr = Field(alias="JELLYFIN_API_KEY")
    username: str = Field(alias="JELLYFIN_USER")
    client_id: str = Field(alias="DISCORD_CLIENT_ID")
    image_asset: str = Field(alias="ART_ASSET")
    poll_rate: int = Field(alias="DISCORD_UPDATE_INTERVAL_SECS")

 


 
# settings = JellyfinSettings() # type: ignore[reportCallIssue]
# #print(settings.model_dump())


# # real_key = settings.api_key.get_secret_value()