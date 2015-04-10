import fileinput, requests, json, psycopg2, indeed

client = indeed.IndeedClient('1942078712727036')


def insert_jobs(jobs, cur):
	queryString = "insert into jobs(job_id, job_title, url, description, location, company_name, company_id)" \
					"values (%s, %s, %s, %s, %s, %s, %s)"

	cur.execute(queryString,(jobs["job_id"], jobs["job_title"], jobs["url"], jobs["description"], jobs["location"], jobs["company_name"], jobs["company_id"]))


def main():

	conn_string = "host='localhost' dbname='banana-fish' user='dataUser' password='password!'"
	conn = psycopg2.connect(conn_string)
	cur = conn.cursor()
	cur.execute("""SELECT company_id, name from companies""")
	rows = cur.fetchall()

	jobs = {}
	i = 1

	for row in rows:
		print(" %d:", i)
		i += 1
		job = {}
		company_id = int(row[0])
		company_name = row[1]

		params = {
			'q' : company_name,
			'userip': '23.253.89.46',
			'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
			'format' : "json"
		}

		search_response = client.search(**params)

		job_id = 1

		for item in search_response['results']:
			if( company_name in item['company'] or item['company'] in company_name): 
				d = {}
				d['job_id'] = item['jobkey']
				job_id = item['jobkey']
				d['job_title'] = item['jobtitle']
				d['url'] = item['url']
				d['description'] = item['snippet']
				d['location'] = item['formattedLocationFull']
				d['company_name'] = item['company']
				d['company_id'] = company_id
				jobs[job_id] = d

		# jobs[job_id] = d
	
	for key in jobs:
		insert_jobs(jobs[key], cur)
	conn.commit()

if __name__ == "__main__":
	main()