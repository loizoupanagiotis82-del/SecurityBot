import discord
from discord.ext import commands
from discord import app_commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ban",
        description="Ban a member from the server."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):

        if member == interaction.user:
            await interaction.response.send_message(
                "❌ You can't ban yourself.",
                ephemeral=True
            )
            return

        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "❌ This member has an equal or higher role than you.",
                ephemeral=True
            )
            return

        try:
            await member.ban(reason=reason)

            embed = discord.Embed(
                title="🔨 Member Banned",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Member",
                value=f"{member} ({member.id})",
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=interaction.user.mention,
                inline=False
            )

            embed.add_field(
                name="Reason",
                value=reason,
                inline=False
            )

            await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to ban that member.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
