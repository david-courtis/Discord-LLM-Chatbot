from discord.ext import commands

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot

    def setup_commands(self):
        """Sets up bot commands."""
        @self.bot.hybrid_command(name="clear", description="Forget conversation history in the channel")
        async def clear_cache(ctx):
            await self.clear_cache(ctx)

        @self.bot.hybrid_command(name="sync", description="Sync slash commands")
        async def sync(ctx):
            await self.sync_commands(ctx)

        @self.bot.hybrid_command(name="creator", description="Who created me?")
        async def creator(ctx):
            await self.say_creator(ctx)

    async def clear_cache(self, ctx: commands.Context):
        """Clears the message cache for the current channel."""
        server_channel = f"{ ctx.guild}{ctx.channel}"
        if server_channel in self.cache and self.cache[server_channel]:
            self.cache[server_channel] = []
            await ctx.reply("I have suddenly developed amnesia, UwU!", ephemeral=False)
        else:
            await ctx.reply("No history found for this channel, b-baka!", ephemeral=False)

    async def sync_commands(self, ctx: commands.Context):
        """Syncs slash commands."""
        if str(ctx.author.id) == self.config.OWNER_ID:
            await self.tree.sync()
            await ctx.send('Command tree synced.')
        else:
            await ctx.send('You must be the owner to use this command!')

    async def say_creator(self, ctx: commands.Context):
        """Sends a message with the bot creator's info."""
        await ctx.send(f'I was created by <@!{ self.config.OWNER_ID}>!')
