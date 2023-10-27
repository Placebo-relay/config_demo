import streamlit as st
import sqlite3

# Connect to the database
conn = sqlite3.connect('profiles.db')
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS profiles
             (name TEXT, option1 INTEGER, option2 INTEGER, option3 INTEGER,
             option4 INTEGER, option5 INTEGER, option6 INTEGER, option7 INTEGER,
             option8 INTEGER)''')

# Check if the default profile exists
c.execute("SELECT * FROM profiles WHERE name='Default'")
default_profile_exists = c.fetchone()

# If the default profile doesn't exist, create it
if not default_profile_exists:
    c.execute("INSERT INTO profiles VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0)", ('Default',))
    conn.commit()

# Get user input
name = st.text_input('Enter your name')
options = []
for i in range(8):
    option = st.checkbox(f'Option {i+1}')
    options.append(int(option))

# Store the data in the database
if st.button('Save') and name != 'Default':
    c.execute("INSERT INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, *options))
    conn.commit()
    st.success('Data saved successfully!')

# Display the stored data
st.subheader('Stored Profiles')
c.execute("SELECT * FROM profiles")
data = c.fetchall()
for row in data:
    st.write(f"Name: {row[0]}, Options: {row[1:]}")

# Close the database connection
conn.close()
