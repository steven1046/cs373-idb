import fileinput, requests, json, psycopg2

# returns a dictionary with company (name, id) as keys and a list of game ids as values
def getCompanyGames(strFile, apiKey) :

	# company queries strings
	compString1 = "http://www.giantbomb.com/api/company/3010-" 
	compString2 = "/?api_key=" + apiKey + "&format=json"
	compFilter = "&field_list=name,developed_games,id"

	companyGames = {}

	f = fileinput.input(files=(strFile))

	for id in f :
		id = id.rstrip()
		response = requests.get(compString1 + id + compString2 + compFilter)
		v = json.loads(response.text)

		# success
		if v["status_code"] == 1 :
			gameIds = []
			companyPair = (v["results"]["name"], v["results"]["id"])
			for game in v["results"]["developed_games"] :
				gameIds += [game["id"]]

			companyGames[companyPair] = gameIds

	return companyGames


# returns a dictionary with game (name, id) as keys and dictionary of game info as values
def getGamesInfo(gamesDict, apiKey) :
	
	# game queries strings
	gameString1 = "http://www.giantbomb.com/api/game/3030-"
	gameString2 = "/?api_key=" + apiKey + "&format=json"
	# gameFilter = "&field_list=name,deck,description,image,images,original_release_date,genres,platforms,reviews"
	# ALWAYS INCLUDE GAMEID. Using as primary key
	gameFilter = "&field_list=name,deck,description,id,image,original_release_date,genres,platforms"
	games = {}
	gameData = []

	for company in gamesDict :
		for gameId in gamesDict[company] :
			response = requests.get(gameString1 + str(gameId) + gameString2 + gameFilter)
			v = json.loads(response.text)

			# success
			if v["status_code"] == 1 :
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
			if field == "image" :
				games[game][field] = games[game][field]["super_url"]
				print(str(type(games[game][field])) + field)
			# replace the platforms dict with platformsId
			elif field == "platforms" :
				platforms[game] = games[game][field]

				# populate platform list
				for platform in games[game][field] :
					platformList += [(game[1], platform["name"])]

				# field = "platformsId"
				games[game]["platforms"] = platformsId
				platformsId += 1
			# replace the genres dict with a genresId
			elif field == "genres" :
				genres[game] = games[game][field]

				# populate genre list
				for genre in games[game][field] :
					genreList += [(game[1], genre["name"])]

				# field = "genresId"
				games[game]["genres"] = genresId
				genresId += 1
			else :
				print(str(type(games[game][field])) + field)

		# populate gamesList. 
		# t = games[game]
		# g = [t["id"], t["name"], t["image"], t["original_release_date"], t["deck"], t["description"]]
		# gameList += [g]

		# Reduce size of game in dictionary??? Can't delete from dict while iterating so I will set to some small variable. Not sure if this is needed.
		# games[game] = {}


	return platformList, genreList, games

def insertGames(games, cursor) :
	for game in games :
		g = games[game]
		queryString = "insert into app.games (game_id, name, image, original_release_date, deck, description) values (" \
						"%s, %s, %s, %s, %s, %s)"
		cursor.execute(queryString, (g["id"], g["name"], g["image"], g["original_release_date"], g["deck"], g["description"]))
		for val in game :
			print(type(val))
		
		


def insertPlatforms(platformList, cursor) :
	for val in platformList :
		queryString = "insert into app.platforms (game_id, platform) values (%s, %s)"
		cursor.execute(queryString, (val[0], val[1]))

def insertGenres(genreList, cursor) :
	for val in genreList :
		queryString = "insert into app.genres (game_id, genre) values (%s, %s)"
		cursor.execute(queryString, (val[0], val[1]))


def main() :
	apiKey = "1d2e0eab2472ceddda3ec2428d5f8c3e52a68045"
	g = getCompanyGames("single_id.txt", apiKey)
	h = getGamesInfo(g, apiKey)

	conn_string = "host='localhost' dbname='postgres' user='dataUser' password='password!'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	
	
	platformList, genreList, gamesDict = normalize(h)

	# each return value from normalize will be its own table. 

	"""
		platformList has two columns, gameId and platform. gameId is fk to pk in games table.
		genreList has two columns, gameId and genre. gameId is fk to pk in games table.

	"""

	insertGames(gamesDict, cursor)
	# insertGenres(genreList, cursor)
	# insertPlatforms(platformList, cursor)
	# for game in gamesDict :
	# 	print(gamesDict[game].keys())

	cursor.execute("select image from app.games")
	print(cursor.fetchall())

	conn.commit()

	# print(h)
	# print(platformList)
	# print(genreList)
	# print(gamesDict)


if __name__ == "__main__":
	main()





