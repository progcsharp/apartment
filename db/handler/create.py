from datetime import date

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import User, Region, City, Apartment, Convenience, Object, ObjectConvenience, Client, UserClient, Reservation, \
    Tariff, Server
from db.handler import check_available_time
from db.handler.update import calculate_end_date
from exception.auth import Forbidden
from exception.database import NotFoundedError, ReservationError
from service.file import upload_file
from service.security import hash_password


async def create_user(user_data, session):
    password = await hash_password(user_data.password)
    user_data.password = password
    # user = User(fullname=user_data.fullname, mail=user_data.mail, phone=user_data.phone, password=password,
    #             date_before=date.today(), is_active=user_data.is_active, is_verified=user_data.is_verified,
    #             is_admin=user_data.is_admin, balance=user_data.balance)
    user = User.from_dict(user_data.__dict__)
    async with session() as session:

        query = select(User).where(User.mail == user_data.mail)
        result = await session.execute(query)
        user_check_mail = result.scalar_one_or_none()

        if user_check_mail:
            raise Forbidden("mail found")

        query = select(User).where(User.phone == user_data.phone)
        result = await session.execute(query)
        user_check_phone = result.scalar_one_or_none()

        if user_check_phone:
            raise Forbidden("phone found")

        if user_data.tariff_id > 0:
            query = select(Tariff).where(Tariff.id == user_data.tariff_id)
            result = await session.execute(query)
            tariff = result.scalar_one_or_none()

            end_date = await calculate_end_date(user.balance, tariff.daily_price)
            user.date_before = end_date
        else:
            user.date_before = date.today()

        session.add(user)
        await session.commit()
        await session.close()
    return user


async def create_region(region_data, session):
    region = Region(name=region_data.name, server_id=region_data.server_id)

    async with session() as session:
        session.add(region)
        await session.commit()
        await session.close()
    return region


async def create_city(city_data, session):
    city = City(name=city_data.name, region_id=city_data.region_id)

    async with session() as session:
        session.add(city)
        await session.commit()
        region = await session.execute(select(Region).where(Region.id == city_data.region_id))
        city.region = region.scalar_one_or_none()
        await session.close()
    return city


async def create_apartment(apartment_data, session):
    apartment = Apartment(name=apartment_data.name)

    async with session() as session:
        session.add(apartment)
        await session.commit()
        await session.close()
    return apartment


async def create_convenience(convenience_data, session):

    convenience = Convenience(name=convenience_data.name, icon=convenience_data.icon)

    async with session() as session:
        session.add(convenience)
        await session.commit()
        await session.close()
    return convenience


async def create_object(object_data, files, user_id, session):
    async with session() as session:
        query_city = select(City).options(selectinload(City.region).subqueryload(Region.servers)).\
            where(City.id == object_data.city_id)
        result = await session.execute(query_city)
        city = result.scalar_one_or_none()

        file_list = upload_file(files, city.region.servers.container_name, city.region.servers.link)

        object = Object(name=object_data.name, author_id=user_id, city_id=object_data.city_id,
                        apartment_id=object_data.apartment_id, description=object_data.description,
                        price=object_data.price,
                        area=object_data.area, room_count=object_data.room_count, adult_places=object_data.adult_places,
                        child_places=object_data.child_places,
                        floor=object_data.floor, min_ded=object_data.min_ded,
                        prepayment_percentage=object_data.prepayment_percentage, photos=file_list,
                        address=object_data.address, letter=object_data.letter)

        session.add(object)
        await session.commit()



        for convenience_id in object_data.convenience:
            object_convenience = ObjectConvenience(object_id=object.id, convenience_id=convenience_id)
            session.add(object_convenience)
            await session.commit()

        query = select(Object).where(Object.id == object.id).options(selectinload(Object.city).subqueryload(City.region)). \
            options(selectinload(Object.apartment)).options(selectinload(Object.author)). \
            options(selectinload(Object.conveniences))
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        await session.close()

    return object


async def create_client(client_data, session, user_id=None):
    client = Client(fullname=client_data.fullname, reiting=client_data.reiting,
                    phone=client_data.phone, email=client_data.email)

    async with session() as session:
        session.add(client)
        await session.commit()
        if user_id:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if not user:
                raise NotFoundedError

            user_client = UserClient(user_id=user.id, client_id=client.id)
            session.add(user_client)
            await session.commit()
        await session.close()
    return client


async def create_reservation(user_id, reservation_data, session):
    async with session() as session:
        query= select(Object).where(Object.id == reservation_data.object_id).where(Object.author_id == user_id)
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

        reservation = Reservation.from_dict(reservation_data.__dict__)


        if await check_available_time(session, reservation_data.object_id, reservation_data.start_date, reservation_data.end_date):
            query = select(UserClient).where(UserClient.user_id == user_id).where(UserClient.client_id == reservation_data.client_id)
            result = await session.execute(query)
            user_client = result.scalar_one_or_none()

            if not user_client:
                client_user = UserClient(user_id=user_id, client_id=reservation_data.client_id)

                session.add(client_user)
            session.add(reservation)
            await session.commit()
        else:
            raise ReservationError

        await session.close()
    return reservation


async def client_reservation_create(client_data, reservation_data, session):
    async with session() as session:

        if not await check_available_time(session, object_id=reservation_data.object_id,
                                          start_date=reservation_data.start_date, end_date=reservation_data.end_date):
            raise ReservationError

        query = select(Object).where(Object.id == reservation_data.object_id)
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

        query_client = select(Client).where(Client.phone == client_data.phone)
        result = await session.execute(query_client)
        client = result.scalar_one_or_none()

        if client:
            stmt = (
                update(Client)
                .where(Client.phone == client_data.phone)
                .values(**dict(client_data))
            )
            await session.execute(stmt)
        else:
            client = Client.from_dict(client_data.__dict__)
            client.reiting = 0
            session.add(client)

        await session.commit()

        query_user_client = select(UserClient).\
            where((UserClient.client_id == client.id) & (UserClient.user_id == object.author_id))
        result = await session.execute(query_user_client)
        user_client = result.scalar_one_or_none()

        if not user_client:
            client_user = UserClient(user_id=object.author_id, client_id=client.id)
            session.add(client_user)

        reservation = Reservation.from_dict(reservation_data.__dict__)
        reservation.client_id = client.id
        reservation.status = "new"
        reservation.letter = object.letter
        session.add(reservation)
        await session.commit()
        await session.close()
        return reservation


async def check_available_time(session: AsyncSession, object_id: int, start_date: date, end_date: date) -> bool:
    query = select(Reservation).where(
        (Reservation.object_id == object_id) & (Reservation.status == 'approved') &
        ((Reservation.start_date < end_date) & (Reservation.end_date > start_date))
    ).execution_options(populate_existing=True)

    result = await session.execute(query)
    existing_reservations = result.scalars().all()
    print(existing_reservations)
    if existing_reservations:
        for res in existing_reservations:
            if (start_date >= res.start_date and start_date < res.end_date) or \
                    (end_date > res.start_date and end_date <= res.end_date) or \
                    (start_date <= res.start_date and end_date >= res.end_date):
                return False

    return True


async def create_tariff(tariff_data, session):
    new_tariff = Tariff(name=tariff_data.name, daily_price=tariff_data.daily_price,
                        object_count=tariff_data.object_count, description=tariff_data.description,
                        icon=tariff_data.icon)

    async with session() as session:
        session.add(new_tariff)
        await session.commit()
        await session.close()
    return new_tariff


async def create_server(server_data, session):
    server = Server.from_dict(server_data.__dict__)
    async with session() as session:
        session.add(server)
        await session.commit()
        await session.close()
    return server


async def create_client_user(client_id, user_id, session):
    async with session() as session:
        query = select(Client).where(Client.id == client_id)
        result = await session.execute(query)
        client = result.scalar_one_or_none()

        if not client:
            raise NotFoundedError

        client_user = UserClient(user_id=user_id, client_id=client_id)
        session.add(client_user)
        await session.commit()
        await session.close
    return client
