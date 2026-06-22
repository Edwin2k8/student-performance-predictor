import sqlite3

conn = sqlite3.connect("database/records.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_hours REAL,
    attendance REAL,
    previous_marks REAL,
    predicted_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("Database created successfully")