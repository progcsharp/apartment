from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import make_session, User, Region, City, Apartment, Convenience
from schemas.user import UserResponse
from service.security import manager


async def get_user_by_id(id, session):
    async with session() as session:
        user = await session.get(User, id)
    return user


async def get_all_users(session):
    async with session() as session:
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        return users


async def get_user(mail, session):
    async with session() as session:
        query = select(User).where(User.mail == mail).options(selectinload(User.objects))
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            print(f"Пользователь с email {mail} не найден.")
            return None

        return user


async def get_all_region(session):
    async with session() as session:
        query = select(Region).options(selectinload(Region.cities))
        result = await session.execute(query)
        regions = result.scalars().all()
        return regions


async def get_region_by_id(id, session):
    async with session() as session:
        query = select(Region).where(Region.id == id).options(selectinload(Region.cities))
        result = await session.execute(query)
        region = result.scalar_one_or_none()
    return region


async def get_all_cities(session):
    async with session() as session:
        query = select(City).options(selectinload(City.region))
        result = await session.execute(query)
        cities = result.scalars().all()
        return cities


async def get_city_by_id(id:int, session):
    async with session() as session:
        query = select(City).where(City.id == id).options(selectinload(City.region))
        result = await session.execute(query)
        city = result.scalar_one_or_none()
    return city


async def get_all_apartment(session):
    async with session() as session:
        query = select(Apartment)
        result = await session.execute(query)
        apartment = result.scalars().all()
        return apartment


async def get_apartment_by_id(id, session):
    async with session() as session:
        apartment = await session.get(Apartment, id)
    return apartment


async def get_all_convenience(session):
    async with session() as session:
        query = select(Convenience)
        result = await session.execute(query)
        convenience = result.scalars().all()
        return convenience


async def get_convenience_by_id(id, session):
    async with session() as session:
        convenience = await session.get(Convenience, id)
    return convenience
