import sqlite3

conn = sqlite3.connect('../BakingContest.db', check_same_thread=False)
cur = conn.cursor()

cur.executescript("CREATE TABLE IF NOT EXISTS USER"
                "(User_Id INTEGER PRIMARY KEY NOT NULL,"
                "Name TEXT NOT NULL,"
                "Age INTEGER NOT NULL,"
                "Phone_Number TEXT NOT NULL,"
                "Security_Level TEXT NOT NULL,"
                "Login_Password TEXT NOT NULL);"
                "INSERT INTO USER (User_Id, Name, Age, Phone_Number, Security_Level, Login_Password)"
                "VALUES"
                "(1, 'Alice', 28, '123-456-7890', '3', 'password123'),"
                "(2, 'Bob', 35, '987-654-3210', '2', 'securePass!'),"
                "(3, 'Charlie', 22, '555-123-4567', '1', 'charlie2024');")



conn.commit()
conn.close()


