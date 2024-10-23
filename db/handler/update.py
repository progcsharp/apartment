from datetime import date, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from db import User, Tariff, Object, Reservation, City, ObjectConvenience
from exception.auth import Forbidden
from exception.database import NotFoundedError
from service.file import delete_file, upload_file
from service.security import hash_password


async def update_user_verified(mail, session):
    async with session() as session:
        query = select(User).where(User.mail == mail)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundedError

        user.is_verified = True
        # session.add(user)
        await session.commit()
        user.tariff = None
    return user


async def update_user_activate(user_data,  session):
    async with session() as session:
        query = select(User).where(User.id == user_data.id).options(selectinload(User.tariff))
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundedError

        user.is_active = not user.is_active
        # session.add(user)
        await session.commit()
    return user


async def update_object_activate(object_data, user, session):
    async with session() as session:
        query = select(Object).where(Object.id == object_data.id).options(selectinload(Object.city).subqueryload(City.region)).\
            options(selectinload(Object.apartment)).options(selectinload(Object.author)).\
            options(selectinload(Object.conveniences))
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

        if not (user.is_admin or object.author_id == user.id):
            raise Forbidden

        object.active = not object.active
        # session.add(object)
        await session.commit()
    return object


async def update_object_by_id(object_data, convenience_and_removed_photos, files, session):
    async with session() as session:
        query = select(Object).where(Object.id == object_data.id).options(selectinload(Object.city).subqueryload(City.region)).\
            options(selectinload(Object.apartment)).options(selectinload(Object.author)).\
            options(selectinload(Object.conveniences))
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

        delete_file(convenience_and_removed_photos.removed_photos)
        urls = upload_file(files)

        query = select(ObjectConvenience).where(ObjectConvenience.object_id == object_data.id)
        result = await session.execute(query)
        objects_convenience = result.scalars().all()

        for convenience in objects_convenience:
            if not (convenience.convenience_id in convenience_and_removed_photos.convenience):
                await session.delete(convenience)
                # convenience_and_removed_photos.convenience.remove(convenience.convenience_id)
                continue




        object.photos.extend(urls)

        stmt = (
            update(Object)
            .where(Object.id == object_data.id)
            .values(**dict(object_data))
        )

        await session.execute(stmt)
        await session.commit()

        return object


async def update_reservation_status(reservation_data, session):
    async with session() as session:
        query = select(Reservation).where(Reservation.id == reservation_data.id).\
            options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        result = await session.execute(query)
        reservation = result.scalar_one_or_none()

        if not reservation:
            raise NotFoundedError

        reservation.status = reservation_data.status
        # session.add(reservation)
        await session.commit()
    return reservation


async def update_reservation(user_id, reservation_data, session):
    async with session() as session:
        query = select(Reservation).where(Reservation.id == reservation_data.id).\
            join(Object).filter(Object.author_id == user_id).\
            options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        result = await session.execute(query)
        reservation = result.scalar_one_or_none()

        if not reservation:
            raise NotFoundedError

        stmt = (
            update(Reservation)
            .where(Reservation.id == reservation_data.id)
            .values(**dict(reservation_data))
        )

        await session.execute(stmt)
        await session.commit()

        return reservation


async def update_user_tariff_activate(user_data, session):
    async with session() as session:
        query = select(Tariff).where(Tariff.id == user_data.tariff_id)
        result = await session.execute(query)
        tariff = result.scalar_one_or_none()

        query = select(User).where(User.id == user_data.user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user and not tariff:
            raise NotFoundedError

        user.is_active = True
        user.balance += user_data.balance
        user.tariff_id = user_data.tariff_id

        end_tariff_data = await calculate_end_date(user.balance, tariff.daily_price)
        user.date_before = end_tariff_data

        # session.add(user)
        user.tariff = tariff
        await session.commit()

    return user


async def update_user_password(user_data, user_id, session):
    password = await hash_password(user_data.new_password)
    async with session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundedError

        user.password = password

        await session.commit()


async def update_user(user_data, session):
    async with session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundedError

        stmt = (
            update(User)
            .where(User.id == user_data.id)
            .values(**dict(user_data))
        )

        await session.execute(stmt)
        await session.commit()


async def calculate_end_date(balance, price_per_day):
    # Вычисляем количество дней, которые можно использовать
    days_to_use = balance // price_per_day

    # Добавляем полученное количество дней к текущей дате
    end_date = date.today() + timedelta(days=days_to_use)

    return end_date


async def update_tariff(tariff_data, session):
    async with session() as session:
        query = select(Tariff).where(Tariff.id == tariff_data.id)
        result = await session.execute(query)
        tariff = result.scalar_one_or_none()

        if not tariff:
            raise NotFoundedError

        stmt = (
            update(Tariff)
            .where(Tariff.id == tariff_data.id)
            .values(**dict(tariff_data))
        )

        # tariff.name = tariff_data.name
        # tariff.daily_price = tariff_data.daily_price
        # tariff.object_count = tariff_data.object_count
        # tariff.description = tariff_data.description
        # tariff.icon = tariff_data.icon

        # session.add(tariff)
        await session.execute(stmt)
        await session.commit()

    return tariff
