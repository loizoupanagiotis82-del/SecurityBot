import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --------------------
    # /ban
    # --------------------

    @app_commands.command(
        name="ban",
        description="Ban a member from the server."
    )
    @app_commands.describe(
        member="The member you want to ban.",
        reason="The reason for the ban."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ This command can only be used inside a server.",
                ephemeral=True
            )
            return

        moderator = interaction.user

        if not isinstance(moderator, discord.Member):
            await interaction.response.send_message(
                "❌ I could not verify your server permissions.",
                ephemeral=True
            )
            return

        if member == moderator:
            await interaction.response.send_message(
                "❌ You cannot ban yourself.",
                ephemeral=True
            )
            return

        if member.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ You cannot ban the bot.",
                ephemeral=True
            )
            return

        if member == guild.owner:
            await interaction.response.send_message(
                "❌ You cannot ban the server owner.",
                ephemeral=True
            )
            return

        if (
            moderator != guild.owner
            and member.top_role >= moderator.top_role
        ):
            await interaction.response.send_message(
                "❌ That member has an equal or higher role than you.",
                ephemeral=True
            )
            return

        bot_member = guild.me

        if bot_member is None:
            await interaction.response.send_message(
                "❌ I could not verify my server permissions.",
                ephemeral=True
            )
            return

        if member.top_role >= bot_member.top_role:
            await interaction.response.send_message(
                "❌ My role must be above that member's highest role.",
                ephemeral=True
            )
            return

        try:
            await member.ban(
                reason=(
                    f"{reason} | Moderator: "
                    f"{moderator} ({moderator.id})"
                )
            )

            embed = discord.Embed(
                title="🔨 Member banned",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Member",
                value=f"{member.mention}\n`{member.id}`",
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=f"{moderator.mention}\n`{moderator.id}`",
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
                "❌ I do not have permission to ban that member.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord returned an error while banning that member.",
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

    # --------------------
    # /kick
    # --------------------

    @app_commands.command(
        name="kick",
        description="Kick a member from the server."
    )
    @app_commands.describe(
        member="The member you want to kick.",
        reason="The reason for the kick."
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided."
    ):
        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ This command can only be used inside a server.",
                ephemeral=True
            )
            return

        moderator = interaction.user

        if not isinstance(moderator, discord.Member):
            await interaction.response.send_message(
                "❌ I could not verify your server permissions.",
                ephemeral=True
            )
            return

        if member == moderator:
            await interaction.response.send_message(
                "❌ You cannot kick yourself.",
                ephemeral=True
            )
            return

        if member.id == self.bot.user.id:
            await interaction.response.send_message(
                "❌ You cannot kick the bot.",
                ephemeral=True
            )
            return

        if member == guild.owner:
            await interaction.response.send_message(
                "❌ You cannot kick the server owner.",
                ephemeral=True
            )
            return

        if (
            moderator != guild.owner
            and member.top_role >= moderator.top_role
        ):
            await interaction.response.send_message(
                "❌ That member has an equal or higher role than you.",
                ephemeral=True
            )
            return

        bot_member = guild.me

        if bot_member is None:
            await interaction.response.send_message(
                "❌ I could not verify my server permissions.",
                ephemeral=True
            )
            return

        if member.top_role >= bot_member.top_role:
            await interaction.response.send_message(
                "❌ My role must be above that member's highest role.",
                ephemeral=True
            )
            return

        try:
            await member.kick(
                reason=(
                    f"{reason} | Moderator: "
                    f"{moderator} ({moderator.id})"
                )
            )

            embed = discord.Embed(
                title="👢 Member kicked",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="Member",
                value=f"{member.mention}\n`{member.id}`",
                inline=False
            )

            embed.add_field(
                name="Moderator",
                value=f"{moderator.mention}\n`{moderator.id}`",
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
                "❌ I do not have permission to kick that member.",
                ephemeral=True
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord returned an error while kicking that member.",
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


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
