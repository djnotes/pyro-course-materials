from sqlalchemy.orm import Session
from sqlalchemy import select
from db import Note

def selectNotes(session: Session, user_id: int) -> str:
    stmt = select(Note).where(Note.author_id == user_id)    
    notesText = ""
    for note in session.scalars(stmt):
        notesText += note.title + ":" + note.text + '\n'
    return notesText