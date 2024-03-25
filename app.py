from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def createConnection():
  connection = sqlite3.connect('books.db')
  return connection

def create_table():
  connection = createConnection()
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

