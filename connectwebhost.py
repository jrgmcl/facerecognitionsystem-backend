import MySQLdb

db = MySQLdb.connect("localhost",  # your host 
                     "phpmyadmin",       # username
                     "admin",     # password
                     "facerecog")   # name of the database

# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
cur.execute("SELECT * FROM rgstrd_users")
 
# print the first and second columns      
for row in cur.fetchall() :
    print (row[0], " ", row[1])