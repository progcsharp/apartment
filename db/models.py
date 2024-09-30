from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, \
    Integer, String, Boolean, ForeignKey, \
    MetaData, Text, Date, ARRAY
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
    bed_count = Column(Integer)
    floor = Column(Integer)
    prepayment_percentage = Column(Integer)
    photos = Column(ARRAY(String))

    author = relationship("User", back_populates="objects")
    city = relationship("City", backref="objects")
    apartment = relationship("Apartment", backref="objects")

    conveniences = relationship("ObjectConvenience", backref="object")


class ObjectConvenience(Base):
    __tablename__ = 'object_convenience'

    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'), primary_key=True)
    convenience_id = Column(Integer, ForeignKey('convenience.id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<ObjectConvenience(object_id={self.object_id}, convenience_id={self.convenience_id})>"

