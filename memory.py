import json
import os

# Memory file path
MEMORY_FILE = 'jarvis_memory.json'

# Load memory from file
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return []

# Save memory to file
def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

# Delete memory within a specific time range
def delete_memory(memory, start_time, end_time):
    memory = [m for m in memory if not (start_time <= m.get('timestamp', 0) <= end_time)]
    save_memory(memory)
