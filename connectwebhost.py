import MySQLdb

db = MySQLdb.connect("localhost",  # your host 
                     "root",       # username
                     "",     # password
                     "fr")   # name of the database

# Create a Cursor object to execute queries.
cur = db.cursor()
id = 1
# Select data from table using SQL query.
cur.execute("SELECT * FROM rgstrd_users WHERE id = " + str(id) + ";")
 
# print the first and second columns      
row = cur.fetchone()
print (row[0], row[1], row[2], row[3], row[4], row[5])

#for row in cur.fetchall() :
    #print (row[0], " ", row[1])