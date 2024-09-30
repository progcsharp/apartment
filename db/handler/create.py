from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import make_session, User, Region, City
from service.security import hash_password


async def create_user(user_data, session):
    password = await hash_password(user_data.password)
    user = User(fullname=user_data.fullname, mail=user_data.mail, phone=user_data.phone, password=password,
                tarif=user_data.tarif, date_before=user_data.date_before)
    async with session() as session:
        session.add(user)
        await session.commit()

    return user


async def create_region(region_data, session):
    region = Region(name=region_data.name)

    async with session() as session:
        session.add(region)
        await session.commit()
    return region


async def create_city(city_data, session):
    city = City(name=city_data.name, region_id=city_data.region_id)

    async with session() as session:
        session.add(city)
        await session.commit()
        region = await session.execute(select(Region).where(Region.id == city_data.region_id))
        city.region = region.scalar_one_or_none()
    return city


async def create_apartment(apartment_data, session):
    apartment = Region(name=apartment_data.name)

    async with session() as session:
        session.add(apartment)
        await session.commit()
    return apartment
