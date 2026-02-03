# Configuration settings for the server
# Edit these values as needed

# Server settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# Face recognition settings
RECOGNITION_THRESHOLD = 0.6  # Lower = stricter (0.4-0.7 recommended)

# File paths
FACES_FILE = "registered_faces.json"
LOGS_FILE = "access_logs.json"

# Access log settings
MAX_LOGS = 100  # Maximum logs to keep
