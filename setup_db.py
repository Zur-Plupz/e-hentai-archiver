import sqlite3

from src.db.sqlite import get_connection

with open('./schema/db.sql', 'r') as f:
  sql = f.read()

  db = get_connection('sadpanda.db')

  cursor = db.cursor()
  cursor.executescript(sql)

  db.commit()
  db.close()