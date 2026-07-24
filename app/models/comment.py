from sqlalchemy import Integer, String, DateTime , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base
from datetime import datetime, timezone


class CommentModel(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String , nullable=False)
    post_id: Mapped[int] = mapped_column(Integer , ForeignKey("posts.id") , nullable=False , index=True)
    author_id : Mapped[int] = mapped_column(Integer , ForeignKey("users.id") , nullable=False , index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))