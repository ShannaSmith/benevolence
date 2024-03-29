"""Server for benevolence app."""
from __future__ import print_function
from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)

from passlib.hash import pbkdf2_sha256
from model import connect_to_db, db, User, Recipient, Note, Like, Prompt, Event, Note
import crud
import os
from jinja2 import StrictUndefined
import requests   #<<<<<<TODO may need to delete

import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

SCOPES = ['https://www.googleapis.com/auth/calendar']
salt = os.urandom
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

    user = crud.check_hash_account(email, password)
    if not user:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        session["user_fname"] = user.fname
        flash(f"Welcome back, {user.fname}!")
    return redirect(f"/recipients/{user.user_id}")

#Logout
@app.route("/logout")
def logout_user():
    """process user log out"""
    session.pop("user_fname", None)
    session.pop('user_email', None)
    session.pop("user_id", None)
    flash("You are now logged out.")
    return redirect("/")

#Google API helper function
def connect_google_API():
    creds = None
        # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    print('>>>>>>>>>>>>>>>>>>>>>Entering the helper funct')
    if os.path.exists('token.json'):
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% token exist')
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print('$'*40, 'no creds')
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            
            # flow = InstalledAppFlow.from_client_secrets_file(
                # 'credentials.json', SCOPES)
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES)
            print("Creating Flow??????????????????????")
            flow.redirect_uri = url_for('oauth2callback', _external=True)
            authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
            session['state'] = state
            # creds = flow.run_local_server(port=0)
            print("running flow server????????????")
            print('!'*40, 'creds is', creds)
            print(dir(creds))
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("wrote token.json file??????????????")
    return(creds)

@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials.json", scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


# Oauth callback
@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('test_api_request'))

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


#toDO
# # create route to recipient profile page
# @app.route("/recipient_profile/<recipient_id>")
# def recipient_profile(recipient_id):
#     """create route to reciepient profile page"""
#     recipient = crud.get_recipient_by_id(recipient_id)
#     return render_template('recipient_details.html', recipient=recipient)

# see all recipients by user id
@app.route("/recipients/<user_id>")
def users_recipients(user_id):
    """create route to all users recipients """
    user = crud.get_user_by_id(user_id)
    recipients = crud.get_recipients(user_id)
    return render_template("recipient_index.html", recipients=recipients, user=user)

#create new like
@app.route("/likes/new/<recipient_id>", methods=["POST"])
def create_likes(recipient_id):
    """"Create likes """
    logged_in_email = session.get("user_email")
    
    if logged_in_email is None:
        flash("You must log in to add an like.")
        return jsonify(f"You have to log in")
    
    prompt_id = request.json.get("prompt_id")
    user_answer = request.json.get("user_answer") #<<<<needs to match the javascript not form
    
    user = crud.get_user_by_email(logged_in_email)
    recipient = crud.get_recipient_by_id(recipient_id)
    
    like = crud.create_like(prompt_id, recipient, user_answer)
    
    db.session.add(like)
    db.session.commit()
    return jsonify({'like_name':like.like_name} )

# create new event
@app.route("/recipients/<recipient_id>/events", methods=["POST"])
def create_event(recipient_id):
    """create events"""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        return jsonify("you must log in to add an event")
    else:
        event_name = request.json.get("event_name")
        event_date = request.json.get("event_date")
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
        return jsonify('An error occurred: %s' % error)

    event = crud.create_event(recipient, event_name, event_date, event_gid)

    db.session.add(event)
    db.session.commit()
    return jsonify({'event_id':event.event_id, 'event_name':event.event_name, 'event_date': event.event_date})

# recipient detail page
@app.route("/recipients_profile/<recipient_id>")
def show_recipient_page(recipient_id):
    recipient = crud.get_recipient_by_id(recipient_id)
    return render_template('recipient_details.html', recipient_id=recipient_id, recipient=recipient)


# recipient detail Ajax
@app.route("/api/recipients_profile/<recipient_id>")
def show_recipient(recipient_id):
    """Show details of a particular recipient"""
    recipient = crud.get_recipient_by_id(recipient_id)
    used_prompt_ids = set([like.prompt_id for like in recipient.likes])
    all_prompts = crud.get_all_prompts()
    prompts = []
    for prompt in all_prompts:
        if prompt.prompt_id not in used_prompt_ids:
            prompts.append(prompt)
    # convert recipient in prompt into dictionaries so they can be serialized
    data={'user_email':session.get('user_email')}
    data['recipient']={'recipient_id':recipient_id, 'r_name':recipient.r_name}
    
    events_data =[]
    for event in recipient.events:
        note_data = None
        if event.note != None:
            note_data = {'note_id':event.note.note_id, 'content':event.note.content}
        event_data ={'event_id':event.event_id, 'event_name':event.event_name, 'event_date':event.event_date, 'note':note_data}
        events_data.append(event_data)
    data['events'] = events_data
    
    prompts_data = []
    for prompt in prompts:
        prompt_data = {'prompt_id':prompt.prompt_id, 'prompt_name':prompt.prompt_name}
        prompts_data.append(prompt_data)
    data['prompts'] = prompts_data

    likes_data =[]
    for like in recipient.likes:
        like_data = {'like_id':like.like_id, 'like_name':like.like_name, 'recipient_id':like.recipient_id, 'prompt_id':like.prompt_id}
        likes_data.append(like_data)
    data['likes'] = likes_data

    return jsonify(data)

# Create new recipient
@app.route("/recipients/new/<user_id>", methods=["POST"])
def  add_recipient(user_id):
    """create new Recipient"""
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("You must log in to add a framily member")
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
        return jsonify('You must be logged in to create a note')
        
    
    user = crud.get_user_by_email(logged_in_email)
    event = crud.get_event_by_id(event_id)
    
    content = request.json.get("note")
    print('%' * 40, content)
    note = crud.create_note(event, content)
    print('^'*40)
    print(note)
    db.session.add(note)
    db.session.commit()
    
    event_name = event.event_name
    recipient_Id= event.recipient.recipient_id
    recipient = crud.get_recipient_by_id(recipient_Id) 
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
        print('the updated date')
        print(updated_event['description'])
    except HttpError as error:
        return jsonify('An error occurred: %s' % error)  

    return jsonify( {'note_id':note.note_id, 'content':note.content} )
    
# # add description to google API
# @app.route("/note/api/<event_id>")
# def add_google_description(event_id):
#     """Add description to event on Google calendar"""
#     logged_in_email = session.get("user_email")
#     if logged_in_email is None:
#         flash("you must log in to add an event")
#         return redirect("/")
#     else:
#         user = crud.get_user_by_email(logged_in_email)  
#         event = crud.get_event_by_id(event_id) 
#         recipient_Id= event.recipient.recipient_id
#         recipient = crud.get_recipient_by_id(recipient_Id) 
#         note = event.note.note_id
#         print('^'*40)
#         print(note)
#         content = event.note.content
#         print('&'*40)
#         print(content)
#         event_gid = crud.get_event_gid(event_id)
#         creds = connect_google_API()
#     try:

#         service = build('calendar', 'v3', credentials=creds)
#         now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#         event = service.events().get(calendarId='primary', eventId= event_gid).execute()
#         print('!'*40)
#         print(event)
#         event['description'] = content
#         updated_event = service.events().update(calendarId='primary', eventId=event_gid, body=event).execute()
#         print('the updated date')
#         print(updated_event['description'])
#     except HttpError as error:
#         print('An error occurred: %s' % error)  
#     return redirect(f"/recipients_profile/{recipient.recipient_id}")

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
    event_id=note.event_id
    event = crud.get_event_by_id(event_id)
    recipient_Id = event.recipient.recipient_id
    recipient = crud.get_recipient_by_id(recipient_Id)
    update_content = request.json["update_content"]
    crud.update_note(note_id, update_content)
    db.session.commit()
    flash(f"You have succesfully updated this note in the database")
    content = event.note.content
    event_gid = crud.get_event_gid(event_id)
    creds = connect_google_API()
    try:

        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        event = service.events().get(calendarId='primary', eventId= event_gid).execute()
        event['description'] = content
        updated_event = service.events().update(calendarId='primary', eventId=event_gid, body=event).execute()
        #print the updated date
        print(updated_event['description'])
        flash(f"Google Calendar has your note")
    except HttpError as error:
        print('An error occurred: %s' % error)  
        flash(f" Error content update to Google calendar was unsuccessful")
    return jsonify('successfully saved note')
   
    # Delete Recipient
@app.route("/remove_recipient/<recipient_id>",methods=["POST"] )
def recipient_delete(recipient_id):
    print('!'*40)
    print(recipient_id)
    recipient_id = int(recipient_id)
    print(recipient_id)
    recipient = crud.get_recipient_by_id(recipient_id)
    events = crud.get_all_events(recipient_id)
    likes =recipient.likes
    print(events)
    for event in events:
        event_id = event.event_id
        note = crud.get_all_notes(event_id)
        db.session.delete(note)
        db.session.delete(event)
    for like in likes:
        db.session.delete(like)
    
    db.session.delete(recipient)
    db.session.commit()
    return {"status":f" You have removed {recipient.r_name}"}

# Delete Event
@app.route("/remove_event/<event_id>", methods=["POST"])
def event_delete(event_id):
    """delete event"""
   
    event = crud.get_event_by_id(event_id)
    note = crud.get_all_notes(event_id)
    if note != None:
        db.session.delete(note)
        db.session.delete(event)
    else:
        db.session.delete(event)
    db.session.commit()
    return{"status":"Success"}


   









    
if __name__ == "__main__":
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True, port=5001)