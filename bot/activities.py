# bot/activities.py
import discord
import random
from typing import List, Tuple, Dict, Any

class ActivityManager:
    def __init__(self):
        self.activity_list = [
            {
                "type": discord.ActivityType.watching,
                "actions": ["the lazer shine!", "the mouse on screen!", "Wavy snore!", "a spider on the wall!"]
            },
            {
                "type": discord.ActivityType.listening,
                "actions": ["the birds!", "the rain!", "the music!", "the TV!"]
            },
            {
                "type": discord.ActivityType.playing,
                "actions": ["with the ball!", "with the yarn!", "with the mouse!", "with the lazer!"]
            },
            {
                "type": discord.ActivityType.competing,
                "actions": ["fastest pounce!", "best zoomies", "loudest mew!"]
            },
        ]
    
    def get_random_activity(self) -> Tuple[discord.ActivityType, str]:
        activity = random.choice(self.activity_list)
        action = random.choice(activity['actions'])
        return activity['type'], action
