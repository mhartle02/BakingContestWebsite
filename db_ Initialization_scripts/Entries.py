import sqlite3

conn = sqlite3.connect('../BakingContest.db', check_same_thread=False)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS ENTRIES
(Entry_Id INTEGER PRIMARY KEY NOT NULL,
User_Id INTEGER NOT NULL,
Item_Name TEXT NOT NULL,
Excellent_Votes INTEGER NOT NULL,
Ok_Votes INTEGER NOT NULL,
Bad_Votes INTEGER NOT NULL);

INSERT INTO ENTRIES (User_Id, Item_Name, Excellent_Votes, Ok_Votes, Bad_Votes)
VALUES (3, 'Pizza', 50, 20, 5);

INSERT INTO ENTRIES (User_Id, Item_Name, Excellent_Votes, Ok_Votes, Bad_Votes)
VALUES (3, 'Muffin', 30, 15, 10);

INSERT INTO ENTRIES (User_Id, Item_Name, Excellent_Votes, Ok_Votes, Bad_Votes)
VALUES (3, 'Carrot Cake', 40, 10, 2);
""")

conn.commit()
conn.close()
