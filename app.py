from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = 'group59'

# Connect to the database
conn = sqlite3.connect('system.db')
c = conn.cursor()

# Create the users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')


# Check if the table is empty
c.execute("SELECT COUNT(*) FROM users")
row_count = c.fetchone()[0]

# Insert example data only if the table is empty
if row_count == 0:
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    c.execute("INSERT INTO users (username, password) VALUES ('student', 'student')")
    c.execute("INSERT INTO users (username, password) VALUES ('itladmin', 'itl')")
    c.execute("INSERT INTO users (username, password) VALUES ('eeadmin', 'ee')")
    c.execute("INSERT INTO users (username, password) VALUES ('ecadmin', 'ec')")
    c.execute("INSERT INTO users (username, password) VALUES ('itsadmin', 'itsadmin')")
    c.execute("INSERT INTO users (username, password) VALUES ('moduleorganiser', 'module')")
    conn.commit()

# Create the tickets table for issues
c.execute('''CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id))''')

# Create the ecs table for ECs
c.execute('''CREATE TABLE IF NOT EXISTS ecs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Save the changes and close the database
conn.commit()
conn.close()

# Login page, or home page if logged in
@app.route('/', methods=['GET', 'POST'])
def login() -> str:
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # try:
            # Connect to the database
            conn = sqlite3.connect('system.db')
            c = conn.cursor()

            # Get the details from the form
            username = request.form['username']
            password = request.form['password']

            # Check if the details are correct
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            data = c.fetchone()

            # If the details are correct, log the user in
            if data is not None:
                session['username'] = request.form['username']
                # Store the user ID in the session
                session['user_id'] = data[0]
                return redirect(url_for('home'))

            # Close the database
            conn.close()
        # except Exception as e:
        #     # Handle errors
        #     return render_template('error.html', message="An error occurred while accessing the database.")

    # If the details are incorrect, show the login page
    return render_template('login.html')

# Home page
@app.route('/home')
def home() -> str:
    if 'username' in session:
        if session['username'] == 'admin':
            return render_template('admin.html', username=session['username'])
        elif session['username'] == 'ecadmin':
            return render_template('ecadmin.html', username=session['username'])
        elif session['username'] == 'itladmin':
            return render_template('itladmin.html', username=session['username'])
        elif session['username'] == 'itsadmin':
            return render_template('itsadmin.html', username=session['username'])
        elif session['username'] == 'eeadmin':
            return render_template('eeadmin.html', username=session['username'])
        elif session['username'] == 'moduleorganiser':
            return render_template('moduleo.html', username=session['username'])
        else:
            return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# EC page
@app.route('/ec', methods=['GET', 'POST'])
def ec():
    if request.method == 'POST':
        # print("about to post")
        # Connect to the database
        conn = sqlite3.connect('system.db')
        # print("connected")
        c = conn.cursor()
        c.execute("INSERT INTO ecs (user_id, title, description, status) VALUES (?, ?, ?, ?)", ())
        data = c.fetchone()
        # Close the database
        conn.close()

    if 'username' in session:
        return render_template('ec.html', username = session['username'])
    return redirect(url_for('login'))

# Issues page
@app.route('/issues')
def issues():
    if 'username' in session:
        return render_template('issues.html', username = session['username'])
    return redirect(url_for('login'))

# Logout page
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()