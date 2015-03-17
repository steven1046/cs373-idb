import fileinput, requests, json, psycopg2


# (Change to return list?? Only need to iterate through this.)
def get_company_games(companyList, apiKey) :

	companyGames = {}
	for company in companyList :
		t = (company["results"]["name"], company["results"]["id"])
		gameList = []

		for game in company["results"]["developed_games"] :
			gameList += [game["id"]]
		
		# make sure list is in descending order
		gameList.sort(reverse = True)
		companyGames[t] = gameList
	return companyGames




def load_company_ids(strFile, apiKey) :
	f = fileinput.input(files=(strFile))
	ids = []
	for id in f :
		ids += [id.rstrip()]

	return ids

def get_company_info(companyIds, apiKey) :

	# company queries strings
	compString1 = "http://www.giantbomb.com/api/company/3010-" 
	compString2 = "/?api_key=" + apiKey + "&format=json"
	compFilter = "&field_list=name,developed_games,id,deck,description,image,location_address,location_city,location_country,location_state,phone,website,date_founded"


	companyList = []
	for id in companyIds :
		print(compString1 + id + compString2 + compFilter)
		response = requests.get(compString1 + id + compString2 + compFilter)
		v = json.loads(response.text)

		if v["status_code"] == 1 :
			companyList += [v]

			# change image to super_url
			v["results"]["image"] = v["results"]["image"]["super_url"]

	return companyList


# returns a dictionary with game (name, id) as keys and dictionary of game info as values. (Change to return list?? Only need to iterate through this.)
def get_games_info(gamesDict, apiKey, game_limit_company = 50) :
	
	# game queries strings
	gameString1 = "http://www.giantbomb.com/api/game/3030-"
	gameString2 = "/?api_key=" + apiKey + "&format=json"
	# gameFilter = "&field_list=name,deck,description,image,images,original_release_date,genres,platforms,reviews"
	# ALWAYS INCLUDE GAMEID. Using as primary key
	gameFilter = "&field_list=name,deck,description,id,image,original_release_date,genres,platforms"
	games = {}
	gameData = []

	for company in gamesDict :
		# limit the number of games per company
		gamesDict[company] = gamesDict[company][:game_limit_company]
		for gameId in gamesDict[company] :
			response = requests.get(gameString1 + str(gameId) + gameString2 + gameFilter)
			v = json.loads(response.text)

			# success
			if v["status_code"] == 1 :
				v["results"]["company_id"] = company[1]
				games[(v["results"]["name"], gameId)] = v["results"]


	return games

def normalize(games) :
	# need to pull out platforms and genres list and put into new dicts

	platforms = {}
	# contains tuples of (gameId, platform)    (giantbomb gameId used)
	platformList = []
	genres = {}
	# contains tuples of (gameId, genre)    (giantbomb game id used)
	genreList = []
	# contains tuples of game information
	gameList = []
	platformsId = 0
	genresId = 0

	# normalizing
	for game in games :
		for field in games[game] :
			# replacing image dict with string for super_url image
			if field == "image" and games[game]["image"] != None :
				games[game][field] = games[game][field]["super_url"]
	
				print(str(type(games[game][field])) + field)
			# replace the platforms dict with platformsId
			elif field == "platforms" and games[game]["platforms"] != None :
				platforms[game] = games[game][field]

				# populate platform list
				for platform in games[game][field] :
					platformList += [(game[1], platform["name"], platform["id"])]

				# field = "platformsId"
				games[game]["platforms"] = platformsId
				platformsId += 1
			# replace the genres dict with a genresId
			elif field == "genres" :
				genres[game] = games[game][field]

				# populate genre list
				for genre in games[game][field] :
					genreList += [(game[1], genre["name"], genre["id"])]

				# field = "genresId"
				games[game]["genres"] = genresId
				genresId += 1
			else :
				print(str(type(games[game][field])) + field)

	return platformList, genreList, games


		# name,developed_games,id,deck,description,image,location_address,location_city,location_country,location_state,phone,website,date_founded"
def insert_companies(companyList, cursor) :
	queryString = "insert into app.companies (company_id, name, deck, description, image, address, city, state, country, phone, date_founded, website)" \
						" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	for company in companyList :
		print(company["results"]["date_founded"])
		c = company["results"]
		print(c["image"])
		cursor.execute(queryString, (c["id"], c["name"], c["deck"], c["description"], c["image"], c["location_address"], c["location_city"], c["location_state"], c["location_country"], c["phone"], c["date_founded"], c["website"]))
		for v in c :
			print(type(v))


def insert_games(games, cursor) :
	queryString = "insert into app.games (game_id, name, image, original_release_date, deck, description, company_id) values (" \
						"%s, %s, %s, %s, %s, %s, %s)"
	for game in games :
		g = games[game]
		cursor.execute(queryString, (g["id"], g["name"], g["image"], g["original_release_date"], g["deck"], g["description"], g["company_id"]))
		for val in game :
			print(type(val))
		
		


def insert_game_platforms(platformList, cursor) :
	queryString = "insert into app.game_platforms (game_id, platform_id) values (%s, %s)"
	for val in platformList :
		cursor.execute(queryString, (val[0], val[2]))

def insert_game_genres(genreList, cursor) :
	queryString = "insert into app.game_genres (game_id, genre_id) values (%s, %s)"
	for val in genreList :
		cursor.execute(queryString, (val[0], val[2]))

def insert_genres(genre_list, cursor) :
	genre_ids = {(x[1], x[2]) for x in genre_list}
	query_string = "insert into app.genres (genre_id, genre) values (%s, %s)"
	for val in genre_ids :
		cursor.execute(query_string, (val[1], val[0]))
	print(genre_ids)

def insert_platforms(platform_list, cursor) :
	platform_ids = {(x[1], x[2]) for x in platform_list}
	query_string = "insert into app.platforms (platform_id, platform) values (%s, %s)"
	for val in platform_ids :
		cursor.execute(query_string, (val[1], val[0]))
	print(platform_ids)


def main() :

	apiKey = "1d2e0eab2472ceddda3ec2428d5f8c3e52a68045"
	conn_string = "host='localhost' dbname='postgres' user='dataUser' password='password!'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	ids = load_company_ids("multiple_ids.txt", apiKey)


	# returns a list. Elements are dictionaries of company info
	a = get_company_info(ids, apiKey)

	# returns a dictionary. Keys are company name, id tuples and values are list of game ids
	g = get_company_games(a, apiKey)

	# returns dictionary. Keys are game name and id tuples. values are dictionary of game info.
	h = get_games_info(g, apiKey, game_limit_company = 5)
	# print(h)

	platformList, genreList, gamesDict = normalize(h)
	print(genreList)
	print(platformList)

	insert_companies(a, cursor)
	insert_games(gamesDict, cursor)
	insert_genres(genreList, cursor)
	insert_platforms(platformList, cursor)
	insert_game_genres(genreList, cursor)
	insert_game_platforms(platformList, cursor)

	conn.commit()

if __name__ == "__main__":
	main()





