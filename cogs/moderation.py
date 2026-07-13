from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from utils.checks import can_moderate


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ===========================
    # BAN
    # ===========================

    @app_commands.command(
        name="ban",
        description="Ban a member from the server."
    )
    @app_commands.describe(
        member="The member to ban.",
        reason="Reason for the ban."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):
        allowed, message = await can_moderate(interaction, member)

        if not allowed:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )
            return

        try:
            await member.ban(
                reason=(
                    f"{reason} | Moderator: "
                    f"{interaction.user} ({interaction.user.id})"
                )
            )

            embed = discord.Embed(
                title="🔨 Member Banned",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Member",
                value=f"{member.mention}\n`{member.id}`",
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=f"{interaction.user.mention}\n`{interaction.user.id}`",
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
                "❌ Discord returned an error while banning this member.",
                ephemeral=True
            )

    @ban.error
    async def ban_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            message = "❌ You need the **Ban Members** permission."
        else:
            message = "❌ An unexpected error occurred while using `/ban`."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )

    # ===========================
    # KICK
    # ===========================

    @app_commands.command(
        name="kick",
        description="Kick a member from the server."
    )
    @app_commands.describe(
        member="The member to kick.",
        reason="Reason for the kick."
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):
        allowed, message = await can_moderate(interaction, member)

        if not allowed:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )
            return

        try:
            await member.kick(
                reason=(
                    f"{reason} | Moderator: "
                    f"{interaction.user} ({interaction.user.id})"
                )
            )

            embed = discord.Embed(
                title="👢 Member Kicked",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="Member",
                value=f"{member.mention}\n`{member.id}`",
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=f"{interaction.user.mention}\n`{interaction.user.id}`",
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
                "❌ I do not have permission to kick this member.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord returned an error while kicking this member.",
                ephemeral=True
            )

    @kick.error
    async def kick_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            message = "❌ You need the **Kick Members** permission."
        else:
            message = "❌ An unexpected error occurred while using `/kick`."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )

    # ===========================
    # TIMEOUT
    # ===========================

    @app_commands.command(
        name="timeout",
        description="Timeout a member."
    )
    @app_commands.describe(
        member="The member to timeout.",
        minutes="Timeout duration in minutes.",
        reason="Reason for the timeout."
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        reason: str = "No reason provided."
    ):
        allowed, message = await can_moderate(interaction, member)

        if not allowed:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )
            return

        try:
            await member.timeout(
                timedelta(minutes=minutes),
                reason=(
                    f"{reason} | Moderator: "
                    f"{interaction.user} ({interaction.user.id})"
                )
            )

            embed = discord.Embed(
                title="⏳ Member Timed Out",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="Member",
                value=f"{member.mention}\n`{member.id}`",
                inline=False
            )

            embed.add_field(
                name="Duration",
                value=f"{minutes} minute(s)",
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=f"{interaction.user.mention}\n`{interaction.user.id}`",
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
                "❌ I do not have permission to timeout this member.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord returned an error while timing out this member.",
                ephemeral=True
            )

    @timeout.error
    async def timeout_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            message = "❌ You need the **Moderate Members** permission."
        else:
            message = "❌ An unexpected error occurred while using `/timeout`."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )

    # ===========================
    # UNTIMEOUT
    # ===========================

    @app_commands.command(
        name="untimeout",
        description="Remove a member's timeout."
    )
    @app_commands.describe(
        member="The member whose timeout will be removed.",
        reason="Reason for removing the timeout."
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):
        allowed, message = await can_moderate(interaction, member)

        if not allowed:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )
            return

        try:
            await member.timeout(
                None,
                reason=(
                    f"{reason} | Moderator: "
                    f"{interaction.user} ({interaction.user.id})"
                )
            )

            embed = discord.Embed(
                title="✅ Timeout Removed",
                color=discord.Color.green()
            )

            embed.add_field(
                name="Member",
                value=f"{member.mention}\n`{member.id}`",
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=f"{interaction.user.mention}\n`{interaction.user.id}`",
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
                "❌ I do not have permission to remove this timeout.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord returned an error while removing the timeout.",
                ephemeral=True
            )

    @untimeout.error
    async def untimeout_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            message = "❌ You need the **Moderate Members** permission."
        else:
            message = "❌ An unexpected error occurred while using `/untimeout`."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(
                message,
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
