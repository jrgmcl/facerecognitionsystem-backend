import os
import MySQLdb

db = MySQLdb.connect("localhost",   #Host 
                     "root",  #Username
                     "frpi",       #Password
                     "fr")   #Database
cur = db.cursor()

cur.execute("SELECT * FROM `qr_pending-users`")
cur.fetchall()
count = cur.rowcount
print (count)
