from datetime import datetime

from crud import s
from models import publicad,localad,user,city
"""
bk1 = Book(
    title='Deep Learning',
    author='Ian Goodfellow',
    pages=775,
    published=datetime(2016, 11, 18),
    price = 32.99,
)
"""
city1 = city(
    name='Харків'
)
city2 = city(
    name='Київ'
)
city3 = city(
    name='Дніпро'
)
city4 = city(
    name='Донецьк'
)
city5 = city(
    name='Львів'
)
city6 = city(
    name='Одеса'
)
pad1 = publicad(
    title='Продаю велосипед "Україна"',
    author='Петро Василенко',
    price= '149'
)

user1 = user(
    firstname='Богдан',
    lastname='Дякунчак',
    password='123',
    phone='+380985563737',
    cityid=city6
)

user2 = user(
    firstname='Олег',
    lastname='Дерех',
    password='щщщ',
    phone='+38067302213',
    cityid=city4
)

user3 = user(
    firstname='Максим',
    lastname='Газін',
    password='qwerty',
    phone='+38044708590',
    cityid=city1
)

lad1 = localad(
    title='Продам ноутбук марки "Asus"',
    author='Вася Пупкін',
    price='1,250 $',
    userid=user3
)

lad2 = localad(
    title='Продам літак Boeing',
    author='Ібрагім',
    price='1,000,000,000 $',
    userid=user1
)

lad3 = localad(
    title='Куплю чайник',
    author='Володимир Великий',
    price='Договірна',
    userid=user2
)
#with session_scope() as s:
s.add(pad1)

s.add(city1)
s.add(city2)
s.add(city3)
s.add(city4)
s.add(city5)
s.add(city6)

s.add(user1)
s.add(user2)
s.add(user3)

s.add(lad1)
s.add(lad2)
s.add(lad3)

s.commit()
s.close()