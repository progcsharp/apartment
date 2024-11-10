from datetime import date

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from db import Reservation


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


def filter_approved_reservations(reservations):
    return [reservation for reservation in reservations if reservation.status == "approved"]


async def calculate_end_date(balance, price_per_day):
    # Вычисляем количество дней, которые можно использовать
    if balance == None:
        balance = 0
    days_to_use = balance // price_per_day

    # Добавляем полученное количество дней к текущей дате
    end_date = date.today() + timedelta(days=days_to_use)

    return end_date
