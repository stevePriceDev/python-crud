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
  connection.close()
  return book_id

@app.post('/books/')
def create_book_endpoint(book: BookCreate):
  book_id = create_book(book)
  return {'id': book_id, **book.model_dump()}

