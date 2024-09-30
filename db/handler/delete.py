from db import User, Region, City, Apartment, Convenience


async def delete_user(id, session):
    async with session() as session:
        user = await session.get(User, id)
        session.delete(user)
        await session.commit()
    return "successful"


async def delete_region(id, session):
    async with session() as session:
        region = await session.get(Region, id)
        region.name = "Crim"
        await session.delete(region)
        await session.commit()
    return "successful"


async def delete_city(id, session):
    async with session() as session:
        city = await session.get(City, id)
        await session.delete(city)
        await session.commit()
    return "successful"


async def delete_apartment(id, session):
    async with session() as session:
        apartment = await session.get(Apartment, id)
        session.delete(apartment)
        await session.commit()
    return "successful"


async def delete_convenience(id, session):
    async with session() as session:
        convenience = await session.get(Convenience, id)
        session.delete(convenience)
        await session.commit()
    return "successful"