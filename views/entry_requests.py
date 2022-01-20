import sqlite3
import json
from models import Entry
from models.mood import Mood

# ENTRIES = [
#     {
#         "id": 1,
#         "concept": "Python",
#         "entry": "test entry", 
#         "date": "date1",
#         "mood_id": 1
#     },
#     {
#         "id": 2,
#         "concept": "JS",
#         "entry": "test entry2", 
#         "date": "date2",
#         "mood_id": 2
#     }
# ]

# def get_all_animals():
#     return ENTRIES


def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        """)
        
        entries = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            mood = Mood(row['id'], row['label'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
            
    
    return json.dumps(entries)

# Function with a single parameter
def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['date'], data['mood_id'])
        mood = Mood(data['id'], data['label'])
        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)
    
def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM Entries
        WHERE id = ?
        """, (id, ))

def search_entries(searchTerms):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM Entries e
        WHERE e.entry LIKE ?;
        """, (f"%{searchTerms}%", ))
        
        entries = []
        dataset = db_cursor.fetchall()
        
        
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            entries.append(entry.__dict__)
    
    return json.dumps(entries)
        