import asyncio

import discord
from discord.ext import commands

from services.guild_settings import get_log_channel
from services.whitelist import is_whitelisted


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(
        self,
        deleted_channel: discord.abc.GuildChannel,
    ):
        guild = deleted_channel.guild

        # Περιμένουμε λίγο ώστε να ενημερωθούν τα Audit Logs.
        await asyncio.sleep(1)

        executor = None

        try:
            async for entry in guild.audit_logs(
                limit=5,
                action=discord.AuditLogAction.channel_delete,
            ):
                if entry.target and entry.target.id == deleted_channel.id:
                    executor = entry.user
                    break

        except discord.Forbidden:
            print(
                f"[SECURITY] Missing View Audit Log permission "
                f"in guild {guild.id}"
            )
            return

        except discord.HTTPException as error:
            print(f"[SECURITY] Audit log error: {error}")
            return

        if executor is None:
            print(
                f"[SECURITY] Could not identify who deleted "
                f"channel {deleted_channel.name}"
            )
            return

        # Δεν τιμωρούμε το ίδιο το bot.
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
                    "❌ Ban failed — bot role is too low "
                    "or Ban Members permission is missing"
                )
                action_success = False

            except discord.HTTPException as error:
                action_taken = f"❌ Ban failed — Discord error: {error}"
                action_success = False

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
            title="🚨 Channel Deleted",
            color=color,
            timestamp=discord.utils.utcnow(),
        )

        embed.add_field(
            name="Channel",
            value=(
                f"Name: `{deleted_channel.name}`\n"
                f"ID: `{deleted_channel.id}`"
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
                f"[SECURITY] Missing permission to send messages "
                f"in log channel {log_channel.id}"
            )

        except discord.HTTPException as error:
            print(f"[SECURITY] Failed to send log embed: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
