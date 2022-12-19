"""Server for movie benevolence app."""
from __future__ import print_function
from flask import (Flask, render_template, request, flash, session, redirect, jsonify)

from model import connect_to_db, db, User, Recipient, Note, Like, Prompt, Event, Note
import crud
import os
from jinja2 import StrictUndefined


import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

SCOPES = ['https://www.googleapis.com/auth/calendar']

#  routes and view functions!
@app.route('/')
def homepage():
    """Create a route to view homepage"""
    return render_template('home_page.html')

#  Create Account
@app.route('/users/new', methods=["POST"])
def register_user():
    """Create account for new users"""
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("Email already exist. Login or Try again.")
        return redirect("/")
    else:
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
        return redirect("/")

# Login
@app.route("/login", methods=["POST"])
def process_login():
    """process user login"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.fname}!")
    return redirect(f"/recipients/{user.user_id}")

#Logout
@app.route("/logout")
def logout_user():
    """process user log out"""
    session.pop('user', None)
    return redirect("/")

#Google API helper function
def connect_google_API():
    creds = None
        # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return(creds)


# create route to recipient profile page
@app.route("/recipient_profile/<recipient_id>")
def recipient_profile(recipient_id):
    """create route to reciepient profile page"""
    recipient = crud.get_recipient_by_id(recipient_id)
    return render_template('recipient_details.html', recipient=recipient)

# see all recipients by user id
@app.route("/recipients/<user_id>")
def users_recipients(user_id):
    """create route to all users recipients """
    user = crud.get_user_by_id(user_id)
    recipients = crud.get_recipients(user_id)
    return render_template("recipient_index.html", recipients=recipients, user=user)

#create new like
@app.route("/likes/new", methods=["POST"])
def create_likes(recipient_id):
    """"Create likes """
    logged_in_email = session.get("user_email")
    prompt = request.form.get("event")
    if logged_in_email is None:
        flash("You must log in to add an like.")
    elif not prompt:
        flash("Error: you didn't answer any questions about your recipient.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        recipient = crud.get_recipient_by_id(recipient_id)

        like = crud.create_like(user, prompt, recipient)

# create new event
@app.route("/recipients/<recipient_id>/events", methods=["POST"])
def create_event(recipient_id):
    """create events"""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("you must log in to add an event")
        return redirect("/")
    else:
        event_name = request.form.get("event_name")
        event_date = request.form.get("event_date")
        recipient = crud.get_recipient_by_id(recipient_id)
        print('!' * 40)
        print(event_date)

    creds = connect_google_API()
    print('!' * 40)
    print(f" creds print out {creds}")
    try:

        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        event = {
            'summary': event_name,
            # 'location': '1750 Stone Ridge Drive, Stone Mountain, GA 30083',
            'description': event_name,
            'start': {
                'date': event_date,
                'timeZone': 'America/New_York',
            },
            'end': {
                'date': event_date,
                'timeZone': 'America/New_York',
            },
        }


        event = service.events().insert(calendarId='primary', body=event).execute()
        event_gid = event['id']
        print('$' * 40)
        print(event_gid)
        print("!" *40)
        print(event)
    except HttpError as error:
        print('An error occurred: %s' % error)
    event = crud.create_event(recipient, event_name, event_date, event_gid)

    db.session.add(event)
    db.session.commit()
    flash(f"You have added {event_name} to this recipient")

    return redirect(f"/recipients_profile/{recipient.recipient_id}")

# recipient detail page
@app.route("/recipients_profile/<recipient_id>")
def show_recipient(recipient_id):
    """Show details of a particular recipient"""
    recipient = crud.get_recipient_by_id(recipient_id)
    return render_template("recipient_details.html", recipient=recipient)

# Create new recipient
@app.route("/recipients/new/<user_id>", methods=["POST"])
def  add_recipient(user_id):
    """create new Recipient"""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("You must log in to add a recipient")
        return redirect("/")
    else:
        user = crud.get_user_by_id(user_id)
        r_name = request.form.get("new_r_name")

        recipient = crud.create_recipient(user, r_name)

        db.session.add(recipient)
        db.session.commit()
        flash(f"You have added {r_name} to your profile!")
        return redirect(f"/recipients/{user.user_id}")

#create note
@app.route("/note/new/<event_id>", methods=["Post", "GET"])
def create_new_note(event_id):
    """create new note for event"""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash('You moust be logged in to create a note')
        return redirect("/")
    else:
        user = crud.get_user_by_email(logged_in_email)
        content = request.form.get("note")
        event = crud.get_event_by_id(event_id)
        note = crud.create_note(event, content)
        event_name = event.event_name
        

        db.session.add(note)
        db.session.commit()
        flash(f"You added your notes for {event_name}!")
    
        return redirect(f"/note/api/{event_id}")

# add description to google API
@app.route("/note/api/<event_id>")
def add_google_description(event_id):
    """Add description to event on Google calendar"""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("you must log in to add an event")
        return redirect("/")
    else:
        user = crud.get_user_by_email(logged_in_email)  
        event = crud.get_event_by_id(event_id) 
        recipient_Id= event.recipient.recipient_id
        recipient = crud.get_recipient_by_id(recipient_Id) 
        note = event.note.note_id
        print('^'*40)
        print(note)
        content = event.note.content
        print('&'*40)
        print(content)
        event_gid = crud.get_event_gid(event_id)
        creds = connect_google_API()
    try:

        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        event = service.events().get(calendarId='primary', eventId= event_gid).execute()
        print('!'*40)
        print(event)
        event['description'] = content
        updated_event = service.events().update(calendarId='primary', eventId=event_gid, body=event).execute()
        #print the updated date
        print(updated_event['description'])
    except HttpError as error:
        print('An error occurred: %s' % error)  
    return redirect(f"/recipients_profile/{recipient.recipient_id}")

# Edit date format for Jinja templates
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d, %Y'):
    """change date format"""
    return value.strftime(format)

# Update Note content
@app.route("/update_note", methods=["POST"])
def update_note():
    """change note content"""
    note_id = int(request.json["note_id"])
    
    
   
    note = crud.get_note_by_id(note_id)
    print('^' * 40)
    print(note)
    event_id=note.event_id
    event = crud.get_event_by_id(event_id)
    print('!' * 40)
    print(event)
    recipient_Id = event.recipient.recipient_id
    recipient = crud.get_recipient_by_id(recipient_Id)
    print('!' * 40)
    print(recipient)
    update_content = request.json["update_content"]
    crud.update_note(note_id, update_content)
    db.session.commit()
    flash(f"You have succesfully updated this note in the database")
    content = event.note.content
    print('&'*40)
    print(content)
    event_gid = crud.get_event_gid(event_id)
    creds = connect_google_API()
    try:

        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        event = service.events().get(calendarId='primary', eventId= event_gid).execute()
        print('!'*40)
        print(event)
        event['description'] = content
        updated_event = service.events().update(calendarId='primary', eventId=event_gid, body=event).execute()
        #print the updated date
        print(updated_event['description'])
        flash(f"Google Calendar has your note")
    except HttpError as error:
        print('An error occurred: %s' % error)  
        flash(f" Error content update to Google calendar was unsuccessful")
    return redirect(f"/recipients_profile/{recipient.recipient_id}")

    # Delete Recipient
@app.route("/remove_recipient/<recipient_id>",methods=["POST"] )
def recipient_delete(recipient_id):
    print('!'*40)
    print(recipient_id)
    recipient_id = int(recipient_id)
    print(recipient_id)
    recipient = crud.get_recipient_by_id(recipient_id)
    events = crud.get_all_events(recipient_id)
    
    print(events)
    for event in events:
        event_id = event.event_id
        note = crud.get_all_notes(event_id)
        db.session.delete(note)
        db.session.delete(event)
    db.session.delete(recipient)
    db.session.commit()
    return {"status":"Success"}

   









    
if __name__ == "__main__":
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True, port=5001)