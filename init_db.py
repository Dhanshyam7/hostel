import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create student table
c.execute('''CREATE TABLE IF NOT EXISTS students
             (id INTEGER PRIMARY KEY,
              name TEXT,
              gender TEXT,
              batch TEXT,
              roommate TEXT)''')

# Create rooms table
c.execute('''CREATE TABLE IF NOT EXISTS rooms
             (id INTEGER PRIMARY KEY,
              room_no TEXT,
              gender TEXT,
              capacity INTEGER,
              allocated INTEGER DEFAULT 0)''')

# ✅ Create allocations table here
c.execute('''CREATE TABLE IF NOT EXISTS allocations
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              student_id INTEGER,
              room_id INTEGER)''')

conn.commit()
conn.close()
print("✅ Database initialized.")
