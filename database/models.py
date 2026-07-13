from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Warning(Base):
    __tablename__ = "warnings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    guild_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)
    moderator_id: Mapped[int] = mapped_column(BigInteger)

    reason: Mapped[str] = mapped_column(String(500))
from database.guild_settings import GuildSettings
