import sqlite3

conn = sqlite3.connect('../BakingContest.db')
cur = conn.cursor()

cur.execute("INSERT INTO ENTRIES(User_Id, Item_Name, Excellent_Votes, Ok_Votes, Bad_Votes)"
                  "VALUES (2, 'Chicken Bakes', 4, 5, 0),"
                  " (3, 'Double Chocolate Chunk Cookies', 4, 3,2)")

conn.commit()
conn.close()