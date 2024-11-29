from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from db import User, Region, City, Apartment, Convenience, Object, ObjectConvenience, Reservation, Client, UserClient, \
    Server, ObjectHashtag, Hashtag
from db.handler.create import create_logs
from exception.auth import Forbidden
from exception.database import NotFoundedError, DependencyConflictError, ErrorDeleteServer


async def delete_user(id, session, admin_id):
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
        await create_logs(session, admin_id, f"Пользователь удален: почта {user.mail}")
        await session.close()
    return "successful"


async def delete_region(id, session, admin_id):
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
        await create_logs(session, admin_id, f"Удален регион {region.name}")
        await session.close()
    return "successful"


async def delete_city(id, session, admin_id):
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
        await create_logs(session, admin_id, f"Удален город {city.name}")
        await session.close()
    return "successful"


async def delete_apartment(id, session, admin_id):
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
        await create_logs(session, admin_id, f"Удален тип недвижимости {apartment.name}")
        await session.close()
    return "successful"


async def delete_convenience(id, session, admin_id):
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
        await create_logs(session, admin_id, f"удалено удобство {convenience.name}")
        await session.close()

    return "successful"


async def delete_hashtag(hashtag_id, session, admin_id):
    async with session() as session:
        query = select(ObjectHashtag).where(ObjectHashtag.hashtag_id == hashtag_id)
        result = await session.execute(query)
        objects = result.scalars().all()

        if objects:
            raise DependencyConflictError

        hashtag = await session.get(Hashtag, id)

        if not hashtag:
            raise NotFoundedError

        await session.delete(hashtag)
        await session.commit()
        await create_logs(session, admin_id, f"удален хештег {hashtag.name}")
        await session.close()

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
        if user.is_admin:
            await create_logs(session, user.id, f"админ удалил объект {object.name} пользователя {object.author_id}")
        else:
            await create_logs(session, user.id, f"Удален объект {object.name}")
        await session.close()

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
        if user.is_admin:
            await create_logs(session, user.id, f"Админ удалил бронь объекта {reservation.object_id}")
        else:
            await create_logs(session, user.id, f"Удалена броль объекта {reservation.object_id}")
        await session.close()

    return "successful"


async def client_delete(user, client_id, session):
    async with session() as session:
        # if user.is_admin:
        #     query = select(Client).where(Client.id == client_id).options(selectinload(Client.reservations))
        # else:
        #     query = select(Client).where(Client.id == client_id).options(selectinload(Client.reservations)).join(UserClient).filter(UserClient.user_id == user.id)
        # result = await session.execute(query)
        # client = result.scalar_one_or_none()
        #
        # if not client:
        #     raise NotFoundedError
        #
        # if not await can_delete_client(client):
        #     raise DependencyConflictError
        #
        # await session.delete(client)
        #
        # # Удаляем связующие записи
        # await session.execute(delete(UserClient).where(UserClient.client_id == client_id))
        # await session.execute(delete(Reservation).where(Reservation.client_id == client_id))
        #
        # await session.commit()
        # await session.close()

        query = select(Client).where(Client.id == client_id)
        if user.is_admin:
            result = await session.execute(query)
            client = result.scalar_one_or_none()

            if not client:
                raise NotFoundedError

            if not await can_delete_client(client, user, session):
                raise DependencyConflictError

            await session.delete(client)

            # Удаляем связующие записи
            await session.execute(delete(UserClient).where(UserClient.client_id == client_id))
            await session.execute(delete(Reservation).where(Reservation.client_id == client_id))
            await session.commit()
            await create_logs(session, user.id, f"Админ удалил клиента {client.phone}")
            await session.close()

            return "successful"
        query = query.join(UserClient).filter(UserClient.user_id == user.id)
        result = await session.execute(query)
        client = result.scalar_one_or_none()

        if not client:
            raise NotFoundedError

        if not await can_delete_client(client, user, session):
            raise DependencyConflictError

        await session.execute(delete(UserClient).where(UserClient.client_id == client_id))
        await session.execute(delete(Reservation).where(Reservation.client_id == client_id))
        await session.commit()
        await create_logs(session, user.id, f"Удалена клиента {client.id} и пользователя {user.id}")
        await session.close()

        return "successful"


async def can_delete_client(client, user, session):
    if user.is_admin:
        query = select(Reservation).where(Reservation.client_id == client.id)
    else:
        query = select(Reservation).where(Reservation.client_id == client.id).join(Object).filter(Object.author_id == user.id)
    result = await session.execute(query)
    reservations = result.scalars().all()

    if not reservations:
        return True

    return all(reservation.status == "rejected" for reservation in reservations)


async def server_delete(server_id, session, admin_id):
    async with session() as session:
        query = select(Server).where(Server.id == server_id)
        result = await session.execute(query)
        server = result.scalar_one_or_none()

        if not server:
            raise NotFoundedError

        if server.default:
            raise ErrorDeleteServer

        query_region = select(Region).where(Region.server_id == server_id)
        result = await session.execute(query_region)
        region = result.scalars().all()

        if region:
            raise DependencyConflictError

        await session.delete(server)
        await session.commit()

        await create_logs(session, admin_id, f"Удален сервер {server.name}")
        await session.close()

        return "successful"
