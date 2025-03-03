import sqlite3

class Tasks:
    def __init__(self, db_name="todoist.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """ Create tasks table if not exists """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                date TEXT DEFAULT (CURRENT_TIMESTAMP)
            )              
            ''')
        
        self.conn.commit()
        
    
    def add_task(self, name, priority, status, date=None):
        """Insert a new task into the database."""
        if not date:
            self.cursor.execute("INSERT INTO tasks (name, priority, status) VALUES (?, ?, ?)", 
                            (name, priority, status))
        else:
            self.cursor.execute("INSERT INTO tasks (name, priority, status, date) VALUES (?, ?, ?, ?)", 
                            (name, priority, status, date))
        self.conn.commit()
        
    
    def get_tasks(self):
        """Fetch all tasks from the database."""
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def update_task(self, task_id, name=None, priority=None, status=None):
        """Update task details."""
        updates = []
        values = []

        if name:
            updates.append("name = ?")
            values.append(name)
        if priority:
            updates.append("priority = ?")
            values.append(priority)
        if status:
            updates.append("status = ?")
            values.append(status)

        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()
        
    def delete_task(self, task_id):
        """Delete a task from the database."""
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()