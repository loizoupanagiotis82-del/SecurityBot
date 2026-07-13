from sqlalchemy import select

from database.database import Session
from database.guild_settings import GuildSettings


async def set_log_channel(
    guild_id: int,
    channel_id: int,
):
    async with Session() as session:

        result = await session.execute(
            select(GuildSettings).where(
                GuildSettings.guild_id == guild_id
            )
        )

        settings = result.scalar_one_or_none()

        if settings is None:

            settings = GuildSettings(
                guild_id=guild_id,
                log_channel=channel_id,
            )

            session.add(settings)

        else:

            settings.log_channel = channel_id

        await session.commit()


async def get_log_channel(
    guild_id: int,
):

    async with Session() as session:

        result = await session.execute(
            select(GuildSettings).where(
                GuildSettings.guild_id == guild_id
            )
        )

        settings = result.scalar_one_or_none()

        if settings is None:
            return None

        return settings.log_channel
