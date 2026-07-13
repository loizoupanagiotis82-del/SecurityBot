from sqlalchemy import delete, select

from database.database import Session
from database.whitelist import Whitelist


async def add_whitelist(guild_id: int, user_id: int):
    async with Session() as session:

        exists = await session.execute(
            select(Whitelist).where(
                Whitelist.guild_id == guild_id,
                Whitelist.user_id == user_id
            )
        )

        if exists.scalar_one_or_none():
            return False

        session.add(
            Whitelist(
                guild_id=guild_id,
                user_id=user_id
            )
        )

        await session.commit()
        return True


async def remove_whitelist(guild_id: int, user_id: int):
    async with Session() as session:

        result = await session.execute(
            delete(Whitelist).where(
                Whitelist.guild_id == guild_id,
                Whitelist.user_id == user_id
            )
        )

        await session.commit()

        return result.rowcount > 0


async def is_whitelisted(guild_id: int, user_id: int):
    async with Session() as session:

        result = await session.execute(
            select(Whitelist).where(
                Whitelist.guild_id == guild_id,
                Whitelist.user_id == user_id
            )
        )

        return result.scalar_one_or_none() is not None
