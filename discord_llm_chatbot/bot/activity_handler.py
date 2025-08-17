# bot/activity_handler.py
import asyncio
import threading
import discord

from .activities import ActivityManager

class ActivityHandler:
    def __init__(self, bot):
        self.bot = bot
        self.activity_manager = ActivityManager()
        self.loop = None

    async def start(self):
        """Starts the activity system."""
        self.loop = asyncio.get_event_loop()
        await self.set_random_activity()
        self.start_activity_timer()

    def start_activity_timer(self):
        """Starts the activity timer."""
        self.schedule_next_activity_update()

    def schedule_next_activity_update(self):
        """Schedules the next activity update."""
        timer = threading.Timer(self.bot.config.ACTIVITY_TIMER, self.threaded_activity_update)
        timer.daemon = True
        timer.start()

    def threaded_activity_update(self):
        """Updates the bot's activity in a separate thread."""
        asyncio.run_coroutine_threadsafe(self.set_random_activity(), self.loop)
        self.schedule_next_activity_update()

    async def set_random_activity(self):
        """Sets a random activity for the bot."""
        activity_type, action = self.activity_manager.get_random_activity()
        await self.bot.change_presence(activity=discord.Activity(type=activity_type, name=action))
