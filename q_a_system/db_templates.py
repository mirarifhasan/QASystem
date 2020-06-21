#!/usr/bin/python3

import pymysql

# Open database connection
db = pymysql.connect("localhost","Thesis","Thesis123", "QASYSTEM" )
# prepare a cursor object using cursor() method
cursor = db.cursor()


# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS TEMPLATES")
'''
# Create table as per requirement
sql = """CREATE TABLE TEMPLATES (
   ID int NOT NULL PRIMARY KEY,
   A  CHAR(255), B  CHAR(255), C  CHAR(255), D  CHAR(255), E  CHAR(255),
   F  CHAR(255), G  CHAR(255), H  CHAR(255), I  CHAR(255), J  CHAR(255)
)"""

cursor.execute(sql)



# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO TEMPLATES(ID,A,B,C,D,E,F,G,H)
   VALUES (1,'SELECT COUNT(DISTINCT ?uri) WHERE{ ?uri res:', 'dbo:','}','','','','','','','')"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

'''


# disconnect from server
db.close()