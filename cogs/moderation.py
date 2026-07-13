import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
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
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ This command can only be used in a server.",
                ephemeral=True
            )
            return

        if member == interaction.user:
            await interaction.response.send_message(
                "❌ You cannot ban yourself.",
                ephemeral=True
            )
            return

        if member == interaction.guild.owner:
            await interaction.response.send_message(
                "❌ You cannot ban the server owner.",
                ephemeral=True
            )
            return

        if (
            interaction.user != interaction.guild.owner
            and member.top_role >= interaction.user.top_role
        ):
            await interaction.response.send_message(
                "❌ This member has an equal or higher role than you.",
                ephemeral=True
            )
            return

        bot_member = interaction.guild.me

        if bot_member is None or member.top_role >= bot_member.top_role:
            await interaction.response.send_message(
                "❌ My role must be above the member's highest role.",
                ephemeral=True
            )
            return

        try:
            await member.ban(
                reason=f"{reason} | Moderator: {interaction.user}"
            )

            embed = discord.Embed(
                title="🔨 Member banned",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Member",
                value=f"{member} (`{member.id}`)",
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
                "❌ I do not have permission to ban this member.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord returned an error while banning the member.",
                ephemeral=True
            )

    @ban.error
    async def ban_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You need the Ban Members permission.",
                ephemeral=True
            )
            return

        raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
