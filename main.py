import asyncio
from database import engine, Base, async_session
from crud import *

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await init_db()
    async with async_session() as session:
        #create user
        await create_user(session, "alice")
        await create_user(session, "bob")

        #create post
        await create_post(session, "First Post", "Hello world!", 1)
        await create_post(session, "Second Post", "Another post content", 1)
        await create_post(session, "Bob's Post", "Hi from Bob!", 2)

        #commit
        await create_comment(session, 1, "Nice post!")
        await create_comment(session, 1, "Thanks for sharing")

        #search
        posts = await search_posts_by_word(session, "hello")
        print("Posts containing 'hello':", [p.title for p in posts])

        #join
        posts_with_authors = await get_posts_with_authors(session)
        for post in posts_with_authors:
            print(f"{post.title} by {post.author.username}")

asyncio.run(main())
