import sqlite3

SQL_CREATE_TABLE_CATEGORY_HABIT = '''CREATE TABLE IF NOT EXISTS category_habits(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    date_current DATETIME
    )
'''

SQL_CREATE_TABLE_HABIT = '''CREATE TABLE IF NOT EXISTS habit(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_time REAL,
    category_id INTEGER,
    date_current DATETIME,
    FOREIGN KEY (category_id) REFERENCES category_habits(id)
    
    )
    '''

SQL_CREATE_TABLE_MONTHS = '''CREATE TABLE IF NOT EXISTS months(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    )
'''

SQL_CREATE_TABLE_GOAL = '''CREATE TABLE IF NOT EXISTS goal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal REAL,
    category_id INTEGER,
    month_id INTEGER,
    date_current DATETIME,
    FOREIGN KEY (category_id) REFERENCES category_habits(id),
    FOREIGN KEY (month_id) REFERENCES months(id)
    
    )'''

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

SQL_CREATE_TABLE = [SQL_CREATE_TABLE_CATEGORY_HABIT,
                    SQL_CREATE_TABLE_HABIT, SQL_CREATE_TABLE_GOAL, SQL_CREATE_TABLE_MONTHS]


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

    def insert_month(self):
        with self as cursor:
            cursor.execute('SELECT COUNT(*) FROM months')
            count = cursor.fetchone()[0]
            if count == 0:
                for month in months:
                    cursor.execute(
                        'INSERT INTO months(name) VALUES(?)', (month,))

    def setup_database(self):
        with self as cursor:
            Connection.create_tables(self)
            Connection.insert_month(self)
