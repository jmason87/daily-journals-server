class Entry():
    
    def __init__(self, id, concept, entry, date, mood_id, tags=[]):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.date = date
        self.mood_id = mood_id
        self.mood = None
        self.tags = tags
