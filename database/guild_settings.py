from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class GuildSettings(Base):
    __tablename__ = "guild_settings"

    guild_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    log_channel: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )
