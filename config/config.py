# config/config.py
from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv

@dataclass
class Config:
    DISCORD_TOKEN: str
    API_KEY: str
    DESIGNATED_CHANNELS: List[int]
    GUILD_TEST_ID: str
    OWNER_ID: str
    LOCAL_CLIENT_URL: str
    MODEL_NAME: str
    
    # Bot specific configs
    ACTIVITY_TIMER: int = 300
    DISCORD_CHARACTER_LIMIT: int = 2000
    MESSAGE_THRESHOLD: int = 5000
    SEND_LIMIT: int = 10000
    MAX_CACHED_IMAGES: int = 10

def load_config() -> Config:
    try:
        load_dotenv()
    except Exception as e:
        print("No .env file found")

    try:
        return Config(
            DISCORD_TOKEN=os.getenv('DISCORD_TOKEN'),
            API_KEY=os.getenv('API_KEY'),
            DESIGNATED_CHANNELS=[int(channel) for channel in os.getenv("DESIGNATED_CHANNELS").split(", ")],
            GUILD_TEST_ID=os.getenv("GUILD_TEST_ID"),
            OWNER_ID=os.getenv("OWNER_ID"),
            LOCAL_CLIENT_URL=os.getenv("LOCAL_CLIENT_URL", ""),
            MODEL_NAME=os.getenv("MODEL_NAME")
        )
    except (KeyError, AttributeError) as e:
        raise ValueError(f"Missing required environment variables: {str(e)}")
