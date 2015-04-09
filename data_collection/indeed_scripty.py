import fileinput, requests, json, psycopg2, indeed

client = IndeedClient('1942078712727036')



def main():

	conn_string = "host='localhost' dbname='banana-fish' user='dataUser' password='password!'"
	conn = psycopg2.connect(conn_string)
	cur = conn.cursor()
	cur.execute("""SELECT * from Companies""")
	rows = cur.fetchall()

	print "\nShow me the databases:\n"
	for row in rows:
		print ("   ", row[0])