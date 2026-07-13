import asyncio

import discord
from discord.ext import commands

from services.guild_settings import get_log_channel
from services.whitelist import is_whitelisted


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_executor(
        self,
        guild: discord.Guild,
        action: discord.AuditLogAction,
        target_id: int,
    ):
        await asyncio.sleep(1)

        try:
            async for entry in guild.audit_logs(
                limit=5,
                action=action,
            ):
                if entry.target and entry.target.id == target_id:
                    return entry.user

        except discord.Forbidden:
            print(
                f"[SECURITY] Missing View Audit Log permission "
                f"in guild {guild.id}"
            )

        except discord.HTTPException as error:
            print(f"[SECURITY] Audit log error: {error}")

        return None

    async def send_security_log(
        self,
        guild: discord.Guild,
        title: str,
        target_name: str,
        target_id: int,
        executor,
        whitelisted: bool,
        action_taken: str,
        action_success: bool,
    ):
        log_channel_id = await get_log_channel(guild.id)

        if log_channel_id is None:
            print(
                f"[SECURITY] No log channel configured "
                f"for guild {guild.id}"
            )
            return

        log_channel = guild.get_channel(log_channel_id)

        if not isinstance(log_channel, discord.TextChannel):
            print(
                f"[SECURITY] Configured log channel "
                f"{log_channel_id} was not found"
            )
            return

        if whitelisted:
            color = discord.Color.green()
        elif action_success:
            color = discord.Color.red()
        else:
            color = discord.Color.orange()

        embed = discord.Embed(
            title=title,
            color=color,
            timestamp=discord.utils.utcnow(),
        )

        embed.add_field(
            name="Channel",
            value=(
                f"Name: `{target_name}`\n"
                f"ID: `{target_id}`"
            ),
            inline=False,
        )

        embed.add_field(
            name="Executor",
            value=(
                f"{executor.mention}\n"
                f"`{executor.id}`"
            ),
            inline=False,
        )

        embed.add_field(
            name="Whitelisted",
            value="✅ Yes" if whitelisted else "❌ No",
            inline=False,
        )

        embed.add_field(
            name="Action Taken",
            value=action_taken,
            inline=False,
        )

        embed.set_footer(text=f"Server: {guild.name}")

        try:
            await log_channel.send(embed=embed)

        except discord.Forbidden:
            print(
                f"[SECURITY] Cannot send messages "
                f"in log channel {log_channel.id}"
            )

        except discord.HTTPException as error:
            print(f"[SECURITY] Failed to send log: {error}")

    # ===========================
    # ANTI CHANNEL DELETE
    # ===========================

    @commands.Cog.listener()
    async def on_guild_channel_delete(
        self,
        deleted_channel: discord.abc.GuildChannel,
    ):
        guild = deleted_channel.guild

        executor = await self.get_executor(
            guild=guild,
            action=discord.AuditLogAction.channel_delete,
            target_id=deleted_channel.id,
        )

        if executor is None:
            return

        if self.bot.user and executor.id == self.bot.user.id:
            return

        whitelisted = await is_whitelisted(
            guild_id=guild.id,
            user_id=executor.id,
        )

        action_taken = "None — user is whitelisted"
        action_success = True

        if not whitelisted:
            try:
                await guild.ban(
                    executor,
                    reason=(
                        "Anti-Nuke: Unauthorized channel deletion | "
                        f"Channel: {deleted_channel.name} "
                        f"({deleted_channel.id})"
                    ),
                    delete_message_seconds=0,
                )

                action_taken = "🔨 User banned"
                action_success = True

            except discord.Forbidden:
                action_taken = (
                    "❌ Ban failed — missing permission "
                    "or bot role is too low"
                )
                action_success = False

            except discord.HTTPException as error:
                action_taken = f"❌ Ban failed — {error}"
                action_success = False

        await self.send_security_log(
            guild=guild,
            title="🚨 Channel Deleted",
            target_name=deleted_channel.name,
            target_id=deleted_channel.id,
            executor=executor,
            whitelisted=whitelisted,
            action_taken=action_taken,
            action_success=action_success,
        )

    # ===========================
    # ANTI CHANNEL CREATE
    # ===========================

    @commands.Cog.listener()
    async def on_guild_channel_create(
        self,
        created_channel: discord.abc.GuildChannel,
    ):
        guild = created_channel.guild

        executor = await self.get_executor(
            guild=guild,
            action=discord.AuditLogAction.channel_create,
            target_id=created_channel.id,
        )

        if executor is None:
            return

        if self.bot.user and executor.id == self.bot.user.id:
            return

        whitelisted = await is_whitelisted(
            guild_id=guild.id,
            user_id=executor.id,
        )

        action_taken = "None — user is whitelisted"
        action_success = True

        if not whitelisted:
            deletion_result = "Created channel deleted"

            try:
                await created_channel.delete(
                    reason="Anti-Nuke: Unauthorized channel creation"
                )

            except discord.Forbidden:
                deletion_result = "Could not delete created channel"
                action_success = False

            except discord.HTTPException:
                deletion_result = "Discord error while deleting channel"
                action_success = False

            try:
                await guild.ban(
                    executor,
                    reason=(
                        "Anti-Nuke: Unauthorized channel creation | "
                        f"Channel: {created_channel.name} "
                        f"({created_channel.id})"
                    ),
                    delete_message_seconds=0,
                )

                action_taken = (
                    f"🔨 User banned\n"
                    f"🗑️ {deletion_result}"
                )

            except discord.Forbidden:
                action_taken = (
                    "❌ Ban failed — missing permission "
                    "or bot role is too low\n"
                    f"🗑️ {deletion_result}"
                )
                action_success = False

            except discord.HTTPException as error:
                action_taken = (
                    f"❌ Ban failed — {error}\n"
                    f"🗑️ {deletion_result}"
                )
                action_success = False

        await self.send_security_log(
            guild=guild,
            title="🚨 Channel Created",
            target_name=created_channel.name,
            target_id=created_channel.id,
            executor=executor,
            whitelisted=whitelisted,
            action_taken=action_taken,
            action_success=action_success,
        )

    # ===========================
    # ANTI ROLE DELETE
    # ===========================

    @commands.Cog.listener()
    async def on_guild_role_delete(
        self,
        deleted_role: discord.Role,
    ):
        guild = deleted_role.guild

        executor = await self.get_executor(
            guild=guild,
            action=discord.AuditLogAction.role_delete,
            target_id=deleted_role.id,
        )

        if executor is None:
            return

        if self.bot.user and executor.id == self.bot.user.id:
            return

        whitelisted = await is_whitelisted(
            guild_id=guild.id,
            user_id=executor.id,
        )

        action_taken = "None — user is whitelisted"
        action_success = True

        if not whitelisted:
            try:
                await guild.ban(
                    executor,
                    reason=(
                        "Anti-Nuke: Unauthorized role deletion | "
                        f"Role: {deleted_role.name} "
                        f"({deleted_role.id})"
                    ),
                    delete_message_seconds=0,
                )

                action_taken = "🔨 User banned"
                action_success = True

            except discord.Forbidden:
                action_taken = (
                    "❌ Ban failed — missing permission "
                    "or bot role is too low"
                )
                action_success = False

            except discord.HTTPException as error:
                action_taken = f"❌ Ban failed — {error}"
                action_success = False

        log_channel_id = await get_log_channel(guild.id)

        if log_channel_id is None:
            return

        log_channel = guild.get_channel(log_channel_id)

        if not isinstance(log_channel, discord.TextChannel):
            return

        if whitelisted:
            color = discord.Color.green()
        elif action_success:
            color = discord.Color.red()
        else:
            color = discord.Color.orange()

        embed = discord.Embed(
            title="🚨 Role Deleted",
            color=color,
            timestamp=discord.utils.utcnow(),
        )

        embed.add_field(
            name="Role",
            value=(
                f"Name: `{deleted_role.name}`\n"
                f"ID: `{deleted_role.id}`"
            ),
            inline=False,
        )

        embed.add_field(
            name="Executor",
            value=(
                f"{executor.mention}\n"
                f"`{executor.id}`"
            ),
            inline=False,
        )

        embed.add_field(
            name="Whitelisted",
            value="✅ Yes" if whitelisted else "❌ No",
            inline=False,
        )

        embed.add_field(
            name="Action Taken",
            value=action_taken,
            inline=False,
        )

        embed.set_footer(text=f"Server: {guild.name}")

        try:
            await log_channel.send(embed=embed)

        except discord.Forbidden:
            print(
                f"[SECURITY] Cannot send messages "
                f"in log channel {log_channel.id}"
            )

        except discord.HTTPException as error:
            print(f"[SECURITY] Failed to send role-delete log: {error}")
async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
