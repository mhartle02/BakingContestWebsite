import sqlite3
from optparse import Values

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'key'

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
    name = session.get('name', 'Guest')  # Default to 'Guest' if not set
    security_level = session.get('Security_Level', 1)  # Default to 1 if not set
    return render_template('HomePage.html', name=name, Security_Level=security_level)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        # Validate the user input
        if not name or not password:
            error_message = "Please provide both username and password!"
        else:
            try:
                # Connect to the database
                conn = sqlite3.connect('../BakingContest.db')
                cur = conn.cursor()

                # Query the database
                user = cur.execute(
                    "SELECT Name, Security_Level FROM USER WHERE Name = ? AND Login_Password = ?",
                    (name, password)
                ).fetchone()

                if user:  # If a matching user is found
                    name, security_level = user
                    session['name'] = name
                    session['Security_Level'] = security_level
                    return render_template(
                        'HomePage.html', name=name, Security_Level=security_level
                    )
                else:
                    error_message = "Invalid username and/or password!"
            except Exception as e:
                # Log the error for debugging
                print(f"Database error: {e}")
                error_message = "An unexpected error occurred. Please try again later."
            finally:
                conn.close()  # Ensure the connection is always closed

    # Render the login page with an error message (if any)
    return render_template('Login.html', error=error_message)



@app.route('/enternew')
def enter_new():
    return render_template('EnterNew.html')


@app.route('/contestResults')
def contest_results():
    conn = sqlite3.connect('../BakingContest.db')
    cur = conn.cursor()
    name = session.get('name', 'Guest')  # Default to 'Guest' if not set
    security_level = session.get('Security_Level', 1)  # Default to 1 if not set
    cur.execute("SELECT Entry_Id, User_Id, Item_Name, Excellent_Votes, Ok_Votes, Bad_Votes FROM ENTRIES")
    results = cur.fetchall()
    conn.close()

    # Debugging: Print results to console to verify
    print("Contest Results: ", results)

    return render_template('ContestResults.html', results=results)

@app.route('/myContestResults')
def my_contest_results():
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
    conn = sqlite3.connect('../BakingContest.db')
    cur = conn.cursor()
    name = session.get('name', 'Guest')  # Default to 'Guest' if not set
    security_level = session.get('Security_Level', 1)  # Default to 1 if not set
    cur.execute('SELECT Name, Age, Phone_Number, Security_Level, Login_Password FROM USER')
    users = cur.fetchall()
    conn.close()
    return render_template('ContestUsers.html', users=users)


@app.route('/addrec', methods=['POST'])
def add_rec():
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

    for error in error_message:
        print(error)

    return render_template('AddRec.html', errors=error_message)


if __name__ == '__main__':
    app.run(debug=True)
