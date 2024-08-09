from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse  # Import the RedirectResponse
from . import models, database
import string
import random

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.post("/shorten/")
def shorten_url(original_url: str, db: Session = Depends(database.get_db)):
    short_url = generate_short_url()
    url_entry = models.URL(original_url=original_url, short_url=short_url)
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)
    return {"short_url": f"http://localhost:8000/{short_url}"}

@app.get("/{short_url}")
def redirect_to_url(short_url: str, db: Session = Depends(database.get_db)):
    url_entry = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    if url_entry is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Use RedirectResponse to redirect the user to the original URL
    return RedirectResponse(url=url_entry.original_url)
