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

        guild = channel.guild

        try:
            async for entry in guild.audit_logs(
                limit=1,
                action=discord.AuditLogAction.channel_delete
            ):

                print("=" * 40)
                print("[ANTI-NUKE]")
                print(f"Channel : {channel.name}")
                print(f"Deleted By : {entry.user}")
                print(f"User ID : {entry.user.id}")
                print("=" * 40)

        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Events(bot))
