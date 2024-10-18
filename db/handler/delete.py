from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import User, Region, City, Apartment, Convenience, Object, ObjectConvenience, Reservation


async def delete_user(id, session):
    async with session() as session:
        query = select(User).where(User.id == id).options(selectinload(User.objects).
                                                          options(selectinload(Object.reservations)))
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        for object in user.objects:
            for reservation in object.reservations:
                await session.delete(reservation)
            await session.delete(object)

        await session.delete(user)
        await session.commit()
    return "successful"


async def delete_region(id, session):
    async with session() as session:
        query = select(City).where(City.region_id==id)
        result = await session.execute(query)
        cities = result.scalars().all()
        if cities:
            raise

        region = await session.get(Region, id)
        await session.delete(region)
        await session.commit()
    return "successful"


async def delete_city(id, session):
    async with session() as session:
        query = select(Object).where(Object.city_id == id)
        result = await session.execute(query)
        objects = result.scalars().all()
        if objects:
            raise

        city = await session.get(City, id)
        await session.delete(city)
        await session.commit()
    return "successful"


async def delete_apartment(id, session):
    async with session() as session:
        query = select(Object).where(Object.apartment_id == id)
        result = await session.execute(query)
        objects = result.scalars().all()

        if objects:
            raise

        apartment = await session.get(Apartment, id)
        await session.delete(apartment)
        await session.commit()
    return "successful"


async def delete_convenience(id, session):
    async with session() as session:
        query = select(ObjectConvenience).where(ObjectConvenience.convenience_id == id)
        result = await session.execute(query)
        objects = result.scalars().all()

        if objects:
            raise

        convenience = await session.get(Convenience, id)
        await session.delete(convenience)
        await session.commit()

    return "successful"


async def delete_object(id, session):
    async with session() as session:
        query = select(Reservation).where(Reservation.object_id == id)
        result = await session.execute(query)
        reservation = result.scalars().all()

        if reservation:
            raise

        query = select(ObjectConvenience).where(ObjectConvenience.object_id == id)
        result = await session.execute(query)
        objects_convenience = result.scalars().all()

        for convenience in objects_convenience:
            await session.delete(convenience)
            await session.commit()

        object = await session.get(Object, id)
        await session.delete(object)
        await session.commit()

    return "successful"


async def delete_reservation(reservation_id, session):
    async with session() as session:
        reservation = await session.get(Reservation, reservation_id)

        await session.delete(reservation)
        await session.commit()

    return "successful"