from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
import sqlite3
import base64
from dotenv import load_dotenv
import json

def add_json_metadata(username: str, password: str, metadata: str, database: str = "databases/database.db"):
    """
    metadata = "{
        "ip": "127.0.0.1",
        "browser": "Firefox",
        "tags": ["new_user", "beta"]
    }"
    """

    metadata_str = json.dumps(metadata)
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
    "UPDATE users SET additional_metadata = ? WHERE username = ? AND password = ?",
        (metadata_str, username, base64.b64encode(password.encode("utf-8")).decode("utf-8")
    )
    )
    conn.commit()
    conn.close()

def create_database_table(database_path: str = "databases/database.db"):
    conn = sqlite3.connect(database_path)
    translator = conn.cursor()
    translator.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    signUpTime TEXT,
    additional_metadata TEXT
    );
    """) # thanks chatgpt
    conn.commit()
    conn.close()

def insert_info(username, password, now, additional_metadata, database_path: str = "databases/database.db"):
    password = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    conn = sqlite3.connect(database_path)
    translator = conn.cursor()
    translator.execute(f"INSERT INTO users (username, password, signUpTime, additional_metadata) VALUES (?, ?, ?, ?)", (username, password, now, additional_metadata))
    conn.commit()
    conn.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/home", StaticFiles(directory="frontend/dist", html=True), name="home")

class User(BaseModel):
    username: str
    password: str
    now: str
    additional_metadata: str

@app.post("/api/request_signup")
def login_done(user: User):
    try:
        create_database_table()
        insert_info(user.username, user.password, user.now, user.additional_metadata)
        return {"user_message": "Login success!", "system_message": "Code 200 OK"}
    except Exception as e:
        print(f"Exception: {e}")
        if str(e) == "database is locked":
            return {"user_message": "Database is locked", "system_message": "CODE 400 FAIL"}
        elif str(e) == "UNIQUE constraint failed: users.username":
            return {"user_message": "Already existing username! Please select another one", "system_message": "CODE 400 FAIL"}
        else:
            return {"user_message": "We had a problem! Please try reloading the page or try again later on", "system_message": "CODE 400 FAIL"}