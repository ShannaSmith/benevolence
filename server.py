"""Server for movie benevolence app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db, User, Recipient, Note, Like, Prompt
import crud
import os
from jinja2 import StrictUndefined
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

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
    print(user.user_id)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
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
    else:
        event_name = request.form.get("event_name")
        event_date = request.form.get("event_date")
        recipient = crud.get_recipient_by_id(recipient_id)

        event = crud.create_event(recipient, event_name, event_date)

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








    
if __name__ == "__main__":
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True, port=5001)