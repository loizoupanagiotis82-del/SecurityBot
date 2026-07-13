import discord

from discord import app_commands
from discord.ext import commands

from services.guild_settings import set_log_channel


class Security(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setlog",
        description="Set the security log channel."
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def setlog(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
    ):

        await set_log_channel(
            interaction.guild.id,
            channel.id
        )

        embed = discord.Embed(
            title="✅ Log Channel Updated",
            description=f"Logs will now be sent to {channel.mention}.",
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Security(bot))
