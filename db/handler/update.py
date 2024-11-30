from datetime import date, timedelta
from service import mail

from fastapi_mail import MessageSchema, MessageType, FastMail
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from config import mail_conf
from db import User, Tariff, Object, Reservation, City, ObjectConvenience, Server, Region, ObjectHashtag, Client
from db.handler import check_available_time
from db.handler.create import create_logs, create_object_hashtag
from db.handler.validate import calculate_end_date
from exception.auth import Forbidden
from exception.database import NotFoundedError, ReservationError
from service.file import delete_file, upload_file
from service.mail import message_mail
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

        await session.close()
    return user


async def update_user_activate(user_data,  session, admin_id):
    async with session() as session:
        query = select(User).where(User.id == user_data.id).options(selectinload(User.tariff))
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundedError

        user.is_active = not user.is_active
        # session.add(user)
        await session.commit()
        await create_logs(session, admin_id, f"Пользователь - статус: {'активирован' if user.is_active else 'деактивирован'}")
        await session.close()
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
        await create_logs(session, user.id, f"Статус объекта {object.id} изменен на {'активирован' if object.active else 'деактивирован'}")
        await session.close()

        if object.active:
            activate = message_mail("activate")
            message = MessageSchema(
                subject=activate['subject'],
                recipients=[object.author.mail],
                body=activate['description'],
                subtype=MessageType.html)

            fm = FastMail(mail_conf)
            await fm.send_message(message)
        else:
            deactivate = message_mail("deactivate")
            message = MessageSchema(
                subject=deactivate['subject'],
                recipients=[object.author.mail],
                body=deactivate['description'],
                subtype=MessageType.html)

            fm = FastMail(mail_conf)
            await fm.send_message(message)

        query_reservation_count = select(func.count(Reservation.object_id)).where(Reservation.object_id == object.id). \
            where(Reservation.status != "rejected").where(Reservation.status != "completed")
        result = await session.execute(query_reservation_count)
        reservation_count = result.scalar()
        object.reservation_count = reservation_count

    return object


async def update_object_by_id(object_data, convenience_and_removed_photos, files, session, user):
    async with session() as session:
        if user.is_admin:
            query = select(Object).where(Object.id == object_data.id).options(selectinload(Object.city).subqueryload(City.region)).\
                options(selectinload(Object.apartment)).options(selectinload(Object.author)).\
                options(selectinload(Object.conveniences))
        else:
            query = select(Object).where(Object.id == object_data.id).where(Object.author_id==user.id).options(
                selectinload(Object.city).subqueryload(City.region)). \
                options(selectinload(Object.apartment)).options(selectinload(Object.author)). \
                options(selectinload(Object.conveniences))
        result = await session.execute(query)
        object = result.scalar_one_or_none()

        if not object:
            raise NotFoundedError

        set2 = set(convenience_and_removed_photos.removed_photos)

        photos = [element for element in object.photos if element not in set2]

        delete_file(convenience_and_removed_photos.removed_photos)
        if files:
            query_server = select(Server).join(Region).filter(Region.id == object.city.region.id)
            result = await session.execute(query_server)
            server = result.scalar_one_or_none()
            urls = upload_file(files, server.container_name, server.link)
            photos.extend(urls)
            object.photos = photos

        query = select(ObjectConvenience.convenience_id).where(ObjectConvenience.object_id == object_data.id)
        result = await session.execute(query)
        objects_convenience = result.scalars().all()

        delete_array, create_array = update_arrays(objects_convenience, convenience_and_removed_photos.convenience)

        delete_stmt = (
            delete(ObjectConvenience).where(ObjectConvenience.convenience_id.in_(delete_array))
        )

        await session.execute(delete_stmt)

        for convenience_id in create_array:
            oc = ObjectConvenience(object_id=object.id, convenience_id=convenience_id)
            session.add(oc)

        query = select(ObjectHashtag.hashtag_id).where(ObjectHashtag.object_id == object_data.id)
        result = await session.execute(query)
        object_hashtag = result.scalars().all()

        delete_array_hashtag, create_array_hashtag = update_arrays(object_hashtag, convenience_and_removed_photos.hashtag)

        delete_hashtag_stmt = (
            delete(ObjectHashtag).where(ObjectHashtag.hashtag_id.in_(delete_array_hashtag))
        )

        await session.execute(delete_hashtag_stmt)

        for hashtag_id in create_array:
            oc = ObjectHashtag(object_id=object.id, hashtag_id=hashtag_id)
            session.add(oc)

        stmt = (
            update(Object)
            .where(Object.id == object_data.id)
            .values(**dict(object_data))
        )

        for tag_id in create_array_hashtag:
            await create_object_hashtag(object.id, tag_id, session)

        await session.execute(stmt)
        await session.commit()
        if user.is_admin:
            await create_logs(session, user.id, f"Изменен объект ID:{object.id} пользователя ID:{object.author_id}")
        else:
            await create_logs(session, user.id, f"Изменен объект ID:{object.id}")

        query_reservation_count = select(func.count(Reservation.object_id)).where(Reservation.object_id == object.id). \
            where(Reservation.status != "rejected").where(Reservation.status != "completed")
        result = await session.execute(query_reservation_count)
        reservation_count = result.scalar()
        object.reservation_count = reservation_count
        await session.close()
        return object


def update_arrays(arr1, arr2):
    # Создаем множество из arr1 для быстрого доступа
    set1 = set(arr1)

    # Создаем множество из arr2
    set2 = set(arr2)

    # Вычитаем set2 из set1 для получения уникальных элементов arr1
    unique_ids = list(set1 - set2)

    # Вычитаем set1 из set2 для получения новых идентификаторов
    new_ids = list(set2 - set1)

    # Объединяем результаты
    return unique_ids, new_ids


async def update_reservation_status(reservation_data, user, session):
    async with session() as session:

        if user.is_admin:
            query = select(Reservation).where(Reservation.id == reservation_data.id).\
                options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        else:
            query = select(Reservation).where(Reservation.id == reservation_data.id).\
                join(Object).filter(Object.author_id == user.id). \
                options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        result = await session.execute(query)
        reservation = result.scalar_one_or_none()

        if not reservation:
            raise NotFoundedError

        if reservation_data.status == "approved":
            if not await check_available_time(session, reservation.object_id,
                                              reservation.start_date, reservation.end_date):
                raise ReservationError

        reservation.status = reservation_data.status

        # session.add(reservation)
        message_approve = message_mail("approve reservation")['description'].replace("(?CLIENT_FULLNAME)", reservation.client.fullname).\
            replace("(?OBJECT_NAME)", reservation.object.name).\
            replace("(?OBJECT_ADDRESS)", f"{reservation.object.city.name},{reservation.object.address}").\
            replace("(?START_DATE)", str(reservation.start_date)).replace("(?END_DATE)", str(reservation.end_date)).\
            replace("(?ADULTS)", reservation.adult_places).replace("(?KIDS)", reservation.child_places).\
            replace("(?PRICE)", reservation.object.price)

        message_reject = message_mail("reject reservation")['description'].replace("(?CLIENT_FULLNAME)", reservation.client.fullname)

        if reservation_data.status == "approved":
            message = MessageSchema(
                subject=message_mail("approve reservation")["subject"],
                recipients=[reservation.client.email],
                body=f'{message_approve}',
                subtype=MessageType.html)
        elif reservation_data.status == "rejected":
            message = MessageSchema(
                subject= message_mail("reject reservation")["subject"],
                recipients=[reservation.client.email],
                body=f'{message_reject}',
                subtype=MessageType.html)
        fm = FastMail(mail_conf)
        await fm.send_message(message)
        await session.commit()
        # await create_logs(session, , f"Создана бронь {reservation.id}")
        if user.is_admin:
            await create_logs(session, user.id, f"Изменен статус брони ID:{reservation.id} на {reservation.status}")
        else:
            await create_logs(session, user.id, f"Изменен статус брони ID:{reservation.id} на {reservation.status}")
        await session.close()
    return reservation


async def update_reservation(user, reservation_data, session):
    async with session() as session:
        if user.is_admin:
            query = select(Reservation).where(Reservation.id == reservation_data.id). \
                options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        else:
            query = select(Reservation).where(Reservation.id == reservation_data.id).\
                join(Object).filter(Object.author_id == user.id).\
                options(selectinload(Reservation.object)).options(selectinload(Reservation.client))
        result = await session.execute(query)
        reservation = result.scalar_one_or_none()

        if not reservation:
            raise NotFoundedError

        if reservation_data.status == "approved":
            if reservation_data.status != reservation.status:
                if not await check_available_time(session, reservation_data.object_id,
                                                  reservation_data.start_date, reservation_data.end_date):
                    raise ReservationError

        stmt = (
            update(Reservation)
            .where(Reservation.id == reservation_data.id)
            .values(**dict(reservation_data))
        )

        await session.execute(stmt)
        await session.commit()

        await create_logs(session, user.id, f"Изменена бронь ID:{reservation.id}")

        await session.close()
        return reservation


async def update_user_tariff_activate(tariff_id, user_id, balance, session):
    async with session() as session:
        query = select(Tariff).where(Tariff.id == tariff_id)
        result = await session.execute(query)
        tariff = result.scalar_one_or_none()

        message_log = ''

        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user.tariff_id != tariff_id:
            message_log = f"Выбран тариф: {tariff.name}"
        else:
            message_log = f'Добавлен баланс: {balance}'

        if not user and not tariff:
            raise NotFoundedError

        user.is_active = True
        user.balance += balance
        user.tariff_id = tariff_id

        end_tariff_data = await calculate_end_date(user.balance, tariff.daily_price)
        user.date_before = end_tariff_data

        # session.add(user)
        user.tariff = tariff
        await session.commit()

        await create_logs(session, user.id, f"{message_log}")
        await session.close()
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
        await create_logs(session, user.id, f"Сменил пароль")
        await session.close()

    return user


async def update_user(user_data, session):
    async with session() as session:
        query = select(User).where(User.id == user_data.id).options(selectinload(User.tariff))
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
        await create_logs(session, user.id, f"Обновлены контактные данные")
        await session.close()

    return user


# async def calculate_end_date(balance, price_per_day):
#     # Вычисляем количество дней, которые можно использовать
#     if balance == None:
#         balance = 0
#     days_to_use = balance // price_per_day
#
#     # Добавляем полученное количество дней к текущей дате
#     end_date = date.today() + timedelta(days=days_to_use)
#
#     return end_date


async def update_tariff(tariff_data, session, admin_id):
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
        await create_logs(session, admin_id, f"Изменен тариф ID:{tariff.id}")
        await session.close()

    return tariff


async def update_server(server_data, session, admin_id):
    async with session() as session:
        query = select(Server).where(Server.id == server_data.id)
        result = await session.execute(query)
        server = result.scalar_one_or_none()

        if not server:
            raise NotFoundedError


        stmt = (
            update(Server)
            .where(Server.id == server_data.id)
            .values(**dict(server_data))
        )
        await session.execute(stmt)
        await session.commit()
        await create_logs(session, admin_id, f"Изменен сервер ID:{server.id}")
        await session.close()

    return server


async def server_activate(server_id, session, admin_id):
    async with session() as session:
        query = select(Server).where(Server.default == True)
        result = await session.execute(query)
        current_default = result.scalar_one_or_none()

        if current_default:
            current_default.default = False

        query = select(Server).where(Server.id == server_id)
        result = await session.execute(query)
        server = result.scalar_one_or_none()

        server.default = True

        await session.commit()
        await create_logs(session, admin_id, f"Изменен сервер по умолчанию ID:{server.id}")
        await session.close()

        return server

