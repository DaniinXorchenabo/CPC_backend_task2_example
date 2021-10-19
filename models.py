from datetime import date
from datetime import datetime
from datetime import time
from pony.orm import *


db = Database()


class Book(db.Entity):
    id = PrimaryKey(int, auto=True)
    page_count = Required(int)
    name = Required(str)
    prise = Optional(float)
    author = Required("Author")


class Author(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    surname = Required(str)
    age = Optional(int)
    email = Required(str, unique=True)
    login = Required(str, unique=True)
    books = Set('Book')




# db.generate_mapping()
