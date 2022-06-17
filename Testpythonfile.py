import os
import MySQLdb
import datetime

db = MySQLdb.connect("localhost",   #Host 
                     "root",  #Username
                     "frpi",       #Password
                     "fr")   #Database
cur = db.cursor()

name = "0"

cur.execute("SELECT * FROM `fr_registered-users` WHERE `id` = " + str(name) + ";")
row = cur.fetchone()

print(str(row[3]))