import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.moderation = True

class SecurityBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents
        )

    async def setup_hook(self):
        print("Loading Cogs...")

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands.")

bot = SecurityBot()

@bot.event
async def on_ready():
    print("=" * 50)
    print(f"Logged in as {bot.user}")
    print(f"Guilds : {len(bot.guilds)}")
    print("=" * 50)

bot.run(TOKEN)
