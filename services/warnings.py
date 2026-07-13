from sqlalchemy import delete, select

from database.database import Session
from database.models import Warning


async def add_warning(
    guild_id: int,
    user_id: int,
    moderator_id: int,
    reason: str,
) -> Warning:
    async with Session() as session:
        warning = Warning(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            reason=reason,
        )

        session.add(warning)
        await session.commit()
        await session.refresh(warning)

        return warning


async def get_warnings(
    guild_id: int,
    user_id: int,
) -> list[Warning]:
    async with Session() as session:
        result = await session.execute(
            select(Warning)
            .where(
                Warning.guild_id == guild_id,
                Warning.user_id == user_id,
            )
            .order_by(Warning.id.asc())
        )

        return list(result.scalars().all())


async def clear_warnings(
    guild_id: int,
    user_id: int,
) -> int:
    async with Session() as session:
        result = await session.execute(
            delete(Warning).where(
                Warning.guild_id == guild_id,
                Warning.user_id == user_id,
            )
        )

        await session.commit()

        return result.rowcount or 0
