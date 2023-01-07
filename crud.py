"""CRUD operation functions"""
import psycopg2
from model import db, User, Recipient, Note, Like, Event, Prompt, connect_to_db

#Functions  start here:
def create_user(fname, lname, email, password):
    """Create and return a new user."""
    user= User(fname=fname, lname=lname, email=email, password=password)
    return user

def get_recipients(user_id):
    """return a list of all recipient names with a link to that user"""
    return Recipient.query.filter(user_id == Recipient.user_id).all()

def get_recipient_by_id(recipient_id):
    """return recipient using its ID"""
    return Recipient.query.get(recipient_id)

def get_user_by_email(email):
    """return user using their email address"""
    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    return User.query.filter(User.user_id == user_id).first()

def create_recipient(user, r_name):
    """create new recipient """
    recipient= Recipient(user=user, r_name=r_name)
    return recipient

def create_like(prompt_id, recipient, like_name):
    """create a prompt"""
    like = Like(prompt_id=prompt_id, recipient=recipient, like_name=like_name)
    return like

def create_event(recipient, event_name, event_date, event_gid):
    """create new event"""
    events = Event(event_name=event_name, event_date=event_date, event_gid=event_gid, recipient=recipient)
    return events

def create_note(event, content):
    """create new note"""
    note = Note(event=event, content=content)
    return note

def get_event_by_id(event_id):
    return Event.query.filter(Event.event_id == event_id).first()

def get_note_by_id(note_id):
    return Note.query.filter(Note.note_id == note_id).first()

def update_note(note_id, update_content):
    """update a note given note_id and the updated content"""
    note = Note.query.get(note_id)
    note.content = update_content

def get_all_events(recipient_id):
    return Event.query.filter(Event.recipient_id == recipient_id).all()

def get_all_notes(event_id):
    return Note.query.filter(Note.event_id == event_id).first()

def get_event_gid(event_id):
    event = Event.query.filter(Event.event_id == event_id).first()
    return event.event_gid

def get_all_prompts():
    return  Prompt.query.all()

def get_all_likes(recipient_id):
    return Like.query.filter(Like.recipient_id == recipient_id).all()


 




if __name__=='__main__':
    from server import app
    connect_to_db(app)

