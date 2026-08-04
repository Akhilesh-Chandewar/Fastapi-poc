from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

ALLOWED_FILE_EXTENSIONS = {".pdf", ".docx", ".txt"}

UPLOAD_DIR = "uploads"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
