import os.path
from fastapi import FastAPI, Body
import uvicorn
from models import db, Author, Book
from pony.orm import db_session, commit
from schema import AuthorOut, CreateBook, CreateAuthor, EditBook, OutBookYet, EditAuthor

app = FastAPI()
DATABASE_FILENAME = 'author_and_books.sqlite'


@app.on_event("startup")
async def start_app():
    """Выполняется при старте приложения"""
    create_db = True
    if os.path.isfile(DATABASE_FILENAME):
        # Если файл с базой данных уже существует, то не будем его создавать еще раз
        create_db = False
    db.bind(provider='sqlite', filename=DATABASE_FILENAME, create_db=create_db)
    db.generate_mapping(create_tables=create_db)


@app.get("/authors", tags=['author'])
async def get_all_authors():
    with db_session:
        authors = Author.select()
        out_authors = []
        for i in authors:
            out_authors.append(AuthorOut.from_orm(i))
    return out_authors


@app.get("/author/{author_id}", tags=['author'])
async def get_author(author_id: int):
    with db_session:
        author = Author.get(author_id)
        AuthorOut.from_orm(author)
        return author


@app.post("/author/new", tags=['author'])
async def create_author(new_author: CreateAuthor = Body(...)):
    with db_session:
        author = Author(**new_author.dict())
        commit()
    return AuthorOut.from_orm(author)


@app.put("/author/edit/{author_id}", tags=['author'])
async def edit_author(author_id: int, editing_author: EditAuthor = Body(...)):
    with db_session:
        edit_author_dict = editing_author.dict(
            # https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict
            exclude_unset=True,
            exclude_none=True
        )
        Author[author_id].set(**edit_author_dict)
        commit()  # сохранение изменений в базе данных
        return AuthorOut.from_orm(Author[author_id])


@app.delete("/author/delete/{author_id}", tags=['author'])
async def delete_author(author_id: int):
    with db_session:
        Author[author_id].delete()
        commit()
        authors = Author.select()
        out_authors = []
        for i in authors:
            out_authors.append(AuthorOut.from_orm(i))
    return out_authors


@app.get("/books", tags=['book'])
async def get_all_books():
    with db_session:
        books = Book.select()
        out_authors = []
        for i in books:
            out_authors.append(OutBookYet.from_orm(i))
    return out_authors


@app.get("/book/{book_id}", tags=['book'])
async def get_book(book_id: int):
    with db_session:
        book = Book.get(book_id)
        return OutBookYet.from_orm(book)


@app.post("/book/new", tags=['book'])
async def create_book(new_book: CreateBook = Body(...)):
    with db_session:
        new_book_dict = new_book.dict()
        Book(
            **new_book_dict  # разыменование словаря, если хотите, почитайте сами
        )
        commit()  # сохранение изменений в базе данных
    return new_book


@app.put("/book/edit/{book_id}", tags=['book'])
async def edit_book(book_id: int, edit_book: EditBook = Body(...)):
    with db_session:
        edit_book_dict = edit_book.dict(
            # https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict
            exclude_unset=True,
            exclude_none=True
        )
        Book[book_id].set(**edit_book_dict)
        commit()  # сохранение изменений в базе данных
        return OutBookYet.from_orm(Book[book_id])


@app.delete("/book/delete/{book_id}", tags=['book'])
async def delete_book(book_id: int):
    with db_session:
        Book[book_id].delete()
        commit()
        books = Book.select()
        out_books= []
        for i in books:
            out_books.append(OutBookYet.from_orm(i))
    return out_books

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
