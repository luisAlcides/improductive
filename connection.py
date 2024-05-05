import sqlite3

SQL_CREATE_TABLE_CATEGORY_HABIT = '''CREATE TABLE IF NOT EXISTS category_habits(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created DATETIME DEFAULT CURRENT_TIMESTAMP 
    )
'''

SQL_CREATE_TABLE_HABIT = '''CREATE TABLE IF NOT EXISTS habit(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER,
    study_time REAL,
    FOREIGN KEY (category_id) REFERENCES category_habits(id)
    
    )'''


SQL_CREATE_TABLE = [SQL_CREATE_TABLE_CATEGORY_HABIT, SQL_CREATE_TABLE_HABIT]


class Connection:
    def __init__(self):
        self.con = None

    def __enter__(self):
        try:
            self.con = sqlite3.connect('database.db')
            return self.con.cursor()
        except Exception as e:
            print('Database connection error:', e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.con:
            self.con.commit()
            self.con.close()
            self.con = None

    def create_tables(self):
        with self as cursor:
            try:
                for table in SQL_CREATE_TABLE:
                    cursor.execute(table)
            except sqlite3.OperationalError as e:
                print('Error creating tables: ', e)

    
    def setup_database(self):
        with self as cursor:
            Connection.create_tables(self)
