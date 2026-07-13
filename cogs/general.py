import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Shows the bot latency.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{latency}ms**",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Shows information about a user.")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):

        member = member or interaction.user

        embed = discord.Embed(
            title=f"{member}",
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="User ID",
            value=member.id,
            inline=False
        )

        embed.add_field(
            name="Joined Server",
            value=f"<t:{int(member.joined_at.timestamp())}:F>",
            inline=False
        )

        embed.add_field(
            name="Account Created",
            value=f"<t:{int(member.created_at.timestamp())}:F>",
            inline=False
        )

        embed.add_field(
            name="Top Role",
            value=member.top_role.mention,
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Shows server information.")
    async def serverinfo(self, interaction: discord.Interaction):

        guild = interaction.guild

        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.blue()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(
            name="Owner",
            value=f"<@{guild.owner_id}>",
            inline=True
        )

        embed.add_field(
            name="Members",
            value=guild.member_count,
            inline=True
        )

        embed.add_field(
            name="Channels",
            value=len(guild.channels),
            inline=True
        )

        embed.add_field(
            name="Roles",
            value=len(guild.roles),
            inline=True
        )

        embed.add_field(
            name="Created",
            value=f"<t:{int(guild.created_at.timestamp())}:F>",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Shows a user's avatar.")
    async def avatar(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):

        member = member or interaction.user

        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar",
            color=discord.Color.purple()
        )

        embed.set_image(url=member.display_avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="Shows bot information.")
    async def botinfo(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🤖 SecurityBot",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Servers",
            value=len(self.bot.guilds),
            inline=True
        )

        embed.add_field(
            name="Users",
            value=sum(g.member_count for g in self.bot.guilds),
            inline=True
        )

        embed.add_field(
            name="Latency",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )

        embed.set_footer(
            text="SecurityBot • Version 1.0.0"
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
