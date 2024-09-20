import psycopg2
from datetime import date

def get_db_connection():
    return psycopg2.connect(
        dbname="tracker",
        user="fahmy",  
        password="ali",  
        host="localhost"
    )

# Create a new habit
def create_habit(name, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO habits (name, description) 
        VALUES (%s, %s) 
        RETURNING id, name, description
    ''', (name, description))
    habit = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    print(f"Habit '{habit[1]}' created successfully.")
    return habit

# Mark habit as completed
def mark_habit_completed(habit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO habit_logs (habit_id, completed_on) 
        VALUES (%s, %s)
    ''', (habit_id, date.today()))
    
    cur.execute('''
        UPDATE habits 
        SET total_completed = total_completed + 1 
        WHERE id = %s
    ''', (habit_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Habit ID {habit_id} marked as completed today.")

# View all habits
def view_habits():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, total_completed FROM habits')
    habits = cur.fetchall()
    cur.close()
    conn.close()
    
    print("Habits:")
    for habit in habits:
        print(f"ID: {habit[0]} | Name: {habit[1]} | Description: {habit[2]} | Times Completed: {habit[3]}")

# View progress of a single habit
def view_habit_progress(habit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT h.id, h.name, h.total_completed, COUNT(l.id) AS times_completed 
        FROM habits h 
        LEFT JOIN habit_logs l ON h.id = l.habit_id 
        WHERE h.id = %s 
        GROUP BY h.id
    ''', (habit_id,))
    habit = cur.fetchone()
    cur.close()
    conn.close()

    if habit:
        print(f"Habit: {habit[1]} | Total Completions: {habit[2]}")
    else:
        print(f"No habit found with ID {habit_id}.")

# Delete a habit
def delete_habit(habit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM habits WHERE id = %s', (habit_id,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Habit ID {habit_id} deleted.")

# Main CLI logic
def main():
    while True:
        print("\nHabit Tracker CLI")
        print("1. Create a new habit")
        print("2. Mark habit as completed")
        print("3. View all habits")
        print("4. View habit progress")
        print("5. Delete a habit")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter habit name: ")
            description = input("Enter habit description: ")
            create_habit(name, description)
        elif choice == '2':
            habit_id = int(input("Enter habit ID to mark as completed: "))
            mark_habit_completed(habit_id)
        elif choice == '3':
            view_habits()
        elif choice == '4':
            habit_id = int(input("Enter habit ID to view progress: "))
            view_habit_progress(habit_id)
        elif choice == '5':
            habit_id = int(input("Enter habit ID to delete: "))
            delete_habit(habit_id)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
