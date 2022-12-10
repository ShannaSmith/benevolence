"""Server for movie benevolence app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
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
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.fname}!")
    return redirect("/")

#Logout
@app.route("/logout")
def logout_user():
    """process user log out"""
    session.pop('user', None)
    return redirect("/")

@app.route("/recipient_profile/<recipient_id>")
def recipient_profile(recipient_id):
    """render reciepient profile page"""
    recipient = crud.get_recipient_by_id(recipient_id)
    return render_template('recipient_details.html', recipient=recipient)

@app.route("/recipients/<user_id>")
def users_recipients(user_id):
    """display all users recipients """
    recipients = crud.get_recipients(user_id)
    return render_template("recipient_index.html", recipients=recipients)

@app.route("likes/new", methods=["POST"])
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

@app.route("/events/new/<recipient_id>", methods=["POST"])
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
    return redirect(f"/recipient_profile/{recipient_id}")
     




    
if __name__ == "__main__":
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True, port=5001)