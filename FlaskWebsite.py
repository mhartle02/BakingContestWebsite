import sqlite3
from functools import wraps
from flask_session import Session
from datetime import timedelta
from flask import Flask, render_template, request, session, redirect, url_for



app = Flask(__name__)
app.secret_key = 'key'  # Ensure this key is consistent
app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side session storage
app.config['SESSION_PERMANENT'] = False  # Allow sessions to persist
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Sessions last for 1 hour
Session(app)


conn = sqlite3.connect('../BakingContest.db', check_same_thread=False)
cur = conn.cursor()

cur.executescript("CREATE TABLE IF NOT EXISTS USER"
                "(User_Id INTEGER PRIMARY KEY NOT NULL,"
                "Name TEXT NOT NULL,"
                "Age INTEGER NOT NULL,"
                "Phone_Number TEXT NOT NULL,"
                "Security_Level TEXT NOT NULL,"
                "Login_Password TEXT NOT NULL);"
                "CREATE TABLE IF NOT EXISTS ENTRIES"
                "(Entry_Id INTEGER PRIMARY KEY NOT NULL,"
                "User_Id INTEGER NOT NULL,"
                "Item_Name TEXT NOT NULL,"
                "Excellent_Votes INTEGER NOT NULL,"
                "Ok_Votes INTEGER NOT NULL,"
                "Bad_Votes INTEGER NOT NULL);")


conn.commit()
conn.close()

@app.route('/')
def home_page():
    # Debugging session data
    print("Session Data:", session)

    # Retrieve session variables
    name = session.get('name', None)  # Use None as the default value for clarity
    security_level = session.get('Security_Level', 1)

    # Check if the name is None (i.e., not in the session)
    if not name:
        return redirect(url_for('login'))

    # Pass session data to the template
    return render_template('HomePage.html', name=name, Security_Level=security_level)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        # Validate user
        conn = sqlite3.connect('../BakingContest.db')
        cur = conn.cursor()
        user = cur.execute(
            "SELECT Name, Security_Level FROM USER WHERE Name = ? AND Login_Password = ?",
            (name, password)
        ).fetchone()
        conn.close()

        if user:
            session['name'], session['Security_Level'] = user
            session.permanent = False  # Ensure session persists
            return redirect(url_for('home_page'))
        else:
            return render_template('Login.html', error="Invalid credentials")
    return render_template('Login.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    print("Session cleared:", session)  # Debugging statement
    return redirect(url_for('login'))





@app.route('/enternew')
def enter_new():
    Security_Level = session.get('Security_Level', 1)
    if session.get('name') is None:
        return redirect(url_for('login'))
    session['page'] = "New User"
    return render_template('EnterNew.html', Security_Level = Security_Level)

@app.route('/enternewentry')
def enter_new_entry():
    session['page'] = "New Entry"
    return render_template('EnterNewEntry.html')


@app.route('/contestResults')
def contest_results():
    if session.get('name') is None:
        return redirect(url_for('login'))
    conn = sqlite3.connect('../BakingContest.db')
    cur = conn.cursor()
    name = session.get('name', 'Guest')  # Default to 'Guest' if not set
    security_level = session.get('Security_Level', 1)  # Default to 1 if not set
    cur.execute("SELECT Entry_Id, User_Id, Item_Name, Excellent_Votes, Ok_Votes, Bad_Votes FROM ENTRIES")
    results = cur.fetchall()
    conn.close()

    # Debugging: Print results to console to verify
    print("Contest Results: ", results)

    return render_template('ContestResults.html', results=results, Security_Level=security_level)

@app.route('/myContestResults')
def my_contest_results():
    if session.get('name') is None:
        return redirect(url_for('login'))
    conn = sqlite3.connect('../BakingContest.db')
    cur = conn.cursor()

    # Retrieve session variables
    name = session.get('name', 'Guest')
    security_level = session.get('Security_Level', 1)

    # Execute the query with the correct parameters
    cur.execute("""
        SELECT e.Entry_Id, e.Item_Name, e.Excellent_Votes, e.Ok_Votes, e.Bad_Votes
        FROM ENTRIES AS e
        JOIN USER AS u ON u.User_Id = e.User_Id
        WHERE u.Name = ?
    """, (name,))

    # Fetch all results from the query
    results = cur.fetchall()

    # Close the connection
    conn.close()

    # Return the results to the template
    return render_template('MyContestResults.html', results=results)


@app.route('/contestUsers')
def contest_users():
    if session.get('name') is None:
        return redirect(url_for('login'))
    conn = sqlite3.connect('../BakingContest.db')
    cur = conn.cursor()
    name = session.get('name', 'Guest')  # Default to 'Guest' if not set
    security_level = session.get('Security_Level', 1)  # Default to 1 if not set
    cur.execute('SELECT Name, Age, Phone_Number, Security_Level, Login_Password FROM USER')
    users = cur.fetchall()
    conn.close()
    return render_template('ContestUsers.html', users=users, Security_Level = security_level)


@app.route('/addrec', methods=['POST'])
def add_rec():
    if session.get('name') is None:
        return redirect(url_for('login'))
    error_message = []
    user = session.get('name')

    if session.get('page') == 'New User':

        name = request.form['Name']
        age = request.form['Age']
        phone_number = request.form['PhoneNumber']
        security_level = request.form['SecurityLevel']
        login_password = request.form['Password']
        error_message = []

        # Input validation
        if not name or name.isspace():
            error_message.append('You cannot enter an empty name.')
        if not age.isdigit() or not (0 < int(age) <= 120):
            error_message.append('Age must be a whole number greater than 0 and less than or equal to 120.')
        if not phone_number or phone_number.isspace():
            error_message.append('You cannot enter an empty phone number.')
        if not security_level or security_level.isspace():
            error_message.append('You cannot enter an empty security level.')
        if not login_password or login_password.isspace():
            error_message.append('You cannot enter an empty login password.')
        if not error_message:
            conn = sqlite3.connect('../BakingContest.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO USER (Name, Age, Phone_Number, Security_Level, Login_Password) VALUES (?, ?, ?, ?, ?)',
                        (name, age, phone_number, security_level, login_password))
            conn.commit()
            conn.close()
            error_message.append('Record successfully added.')
    else:
        name = request.form['Name']
        excellentVotes = request.form['ExcellentVotes']
        okVotes = request.form['OkVotes']
        badVotes = request.form['BadVotes']

        # Input validation
        if not name or name.isspace():
            error_message.append('You cannot enter an empty name.')
        if not excellentVotes.isdigit() or not (0 <= int(excellentVotes)):
            error_message.append('Excellent votes must be a whole number greater or equal to 0 .')
        if not okVotes.isdigit() or not (0 <= int(okVotes)):
            error_message.append('Ok votes must be a whole number greater or equal to 0 .')
        if not badVotes.isdigit() or not (0 <= int(badVotes)):
            error_message.append('Bad votes must be a whole number greater or equal to 0 .')
        if not error_message:
            conn = sqlite3.connect('../BakingContest.db')
            cur = conn.cursor()
            userid = cur.execute("SELECT User_Id FROM USER WHERE Name = ?", (user,)).fetchone()
            cur.execute(
                'INSERT INTO ENTRIES (User_Id, Item_Name, Excellent_Votes, Ok_Votes, Bad_Votes) VALUES (?, ?, ?, ?, ?)',
                (userid[0], name, excellentVotes, okVotes, badVotes))
            conn.commit()
            conn.close()
            error_message.append('Record successfully added.')

    for error in error_message:
        print(error)

    return render_template('AddRec.html', errors=error_message)


if __name__ == '__main__':
    app.run(debug=True)