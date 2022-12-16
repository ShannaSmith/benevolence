"""Models for benevolence app"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """benevolent people"""
    __tablename__ = "users"
    user_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(10))
   
    recipients = db.relationship('Recipient', back_populates='user')
    events =db.relationship('Event',back_populates='user')
   
    def __repr__(self):
        return f"<User ID={self.user_id} Name={self.fname} {self.lname} Email={self.email}>"

class Recipient(db.Model):
    """"receivers of benevolent acts"""
    __tablename__ = "recipients"
    recipient_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    r_name = db.Column(db.String(50), nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    events = db.relationship('Event', back_populates='recipient')
    notes = db.relationship('Note', back_populates='recipient')
    user = db.relationship('User', back_populates='recipients')
    likes = db.relationship('Like', back_populates='recipient')

    def __repr__(self):
        return f"<Recipient ID={self.recipient_id} Name={self.r_name}>"

class Like(db.Model):
    """What our recipients like"""

    __tablename__ = "likes"
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    like_name = db.Column(db.String(40), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("recipients.recipient_id"), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompts.prompt_id"), nullable=False)

    recipient = db.relationship('Recipient', back_populates='likes')
    prompt = db.relationship('Prompt',back_populates='likes' )

    def __repr__(self):
        return f"<Like ID={self.like_id} Name={self.like_name}>"

class Event(db.Model):
    """Benevolent Acts"""
    __tablename__="events"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    event_name = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_gid = db.Column(db.String(40), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("recipients.recipient_id"))
    # note_id = db.Column(db.Integer, db.ForeignKey("notes.note_id"), nullable=True)

    user = db.relationship('User', back_populates='events')
    recipient = db.relationship('Recipient', back_populates='events')
    note = db.relationship('Note', uselist=False, back_populates='event')

    def __repr__(self):
        return f"<Event ID={self.event_id} Name={self.event_name} Date={self.event_date}>"

class Note(db.Model):
    """Comments about how well benevolent acts were received"""

    __tablename__="notes"
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = db.Column(db.Text, nullable=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("recipients.recipient_id"), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), nullable=False)

    recipient = db.relationship('Recipient', back_populates='notes')
    event = db.relationship('Event', uselist=False, back_populates='note')

    def __repr__(self):
        return f"<Note ID={self.note_id} Content={self.content[:20]}>"

class Prompt(db.Model):
    """Form questions about recipients favorite things"""
    __tablename__="prompts"
    prompt_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    prompt_name = db.Column(db.String(100), nullable=True)

    likes = db.relationship('Like', back_populates='prompt' )

    def __repr__(self):
        return f"<Prompt ID={self.prompt_id} Question={self.prompt_name[:40]}>"


def connect_to_db(app, db_url="postgresql:///benevolence", echo=True):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_ECHO"] = echo
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    app.app_context().push()
    print("Connected to the db!")

if __name__ == "__main__":
    from flask import Flask
    app= Flask(__name__)
    connect_to_db(app)