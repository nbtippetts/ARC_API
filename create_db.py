import mysql.connector

mydb = mysql.connector.connect(
	host='localhost',
	user='root',
	passwd='@Wicked2009'
)

my_cur = mydb.cursor()
my_cur.execute("CREATE DATABASE arc_db")
my_cur.execute("SHOW DATABASE")
for db in my_cur:
	print(db)
