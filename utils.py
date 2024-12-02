import uuid

def get_unique_id(length):
    return str(uuid.uuid4())[:length]  # Unique ID for student of specified length
