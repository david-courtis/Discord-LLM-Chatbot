# bot/fun_commands.py
import random

import numpy as np
from discord.message import Message
from scipy.stats import triang

from .bot import MyBot


class FunCommands:
    def __init__(self, bot: MyBot):
        self.bot = bot

    async def chubcheck(self, message: Message):
        """Handles the chubcheck command."""
        nickname = message.author.display_name
        chub_percentage = random.randint(0, 100)
        freak_percentage = random.randint(0, 100)
        response = f"{ nickname} is at {chub_percentage}% chub & {freak_percentage}% freak 👅💦"
        await message.channel.send(response)

    async def chugmeter(self, message: Message):
        """Handles the chugmeter command."""
        nickname = message.author.display_name
        loc, scale = 0.1, 0.9
        c = 0
        tri_dist = triang(c, loc=loc, scale=scale)
        raw_samples = tri_dist.rvs(size=1000)
        skew_factor = 0.1
        exp_skewed_samples = np.exp(-skew_factor * (raw_samples - loc) / scale)
        normalized_samples = (
            raw_samples * exp_skewed_samples / np.max(exp_skewed_samples)
        )
        chug_time = int(np.random.choice(normalized_samples) * 100)
        response = f"{ nickname} chugs {chug_time}% of their drink! 🍺😈"
        await message.channel.send(response)
