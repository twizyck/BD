from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped["User"] = relationship(back_populates='posts')
    comments: Mapped[list["Comment"]] = relationship(back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    content: Mapped[str] = mapped_column(Text)
    post: Mapped["Post"] = relationship(back_populates='comments')
