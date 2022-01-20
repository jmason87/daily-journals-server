import json
import sqlite3
from models import Mood

def get_all_moods():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """)
        
        moods = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)
    
    return json.dumps(moods)

def get_single_mood(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        WHERE m.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        entry = Mood(data['id'], data['label'])

        return json.dumps(entry.__dict__)
