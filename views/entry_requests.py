import sqlite3
import json
from models import Entry, Mood

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
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'], [])
            mood = Mood(row['id'], row['label'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
            
            db_cursor.execute("""
            SELECT t.id, t.name
            FROM Entries e
            join Entrytag et on e.id = et.entry_id
            join Tag t on t.id = et.tag_id
            WHERE et.entry_id = ?
            """, (entry.id,)) 
            
            tagset = db_cursor.fetchall()
            for tag_data in tagset:
                tag = {'id': tag_data['id'], 'name': tag_data['name']}
                entry.tags.append(tag)
    
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

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Entries
            (concept, entry, date, mood_id)
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['mood_id']))
        
        id = db_cursor.lastrowid
        new_entry['id'] = id
        
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO Entrytag
                (entry_id, tag_id)
                VALUES (?, ?)
            """, (id, tag))
    
    return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Entries
            SET
                concept = ?,
                entry = ?,
                date = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['mood_id'], id, ))

        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True