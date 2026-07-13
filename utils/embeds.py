import discord


def success(title: str, description: str):
    return discord.Embed(
        title=f"✅ {title}",
        description=description,
        color=discord.Color.green()
    )


def error(title: str, description: str):
    return discord.Embed(
        title=f"❌ {title}",
        description=description,
        color=discord.Color.red()
    )


def warning(title: str, description: str):
    return discord.Embed(
        title=f"⚠️ {title}",
        description=description,
        color=discord.Color.orange()
    )


def info(title: str, description: str):
    return discord.Embed(
        title=f"ℹ️ {title}",
        description=description,
        color=discord.Color.blurple()
    )
