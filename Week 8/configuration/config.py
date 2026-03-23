from pydantic import BaseModel
from pydantic_settings import BaseSettings

class ServerSettings(BaseSettings):
    api_key:str = 'c0be3e73b2f542a296dccaa25dedea7a'
    endpoint:str = 'https://api-v3.mbta.com/'

class Message(BaseModel):
    message:str