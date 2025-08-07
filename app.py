from flask import Flask, render_template, request, redirect
import sqlite3
from allocator import allocate_rooms  # Import allocation function


app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('student_form.html')

# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    gender = request.form['gender']
    batch = request.form['batch']
    roommate = request.form['roommate']
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, gender, batch, roommate) VALUES (?, ?, ?, ?)",
              (name, gender, batch, roommate))
    conn.commit()
    conn.close()

    # Automatically run allocation after new student is added
    allocate_rooms()
    
    return "Form Submitted and Room Allocation Done!"

# Admin dashboard route
@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    c.execute("SELECT * FROM rooms")
    rooms = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', students=students, rooms=rooms)

# Add a new room
@app.route('/add_room', methods=['POST'])
def add_room():
    room_no = request.form['room_no']
    gender = request.form['gender']
    capacity = int(request.form['capacity'])

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO rooms (room_no, gender, capacity) VALUES (?, ?, ?)",
              (room_no, gender, capacity))
    conn.commit()
    conn.close()
    return redirect('/admin')

# Manual route to run allocation
@app.route('/run_allocation')
def run_allocation():
    allocate_rooms()
    return redirect('/admin')

# View all allocations
@app.route('/allocations')
def view_allocations():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        SELECT students.name, rooms.room_no
        FROM allocations
        JOIN students ON allocations.student_id = students.id
        JOIN rooms ON allocations.room_id = rooms.id
    ''')
    results = c.fetchall()
    conn.close()
    return render_template('allocations.html', results=results)

# Form to check student allocation by name
@app.route('/check')
def check_form():
    return render_template('check_form.html')

@app.route('/get_room', methods=['POST'])
def get_room():
    student_name = request.form['name']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Find student by name
    c.execute("SELECT id FROM students WHERE name = ?", (student_name,))
    student = c.fetchone()

    if not student:
        conn.close()
        return f"No student found with name {student_name}"

    student_id = student[0]

    # Find allocation
    c.execute('''
        SELECT rooms.room_no
        FROM allocations
        JOIN rooms ON allocations.room_id = rooms.id
        WHERE allocations.student_id = ?
    ''', (student_id,))
    room = c.fetchone()
    conn.close()

    if room:
        return f"{student_name}, you have been allocated Room No: {room[0]}"
    else:
        return f"{student_name}, you have not been allocated a room yet."
@app.route('/reset_allocations', methods=['POST'])
def reset_allocations():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM allocations")
    c.execute("UPDATE rooms SET allocated = 0")
    conn.commit()
    conn.close()
    return redirect('/admin')


    

if __name__ == '__main__':
    app.run(debug=True)
