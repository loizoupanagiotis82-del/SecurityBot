import os

import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="ping", description="Check if the bot is online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

bot.run(TOKEN)
