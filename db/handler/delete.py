from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from db import User, Region, City, Apartment, Convenience, Object, ObjectConvenience, Reservation, Client, UserClient
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


async def client_delete(user, client_id, session):
    async with session() as session:
        if user.is_admin:
            query = select(Client).where(Client.id == client_id).options(selectinload(Client.reservations))
        else:
            query = select(Client).where(Client.id == client_id).options(selectinload(Client.reservations)).join(UserClient).filter(UserClient.user_id == user.id)
        result = await session.execute(query)
        client = result.scalar_one_or_none()

        if not client:
            raise NotFoundedError

        if not await can_delete_client(client):
            raise DependencyConflictError

        await session.delete(client)

        # Удаляем связующие записи
        await session.execute(delete(UserClient).where(UserClient.client_id == client_id))
        await session.execute(delete(Reservation).where(Reservation.client_id == client_id))

        await session.commit()

    return "successful"


async def can_delete_client(client):
    if not client.reservations:
        return True

    return all(reservation.status == "rejected" for reservation in client.reservations)
