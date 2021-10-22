import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('CREATE TABLE IF NOT EXISTS uploads (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT not null,  distibution TEXT )')
conn.execute('CREATE TABLE IF NOT EXISTS upload_details ( upload_id INTEGER NOT NULL , name TEXT, population INTEGER , c3  INTEGER , c4 INTEGER, c5 DECIMAL, FOREIGN KEY (upload_id) REFERENCES  uploads (id) )')

print("Table created successfully")
conn.close()