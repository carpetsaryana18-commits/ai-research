
import sqlite3

def init_db():
    conn = sqlite3.connect('research_assistant.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Create activity table
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            activity_type TEXT NOT NULL,
            query TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Add default users if they don't exist
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'admin', 'admin'))
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('user1', 'user1', 'user'))
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('user2', 'user2', 'user'))
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('user3', 'user3', 'user'))
    except sqlite3.IntegrityError:
        # Users already exist
        pass
    
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('research_assistant.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def log_activity(user_id, activity_type, query):
    conn = sqlite3.connect('research_assistant.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity (user_id, activity_type, query) VALUES (?, ?, ?)", (user_id, activity_type, query))
    conn.commit()
    conn.close()

def get_user_activity():
    conn = sqlite3.connect('research_assistant.db')
    c = conn.cursor()
    c.execute('''
        SELECT u.username, a.activity_type, a.query
        FROM activity a
        JOIN users u ON a.user_id = u.id
        WHERE u.role = 'user'
    ''')
    activity = c.fetchall()
    conn.close()
    return activity
