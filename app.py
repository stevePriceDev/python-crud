from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def create_connection():
  connection = sqlite3.connect('books.db')
  return connection

def create_table():
  connection = create_connection()
  cursor = connection.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS books (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      author TEXT NOT NULL
  )             
  """)
  connection.commit()
  connection.close()

create_table()

@app.get('/')
def read_root():
  return {'message': 'Welcome to the CRUD API'}

class BookCreate(BaseModel):
  title: str
  author: str

class Book(BookCreate):
  id: int

def create_book(book: BookCreate):
  connection = create_connection()
  cursor = connection.cursor()
  cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (book.title, book.author))
  connection.commit()
  book_id = cursor.lastrowid
  new_book = Book(id=book_id, title=book.title, author=book.author)
  connection.close()
  return new_book

@app.post('/books/')
def create_book_endpoint(book: BookCreate):
  new_book = create_book(book)
  return new_book

def find_all_books():
  connection = create_connection()
  cursor = connection.cursor()
  db_results = cursor.execute('SELECT * FROM books')
  connection.commit()
  list = [book for book in db_results]
  connection.close()
  return list

@app.get('/books/')
def read_all_books():
  books_list = find_all_books()
  return books_list

def find_one_book(id: int):
  connection = create_connection()
  cursor = connection.cursor()
  book = cursor.execute('SELECT * FROM books WHERE id = ?', (id))
  connection.commit()
  result = book.fetchone()
  connection.close()
  return result

@app.get('/books/{id}')
def read_one_book(id: str):
  book_id = id
  book = find_one_book(book_id)
  return book


