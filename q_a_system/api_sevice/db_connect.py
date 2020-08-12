import pymysql

# Open database connection
hostname = "myclouddb.c4hfxbeu2kdo.ap-southeast-1.rds.amazonaws.com"
user = "admincoder"
password = "adm!nadm!n"
databaseName = "qasystemdb"
connection = pymysql.connect(hostname, user, password, databaseName)
# connection = pymysql.connect("localhost","root","", "qasystem")

# prepare a cursor object using cursor() method
cursor = connection.cursor()

# disconnect from server
# connection.close()