from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship

Base = declarative_base()

class city(Base):
    __tablename__ = 'cities'
    id = Column(Integer,primary_key=True)
    name = Column(String)

class publicad(Base):
    __tablename__ = 'PublicAD'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    price = Column(MONEY)

    def __repr__(self):
        return "<PublicADs(title='{}', author='{}', price={})>".format(self.title, self.author, self.price)

class user(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    phone = Column(String)
    city_id = Column(Integer, ForeignKey('cities.id'))
    cityid = relationship(city, backref="users", lazy="joined")

    def __repr__(self):
        return "<Users(firstname='{}', lastname='{}', cityid={})>" .format(self.firstname, self.lastname, self.cityid)

class localad(Base):
    __tablename__ = 'LocalAD'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    price = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    userid = relationship(user, backref="LocalAD", lazy="joined")

    def __repr__(self):
        return "<LocalADs(title='{}', author='{}', price={})>".format(self.title, self.author, self.price)

