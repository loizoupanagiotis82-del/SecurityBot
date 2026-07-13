import discord
from discord import app_commands
from discord.ext import commands

from services.whitelist import (
    add_whitelist,
    remove_whitelist,
    is_whitelisted,
)


class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    whitelist = app_commands.Group(
        name="whitelist",
        description="Manage the security whitelist."
    )

    @whitelist.command(
        name="add",
        description="Add a user to the whitelist."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def add(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):
        added = await add_whitelist(
            interaction.guild.id,
            member.id
        )

        if not added:
            await interaction.response.send_message(
                f"⚠️ {member.mention} is already whitelisted.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ {member.mention} has been added to the whitelist."
        )

    @whitelist.command(
        name="remove",
        description="Remove a user from the whitelist."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def remove(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):
        removed = await remove_whitelist(
            interaction.guild.id,
            member.id
        )

        if not removed:
            await interaction.response.send_message(
                "❌ That user isn't whitelisted.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ Removed {member.mention} from the whitelist."
        )


async def setup(bot):
    await bot.add_cog(Whitelist(bot))
