import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(
        self,
        channel: discord.abc.GuildChannel
    ):

        print(
            f"[ANTI-NUKE] Channel deleted: {channel.name}"
        )


async def setup(bot):
    await bot.add_cog(Events(bot))
