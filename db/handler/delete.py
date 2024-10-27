from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import User, Region, City, Apartment, Convenience, Object, ObjectConvenience, Reservation
from exception.auth import Forbidden
from exception.database import NotFoundedError, DependencyConflictError


async def delete_user(id, session):
    async with session() as session:
        query = select(User).where(User.id == id).options(selectinload(User.objects).
                                                          options(selectinload(Object.reservations)))
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundedError

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
            raise DependencyConflictError

        region = await session.get(Region, id)

        if not region:
            raise NotFoundedError

        await session.delete(region)
        await session.commit()
    return "successful"


async def delete_city(id, session):
    async with session() as session:
        query = select(Object).where(Object.city_id == id)
        result = await session.execute(query)
        objects = result.scalars().all()
        if objects:
            raise DependencyConflictError

        city = await session.get(City, id)

        if not city:
            raise NotFoundedError

        await session.delete(city)
        await session.commit()
    return "successful"


async def delete_apartment(id, session):
    async with session() as session:
        query = select(Object).where(Object.apartment_id == id)
        result = await session.execute(query)
        objects = result.scalars().all()

        if objects:
            raise DependencyConflictError

        apartment = await session.get(Apartment, id)

        if not apartment:
            raise NotFoundedError

        await session.delete(apartment)
        await session.commit()
    return "successful"


async def delete_convenience(id, session):
    async with session() as session:
        query = select(ObjectConvenience).where(ObjectConvenience.convenience_id == id)
        result = await session.execute(query)
        objects = result.scalars().all()

        if objects:
            raise DependencyConflictError

        convenience = await session.get(Convenience, id)

        if not convenience:
            raise NotFoundedError

        await session.delete(convenience)
        await session.commit()

    return "successful"


async def delete_object(object_id, user, session):
    async with session() as session:
        query = select(Object).where(Object.id == object_id)
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

        if not (user.is_admin or object.author_id == user.id):
            raise Forbidden

        query = select(Reservation).where(Reservation.object_id == object_id)
        result = await session.execute(query)
        reservation = result.scalars().all()

        if reservation:
            raise DependencyConflictError

        query = select(ObjectConvenience).where(ObjectConvenience.object_id == object_id)
        result = await session.execute(query)
        objects_convenience = result.scalars().all()

        for convenience in objects_convenience:
            await session.delete(convenience)
            await session.commit()

        await session.delete(object)
        await session.commit()

    return "successful"


async def delete_reservation(user, reservation_id, session):
    async with session() as session:
        if user.is_admin:
            query = select(Reservation).where(Reservation.id == reservation_id)
        else:
            query = select(Reservation).where(Reservation.id == reservation_id).\
                join(Object).filter(Object.author_id == user.id)
        result = await session.execute(query)
        reservation = result.scalar_one_or_none()

        if not reservation:
            raise NotFoundedError

        await session.delete(reservation)
        await session.commit()

    return "successful"