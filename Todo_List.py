import os
import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database Configuration (Load from environment variables)
DB_NAME = os.getenv("DB_NAME", "todo_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "peters")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")


def connect_db() -> connection:
    """Establish and return database connection."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except Exception as e:
        logging.error("Database Connection Error: %s", e)
        raise


def create_table():
    """Create the tasks table if it does not exist."""
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        status BOOLEAN DEFAULT FALSE
                    )
                """)
                conn.commit()
                logging.info("Table created successfully.")
    except Exception as e:
        logging.error("Error creating table: %s", e)


def add_task(title: str):
    """Insert a new task into the database."""
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id", (title,))
                task_id = cur.fetchone()[0]
                conn.commit()
                logging.info("Task '%s' added with ID %d.", title, task_id)
    except Exception as e:
        logging.error("Error adding task: %s", e)


def list_tasks():
    """Fetch and display all tasks, renumbered sequentially for display."""
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tasks ORDER BY id")
                tasks = cur.fetchall()
                print("\nTasks:")
                print("{:<5} {:<30} {:<10}".format("No.", "Title", "Status"))
                print("-" * 50)
                for idx, task in enumerate(tasks, start=1):  # Dynamically renumber
                    print(f"{idx:<5} {task[1]:<30} {'✔️ Done' if task[2] else '⌛ Pending'}")
    except Exception as e:
        logging.error("Error listing tasks: %s", e)



def update_task(task_no: int, status: bool):
    """Update the status of a task using its displayed number."""
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                # Fetch the actual database ID of the nth task
                cur.execute("SELECT id FROM tasks ORDER BY id")
                tasks = cur.fetchall()
                if 0 < task_no <= len(tasks):
                    task_id = tasks[task_no - 1][0]  # Map display number to real ID
                    cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
                    conn.commit()
                    logging.info("Task %d marked as %s.", task_no, "Done" if status else "Pending")
                else:
                    print("Task number not found.")
    except Exception as e:
        logging.error("Error updating task: %s", e)



def delete_task(task_no: int):
    """Delete a task using its displayed number."""
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                # Fetch the actual database ID of the nth task
                cur.execute("SELECT id FROM tasks ORDER BY id")
                tasks = cur.fetchall()
                if 0 < task_no <= len(tasks):
                    task_id = tasks[task_no - 1][0]  # Map display number to real ID
                    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                    conn.commit()
                    logging.info("Task %d deleted.", task_no)
                else:
                    print("Task number not found.")
    except Exception as e:
        logging.error("Error deleting task: %s", e)



def main():
    """Main menu loop for the To-Do List Application."""
    create_table()  # Ensure table exists
    while True:
        print("\nTo-Do List")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter task title: ").strip()
            if title:
                add_task(title)
            else:
                print("Task title cannot be empty.")
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to mark as done: "))
                update_task(task_id, True)
            except ValueError:
                print("Invalid task ID.")
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to delete: "))
                delete_task(task_id)
            except ValueError:
                print("Invalid task ID.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
