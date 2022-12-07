"""CRUD operation functions"""
from model import db, User, Recipient, Note, Like, Event, Prompt, connect_to_db

#Functions  start here:
def create_user(email, password):
    """Create and return a new user."""
    user= User(email=email, password=password)
    return user

def get_recipients():
        """return a list of all recipientnames with a link to that user"""
        return Recipient.query.all()

def get_recipient_by_id(recipient_id):
    """return recipient using its ID"""
    return Recipient.query.get(recipient_id)

def get_user_by_email(email):
    """return user using their email address"""
    return User.query.filter(User.email == email).first()

def create_recipient(r_name, ranking):
    """create new recipient """
    recipient= Recipient(r_name=r_name, ranking=ranking)
    return recipient

