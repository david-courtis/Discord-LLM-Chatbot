# bot/bot.py
import discord
from discord.ext import commands
from typing import Dict

from config.config import Config
from bot.message_handler import MessageHandler
from bot.activity_handler import ActivityHandler
from bot.command_handler import CommandHandler
from bot.fun_commands import FunCommands

class MyBot(commands.Bot):
    def __init__(self, config: Config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True

        super().__init__(command_prefix="$", intents=intents)

        self.config = config
        self.cache: Dict[str, list] = {}

        # Initialize handlers
        self.message_handler = MessageHandler(self)
        self.activity_handler = ActivityHandler(self)
        self.command_handler = CommandHandler(self)
        self.fun_commands = FunCommands(self)

        # Setup commands
        self.command_handler.setup_commands()

    async def on_ready(self):
        """Called when the bot is ready and connected to Discord."""
        print(f"Logged in as { self.user}!")
        await self.tree.sync()
        await self.activity_handler.start()

    async def on_message(self, message):
        """Handles incoming messages."""
        if message.author == self.user or not message.content.strip():
            return

        print(f'Message from { message.author}, {message.guild}, {message.channel}: {message.content}')

        # Handle fun commands
        if message.content.startswith('!chubmeter'):
            await self.fun_commands.chubcheck(message)
            return
        elif message.content.startswith('!chugmeter'):
            await self.fun_commands.chugmeter(message)
            return

        await self.message_handler.handle_message(message)
