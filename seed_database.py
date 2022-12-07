import os
import model
import server

os.system('dropdb benevolence')
os.system('createdb benevolence')

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

# TODO: use create methods to add objects to database
