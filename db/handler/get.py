from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload, aliased

from db import make_session, User, Region, City, Apartment, Convenience, Object, ObjectConvenience, Client, UserClient, \
    Reservation, Tariff
from exception.database import NotFoundedError
from schemas.user import UserResponse
from service.security import manager


async def get_user_by_id(id, session):
    async with session() as session:
        query = select(User).where(User.id == id).where(User.is_admin==False).options(selectinload(User.tariff))
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundedError

    return user


async def get_all_users(session):
    async with session() as session:
        query = select(User).where(User.is_admin==False).options(selectinload(User.tariff))
        result = await session.execute(query)
        users = result.scalars().all()
        return users


async def get_user(mail, session):
    async with session() as session:
        query = select(User).where(User.mail == mail).options(selectinload(User.objects)).options(selectinload(User.tariff))
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            print(f"Пользователь с email {mail} не найден.")
            raise NotFoundedError

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

        if not region:
            raise NotFoundedError

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

        if not city:
            raise NotFoundedError

    return city


async def get_all_apartment(session):
    async with session() as session:
        query = select(Apartment)
        result = await session.execute(query)
        apartment = result.scalars().all()
        return apartment


async def get_apartment_by_id(id: int, session):
    async with session() as session:
        query = select(Apartment).where(Apartment.id == id)
        result = await session.execute(query)
        apartment = result.scalar_one_or_none()
        # apartment = await session.get(Apartment, id)

        if not apartment:
            raise NotFoundedError

    return apartment


async def get_all_convenience(session):
    async with session() as session:
        query = select(Convenience)
        result = await session.execute(query)
        convenience = result.scalars().all()
        return convenience


async def get_convenience_by_id(convenience_id, session):
    async with session() as session:
        query = select(Convenience).where(Convenience.id == convenience_id)
        result = await session.execute(query)
        convenience = result.scalar_one_or_none()

        if not convenience:
            raise NotFoundedError

    return convenience


async def get_all_object(user, session):
    async with session() as session:
        if user.is_admin:
            query = select(Object).options(selectinload(Object.city).subqueryload(City.region)).\
                options(selectinload(Object.apartment)).options(selectinload(Object.author)).\
                options(selectinload(Object.conveniences))
        else:
            query = select(Object).where(Object.author_id == user.id).options(selectinload(Object.city).subqueryload(City.region)). \
                options(selectinload(Object.apartment)).options(selectinload(Object.author)). \
                options(selectinload(Object.conveniences))
        result = await session.execute(query)
        object = result.scalars().all()

    return object


async def get_by_id_object(id, session):
    async with session() as session:
        query = select(Object).where(Object.id == id).options(selectinload(Object.city).subqueryload(City.region)).\
            options(selectinload(Object.apartment)).options(selectinload(Object.author)).\
            options(selectinload(Object.conveniences))
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

    return object


async def get_by_id_object_by_user(object_id, session):
    async with session() as session:
        # if user.is_admin:
        query = select(Object).where(Object.id == object_id).options(
            selectinload(Object.city).subqueryload(City.region)). \
            options(selectinload(Object.apartment)).options(selectinload(Object.author)). \
            options(selectinload(Object.conveniences))
        # else:
        #     query = select(Object).where(Object.id == object_id).where(Object.author_id == user.id).options(selectinload(Object.city).subqueryload(City.region)).\
        #         options(selectinload(Object.apartment)).options(selectinload(Object.author)).\
        #         options(selectinload(Object.conveniences))
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

    return object


async def get_object_by_user_id(user_id, user, session):
    async with session() as session:
        if user.is_admin:
            query = select(Object).where(Object.author_id==user_id).options(selectinload(Object.city).subqueryload(City.region)).\
                options(selectinload(Object.apartment)).options(selectinload(Object.author)).\
                options(selectinload(Object.conveniences))
        result = await session.execute(query)
        objects = result.scalars().all()
    return objects


async def get_all_client(session, user):
    async with session() as session:
        if not user.is_admin:
            query = select(Client).join(UserClient).filter(UserClient.user_id == user.id)
            result = await session.execute(query)
            client = result.scalars().all()
        else:
            query = select(Client)
            result = await session.execute(query)
            client = result.scalars().all()

    return client


async def get_client_by_phone(phone_client, session):
    async with session() as session:
        query = select(Client).where(Client.phone == phone_client)
        result = await session.execute(query)
        client = result.scalar_one_or_none()

        if not client:
            raise NotFoundedError

    return client


async def get_client_by_id(user_id, session):
    async with session() as session:
        query = select(Client).join(UserClient).filter(UserClient.user_id == user_id)
        result = await session.execute(query)
        client = result.scalars().all()

    return client


async def get_reservation_all(user, session):
    async with session() as session:
        if user.is_admin:
            query = select(Reservation).join(Object). \
                options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        else:
            query = select(Reservation).join(Object).filter(Object.author_id == user.id).\
                options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        result = await session.execute(query)
        reservation = result.scalars().all()

    return reservation


async def get_reservation_by_object_id(user, object_id, session):
    async with session() as session:
        query = select(Reservation).where(Reservation.object_id == object_id)
        #     options(selectinload(Reservation.object)).options(selectinload(Reservation.client))

        if not user.is_admin:
            query = query.join(Object).filter(Object.author_id==user.id)

        query = query.options(selectinload(Reservation.object)).options(selectinload(Reservation.client))

        result = await session.execute(query)
        reservation = result.scalars().all()

    return reservation


async def get_reservation_by_client_id(user, client_id, session):
    async with session() as session:
        query = select(Reservation).where(Reservation.client_id == client_id).\
            options(selectinload(Reservation.object)).options(selectinload(Reservation.client))

        if not user.is_admin:
            query = query.join(Object).filter(Object.author_id == user.id)

        query = query.\
            options(selectinload(Reservation.object)).options(selectinload(Reservation.client))

        result = await session.execute(query)
        reservation = result.scalars().all()

    return reservation


async def get_reservation_by_user_id(user_id, session):
    async with session() as session:
        query = select(Reservation).join(Object).filter(Object.author_id == user_id).\
            options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        result = await session.execute(query)
        reservation = result.scalars().all()

    return reservation


async def get_reservation_by_id(user, reservation_id, session):
    async with session() as session:
        query = select(Reservation).where(Reservation.id == reservation_id)

        if not user.is_admin:
            query = query.join(Object).filter(Object.author_id == user.id)

        query = query.options(selectinload(Reservation.client)).\
            options(selectinload(Reservation.object))

        result = await session.execute(query)
        reservation = result.scalar_one_or_none()

        if not reservation:
            raise NotFoundedError

    return reservation


async def get_tariff_by_id(id, session):
    async with session() as session:
        query = select(Tariff).where(Tariff.id==id)
        result = await session.execute(query)
        tariff = result.scalar_one_or_none()

        if not tariff:
            raise NotFoundedError

    return tariff


async def get_all_tariff(session):
    async with session() as session:
        query = select(Tariff).order_by(Tariff.daily_price)
        result = await session.execute(query)
        tariffs = result.scalars().all()

    return tariffs


# async def count_objects_in_region(session):
#     async with session() as session:
#         # stmt = select(func.count(Object.id)).join(City).group_by(Region.name)
# #         stmt = """SELECT r.name AS region_name, COUNT(o.id) AS object_count
# # FROM region r
# # LEFT JOIN city c ON r.id = c.region_id
# # LEFT JOIN object o ON c.id = o.city_id
# # GROUP BY r.id, r.name
# # ORDER BY object_count DESC;"""
#
#         # stmt = (
#         #     select(
#         #         Region.name.label('region_name'),
#         #         func.count(Object.id).label('object_count')
#         #     )
#         #     .outerjoin(City)
#         #     .outerjoin(Object)
#         #     .group_by(Region.id, Region.name)
#         #     .order_by(func.count(Object.id).desc())
#         # )
#         # stmt = select(Region.name, func.count(Object.id).label("count")).join(City).filter(City.region_id == Region.id).join(Object).filter(Object.city_id == City.id).group_by(Region.id, Region.name)
#         RegionAlias = aliased(Region)
#
#         stmt = (
#             select(
#                 RegionAlias,
#                 func.count(Object.id).label('object_count')
#             )
#             .select_from(RegionAlias)
#             .outerjoin(City)
#             .outerjoin(Object)
#             .group_by(RegionAlias.id, RegionAlias.name)
#             .order_by(func.count(Object.id).desc())
#         )
#
#         # stmt2 = select(func.count(Object.id)).where(Object.city_id)
#
#         # stmt = select(func.count(Object.id)).where(Object.city_id == 24)
#         # result = await session.execute(stmt)
#         # regions = result.unique().all()
#
#         # region_data = {}
#         # for row in regions:
#         #     region_name, count = row
#         #     region_data[region_name] = count
#
#     return regions
