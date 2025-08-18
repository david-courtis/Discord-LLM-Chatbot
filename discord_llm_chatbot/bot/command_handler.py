from typing import TYPE_CHECKING

from discord.ext.commands import Context

if TYPE_CHECKING:
    from .bot import MyBot


class CommandHandler:
    def __init__(self, bot: "MyBot"):
        self.bot = bot

        # self.SPIN_PROMPTS = [

        # ]

    def setup_commands(self):
        """Sets up bot commands."""

        @self.bot.hybrid_command(
            name="clear", description="Forget conversation history in the channel"
        )
        async def clear_cache(ctx: Context):
            await self.clear_cache(ctx)

        @self.bot.hybrid_command(name="sync", description="Sync slash commands")
        async def sync(ctx: Context):
            await self.sync_commands(ctx)

        @self.bot.hybrid_command(name="creator", description="Who created me?")
        async def creator(ctx: Context):
            await self.say_creator(ctx)

        # @self.bot.hybrid_command(
        #     name="spin",
        #     description="Spin the bottle drinking game!"
        # )
        # @commands.describe(user="User to apply the spin result to (optional)")
        # async def spin_command(ctx, user: discord.Member = None):
        #     await self.spin_game(ctx, user)

    async def clear_cache(self, ctx: Context):
        """Clears the cache for the current channel."""
        await ctx.defer()
        server_channel = f"{ ctx.guild}{ctx.channel}"
        if server_channel in self.bot.cache and self.bot.cache[server_channel]:
            self.bot.cache[server_channel] = []
            await ctx.send("I have suddenly developed amnesia, UwU!", ephemeral=False)
        else:
            await ctx.send(
                "No history found for this channel, b-baka!", ephemeral=False
            )

    async def sync_commands(self, ctx: Context):
        """Syncs slash commands."""
        await ctx.defer()
        if str(ctx.author.id) == self.bot.config.OWNER_ID:
            await self.bot.tree.sync()
            await ctx.send("Command tree synced.")
        else:
            await ctx.send("You must be the owner to use this command!")

    async def say_creator(self, ctx: Context):
        """Sends a message with the bot creator's info."""
        await ctx.defer()
        await ctx.send(f"I was created by <@!{ self.bot.config.OWNER_ID}>!")
        await ctx.send(f"I was created by <@!{ self.bot.config.OWNER_ID}>!")

    # async def spin_game(self, ctx: commands.Context, user: discord.Member = None):
    #     """Randomly picks a spin-the-bottle prompt and directs it at a user or the invoker."""
    #     await ctx.defer()
    #     target = user if user else ctx.author
    #     chosen_prompt = random.choice(self.SPIN_PROMPTS)
    #     response = f"{target.mention}, your spin prompt is: **{chosen_prompt}**"
    #     await ctx.send(response, ephemeral=False)
