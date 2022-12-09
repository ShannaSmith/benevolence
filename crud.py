"""CRUD operation functions"""
from model import db, User, Recipient, Note, Like, Event, Prompt, connect_to_db

#Functions  start here:
def create_user(fname, lname, email, password):
    """Create and return a new user."""
    user= User(fname=fname, lname=lname, email=email, password=password)
    return user

def get_recipients(user_id):
        """return a list of all recipientnames with a link to that user"""
        return Recipient.query.filter(User.user_id == user_id).all()

def get_recipient_by_id(recipient_id):
    """return recipient using its ID"""
    return Recipient.query.get(recipient_id)

def get_user_by_email(email):
    """return user using their email address"""
    return User.query.filter(User.email == email).first()

def create_recipient(user, r_name):
    """create new recipient """
    recipient= Recipient(user=user, r_name=r_name)
    return recipient

def create_like(prompt, recipient, like_name):
    """create a prompt"""
    like=Like(prompt=prompt, recipient=recipient, like_name=like_name)
    return like


if __name__=='__main__':
    from server import app
    connect_to_db(app)