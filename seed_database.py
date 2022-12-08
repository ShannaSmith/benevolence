import os
import model
import crud
import server
import names

# drop and create new databse
os.system('dropdb benevolence')
os.system('createdb benevolence')

# connect to the database
model.connect_to_db(server.app)

# Updates the database schema
model.db.create_all()

# creating standard prompts
prompt_one = model.Prompt(prompt_name='What is their favorite color?')
model.db.session.add(prompt_one)
prompt_two = model.Prompt(prompt_name='What is their favorite food?')
model.db.session.add(prompt_two)
prompt_three = model.Prompt(prompt_name='what are their hobbies/interest?')
model.db.session.add(prompt_three)
prompt_four = model.Prompt(prompt_name='What is their favorite sport?')
model.db.session.add(prompt_four)
prompt_five = model.Prompt(prompt_name='What is their favorite sports team?')
model.db.session.add(prompt_five)

model.db.session.commit()

# use create methods to add objects to database

# Create an user
for n in range(10):
    fname = names.get_first_name()
    lname = names.get_last_name()
    email = f'{fname}@test.com'
    password = 'test'
    user =crud.create_user(fname, lname, email, password)
    model.db.session.add(user)
# Create 10 fake recipients for user
for i in range(10):
    r_name = names.get_full_name()
    recipient = crud.create_recipient(user, r_name)
    model.db.session.add(recipient)

model.db.session.commit()