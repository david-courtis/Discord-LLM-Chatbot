# utils/openai_client.py
from openai import OpenAI
from typing import List, Dict
import time

from ..config.config import Config

class OpenAIClient:
    def __init__(self, config: Config):
        base_url = config.LOCAL_CLIENT_URL if config.LOCAL_CLIENT_URL else None
        self.client = OpenAI(api_key=config.OPENAI_API_KEY, base_url=base_url)

    def send_message(self, messages: List[Dict[str, str]]) -> str:
        default_response = "Sorry I am kinda sleepy right now, can you ask me later?"

        for _ in range(3):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(3)
                continue

        return default_response
