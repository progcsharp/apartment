from sqlalchemy import select

from db import make_session, User


async def update_user_activate(mail, session):
    async with session() as session:
        query = select(User).where(User.mail == mail)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        user.is_active = True
        session.add(user)
        session.commit()
        session.close()
    return user

