from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class Whitelist(Base):
    __tablename__ = "whitelist"

    guild_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
