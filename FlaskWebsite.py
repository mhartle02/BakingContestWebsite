import sqlite3
from flask import Flask, render_template, request

#create a new db
conn = sqlite3.connect('../BakingContest.db')

#create cursor to exectute queries
cur = conn.cursor()


#Create USER table
try:
    cur.execute("CREATE TABLE USER"
                "(User_Id Integer PRIMARY KEY NOT NULL,"
                "Name String NOT NULL,"
                " Age Integer NOT NULL,"
                " Phone_Number String NOT NULL,"
                " Security_Level String NOT NULL,"
                " Login_Password String NOT NULL);")

    print("User table created.")

except Exception as e:
    print(e)

#Create ENTRIES table
try:
    cur.execute("CREATE TABLE ENTRIES"
                "(Entry_Id Integer PRIMARY KEY NOT NULL,"
                "User_Id Integer NOT NULL,"
                "Item_Name String NOT NULL,"
                "Excellent_Votes Integer NOT NULL,"
                "Ok_Votes Integer NOT NULL,"
                "Bad_Votes Integer NOT NULL);")
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('HomePage.html')

@app.route('/enternew')
def enter_new():
    return render_template('EnterNew.html')

@app.route('/contestResults')
def contest_results():
    return render_template('ContestResults.html')

@app.route('/contestUsers')
def contest_users():
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM USER')
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

    conn = sqlite3.connect('../BakingContest.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO USER (Name, Age, Phone_Number, Security_Level, Login_Password) VALUES (? ,? ,?, ?, ?)', (name, age, phone_number, security_level, login_password))
    conn.commit()
    conn.close()

    return render_template('AddRec.html')

if __name__ == '__main__':
    app.run(debug=False)
    t = cur.execute("SELECT * FROM USER")
    for row in t:
        print(row)
