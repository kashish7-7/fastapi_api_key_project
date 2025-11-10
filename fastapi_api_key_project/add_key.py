from database import SessionLocal, APIKey, init_db

init_db()
db = SessionLocal()

new_key = APIKey(key="12345abcde")  # same key as before
db.add(new_key)
db.commit()
db.close()

print("API Key added to database.")
