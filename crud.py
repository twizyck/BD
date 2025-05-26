from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import User, Post, Comment

# создание
async def create_user(session: AsyncSession, username: str):
    user = User(username=username)
    session.add(user)
    await session.commit()

async def create_post(session: AsyncSession, title: str, content: str, user_id: int):
    post = Post(title=title, content=content, author_id=user_id)
    session.add(post)
    await session.commit()

async def create_comment(session: AsyncSession, post_id: int, content: str):
    comment = Comment(post_id=post_id, content=content)
    session.add(comment)
    await session.commit()

# чтение
async def get_user_posts(session: AsyncSession, user_id: int):
    result = await session.execute(select(Post).where(Post.author_id == user_id))
    return result.scalars().all()

async def get_post_comments(session: AsyncSession, post_id: int):
    result = await session.execute(select(Comment).where(Comment.post_id == post_id))
    return result.scalars().all()

async def search_posts_by_word(session: AsyncSession, word: str):
    result = await session.execute(select(Post).where(Post.content.ilike(f"%{word}%")))
    return result.scalars().all()

# обновление
async def update_post_title(session: AsyncSession, post_id: int, new_title: str):
    await session.execute(update(Post).where(Post.id == post_id).values(title=new_title))
    await session.commit()

# удаление
async def delete_comment(session: AsyncSession, comment_id: int):
    await session.execute(delete(Comment).where(Comment.id == comment_id))
    await session.commit()

# присоединение с предзагрузкой автора
async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(selectinload(Post.author))
    result = await session.execute(stmt)
    return result.scalars().all()
