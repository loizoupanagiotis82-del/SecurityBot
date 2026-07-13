import discord
from discord import app_commands
from discord.ext import commands

from services.warnings import (
    add_warning,
    clear_warnings,
    get_warnings,
)
from utils.checks import can_moderate


class Warnings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ===========================
    # WARN
    # ===========================

    @app_commands.command(
        name="warn",
        description="Warn a member."
    )
    @app_commands.describe(
        member="The member to warn.",
        reason="Reason for the warning."
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided.",
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ This command can only be used in a server.",
                ephemeral=True,
            )
            return

        allowed, message = await can_moderate(interaction, member)

        if not allowed:
            await interaction.response.send_message(
                message,
                ephemeral=True,
            )
            return

        try:
            warning = await add_warning(
                guild_id=guild.id,
                user_id=member.id,
                moderator_id=interaction.user.id,
                reason=reason,
            )

            embed = discord.Embed(
                title="⚠️ Member Warned",
                color=discord.Color.orange(),
            )

            embed.add_field(
                name="Warning ID",
                value=f"`{warning.id}`",
                inline=False,
            )

            embed.add_field(
                name="Member",
                value=f"{member.mention}\n`{member.id}`",
                inline=False,
            )

            embed.add_field(
                name="Moderator",
                value=interaction.user.mention,
                inline=False,
            )

            embed.add_field(
                name="Reason",
                value=reason,
                inline=False,
            )

            await interaction.response.send_message(embed=embed)

        except Exception as error:
            print(f"Warn error: {error}")

            await interaction.response.send_message(
                "❌ Failed to save the warning.",
                ephemeral=True,
            )

    @warn.error
    async def warn_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ):
        if isinstance(error, app_commands.MissingPermissions):
            message = "❌ You need the **Moderate Members** permission."
        else:
            message = "❌ An unexpected error occurred while using `/warn`."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(
                message,
                ephemeral=True,
            )

    # ===========================
    # WARNINGS
    # ===========================

    @app_commands.command(
        name="warnings",
        description="Show a member's warnings."
    )
    @app_commands.describe(
        member="The member whose warnings you want to view."
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ This command can only be used in a server.",
                ephemeral=True,
            )
            return

        member_warnings = await get_warnings(
            guild_id=guild.id,
            user_id=member.id,
        )

        if not member_warnings:
            await interaction.response.send_message(
                f"✅ {member.mention} has no warnings.",
                ephemeral=True,
            )
            return

        lines = []

        for warning in member_warnings[:15]:
            lines.append(
                f"**#{warning.id}** — {warning.reason}\n"
                f"Moderator: <@{warning.moderator_id}>"
            )

        embed = discord.Embed(
            title=f"⚠️ Warnings for {member}",
            description="\n\n".join(lines),
            color=discord.Color.orange(),
        )

        embed.set_footer(
            text=f"Total warnings: {len(member_warnings)}"
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )

    # ===========================
    # CLEAR WARNINGS
    # ===========================

    @app_commands.command(
        name="clearwarnings",
        description="Clear all warnings from a member."
    )
    @app_commands.describe(
        member="The member whose warnings will be cleared."
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def clearwarnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ This command can only be used in a server.",
                ephemeral=True,
            )
            return

        deleted_count = await clear_warnings(
            guild_id=guild.id,
            user_id=member.id,
        )

        if deleted_count == 0:
            await interaction.response.send_message(
                f"✅ {member.mention} had no warnings.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="✅ Warnings Cleared",
            description=(
                f"Removed **{deleted_count}** warning(s) "
                f"from {member.mention}."
            ),
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Warnings(bot))
