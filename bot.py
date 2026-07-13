import os

import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN environment variable.")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.moderation = True


class SecurityBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
        )

    async def setup_hook(self):
        print("Loading cogs...")

        for filename in os.listdir("./cogs"):
            if not filename.endswith(".py"):
                continue

            # Δεν φορτώνουμε αρχεία όπως __init__.py
            if filename.startswith("_"):
                continue

            extension = f"cogs.{filename[:-3]}"
            await self.load_extension(extension)
            print(f"Loaded {extension}")

        if DEV_GUILD_ID:
            guild = discord.Object(id=int(DEV_GUILD_ID))

            # Αντιγράφει τα global commands στον test server.
            self.tree.copy_global_to(guild=guild)

            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to test server.")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} global commands.")


bot = SecurityBot()


@bot.event
async def on_ready():
    print("=" * 50)
    print(f"Logged in as {bot.user}")
    print(f"Guilds: {len(bot.guilds)}")
    print("=" * 50)


bot.run(TOKEN)
