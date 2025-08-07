import sqlite3

def allocate_rooms():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Clear old allocations
    c.execute("DELETE FROM allocations")

    # Reset allocated count in all rooms
    c.execute("UPDATE rooms SET allocated = 0")

    # Get all students, grouped by gender
    c.execute("SELECT * FROM students ORDER BY gender")
    students = c.fetchall()

    # Get all available rooms, ordered by gender
    c.execute("SELECT * FROM rooms ORDER BY gender")
    rooms = c.fetchall()

    room_index = 0
    allocations = []

    for student in students:
        student_id = student[0]
        student_gender = student[2]

        # Find next suitable room
        while room_index < len(rooms):
            room = rooms[room_index]
            room_id, room_no, room_gender, capacity, allocated = room

            if room_gender != student_gender or allocated >= capacity:
                room_index += 1
                continue

            # Allocate student
            allocations.append((student_id, room_id))

            # Update allocated count
            allocated += 1
            c.execute("UPDATE rooms SET allocated = ? WHERE id = ?", (allocated, room_id))

            # Update local copy too
            rooms[room_index] = (room_id, room_no, room_gender, capacity, allocated)
            break

    # Insert new allocations
    for student_id, room_id in allocations:
        c.execute("INSERT INTO allocations (student_id, room_id) VALUES (?, ?)", (student_id, room_id))

    conn.commit()
    conn.close()
    print(f"✅ Room allocation completed for {len(allocations)} students.")
