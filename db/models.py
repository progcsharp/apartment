from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, \
    Integer, String, Boolean, ForeignKey, \
    MetaData, Text, Date, ARRAY, Float, VARCHAR
# Pay attentions if you use another DB like Oracle, MySQL etc.
# This types implement for specific dialect


from sqlalchemy.orm import relationship

from .utils import conventions


meta = MetaData(naming_convention=conventions)

Base = declarative_base(metadata=meta)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    fullname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    mail = Column(Text, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    tarif = Column(String(20), nullable=False, default="standart")
    balance = Column(Integer, default=0)
    date_before = Column(Date)

    clients = relationship("Client", secondary="client_user", back_populates="user")
    objects = relationship("Object", back_populates="author")


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    cities = relationship("City", back_populates="region")


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    region_id = Column(Integer, ForeignKey('region.id', ondelete='CASCADE'))

    region = relationship("Region", back_populates="cities")


class Apartment(Base):
    __tablename__ = 'apartment'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class Convenience(Base):
    __tablename__ = 'convenience'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    photo = Column(String)

    objects = relationship("Object", secondary="object_convenience", back_populates="conveniences")


class Object(Base):
    __tablename__ = 'object'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    city_id = Column(Integer, ForeignKey('city.id', ondelete='CASCADE'))
    apartment_id = Column(Integer, ForeignKey('apartment.id', ondelete='CASCADE'))
    description = Column(Text)
    price = Column(Integer)
    area = Column(String)
    room_count = Column(Integer)
    bed_count = Column(Text)
    floor = Column(Text)
    min_ded = Column(Integer)
    prepayment_percentage = Column(Integer)
    photos = Column(ARRAY(String))
    address = Column(Text)
    active = Column(Boolean, server_default="false")

    author = relationship("User", back_populates="objects")
    city = relationship("City", backref="objects")
    apartment = relationship("Apartment", backref="objects")

    # conveniences = relationship("ObjectConvenience", backref="convenience")
    conveniences = relationship("Convenience", secondary="object_convenience", back_populates="objects")

    reservations = relationship("Reservation", back_populates="object")



class ObjectConvenience(Base):
    __tablename__ = 'object_convenience'

    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'), primary_key=True)
    convenience_id = Column(Integer, ForeignKey('convenience.id', ondelete='CASCADE'), primary_key=True)

    # convenience = relationship("Convenience", backref="objects")


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    fullname = Column(VARCHAR(255))
    reiting = Column(Float)
    phone = Column(VARCHAR(20))
    email = Column(Text)

    user = relationship("User", secondary="client_user", back_populates="clients")
    reservations = relationship("Reservation", back_populates="client")


class UserClient(Base):
    __tablename__ = 'client_user'

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), primary_key=True)


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey("object.id"))
    client_id = Column(Integer, ForeignKey("client.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20))
    description = Column(Text)

    # Внешние ключи
    object = relationship("Object", back_populates="reservations")
    client = relationship("Client", back_populates="reservations")
