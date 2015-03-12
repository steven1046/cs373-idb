import fileinput, requests, json

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
		# print(id)
		# print(compString1 + id + compString2 + compFilter)
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
	gameFilter = "&field_list=name,deck,description,image,original_release_date,genres,platforms"
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
	genres = {}
	platformsId = 0
	genresId = 0

	# normalizing
	for game in h :
		for field in h[game] :
			# replacing image dict with string for super_url image
			if field == "image" :
				h[game][field] = h[game][field]["super_url"]
			# replace the platforms dict with platformsId
			elif field == "platforms" :
				platforms[game] = h[game][field]
				del h[game][field]
				field = "platformsId"
				h[game]["platformsId"] = platformsId
				platformsId += 1
			# replace the genres dict with a genresId
			elif field == "genres" :
				genres[game] = h[game][field]
				del h[game][field]
				field = "genresId"
				h[game]["genresId"] = genresId
				genresId += 1


			print(str(type(h[game][field])) + field)
		print()


def main() :
	apiKey = "1d2e0eab2472ceddda3ec2428d5f8c3e52a68045"
	g = getCompanyGames("single_id.txt", apiKey)
	h = getGamesInfo(g, apiKey)
	
	# need to pull out platforms and genres list and put into new dicts

	platforms = {}
	genres = {}
	platformsId = 0
	genresId = 0

	# normalizing
	for game in h :
		for field in h[game] :
			# replacing image dict with string for super_url image
			if field == "image" :
				h[game][field] = h[game][field]["super_url"]
			# replace the platforms dict with platformsId
			elif field == "platforms" :
				platforms[game] = h[game][field]
				del h[game][field]
				field = "platformsId"
				h[game]["platformsId"] = platformsId
				platformsId += 1
			# replace the genres dict with a genresId
			elif field == "genres" :
				genres[game] = h[game][field]
				del h[game][field]
				field = "genresId"
				h[game]["genresId"] = genresId
				genresId += 1


			print(str(type(h[game][field])) + field)
		print()

	print(h)
	print(platforms)
	print(genres)



main()

# f = fileinput.input(files=("single_id.txt"))
# #f = fileinput.input(files=("company_ids.txt"))

# apiKey = "1d2e0eab2472ceddda3ec2428d5f8c3e52a68045"

# companyIds = []

# for id in f :
# 	companyIds += [id.rstrip()]

# # for the filter strings see http://www.giantbomb.com/api/documentation for options


# # company queries
# compString1 = "http://www.giantbomb.com/api/company/3010-" 
# compString2 = "/?api_key=" + apiKey + "&format=json"
# compFilter = "&field_list=name,developed_games"

# for id in companyIds :
# 	print(compString1 + id + compString2 + compFilter)
# 	response = requests.get(compString1 + id + compString2 + compFilter)
# 	v = json.loads(response.text)

# 	print("Company name: " + v["results"]["name"])
# 	print("Games:")

# 	# game queries
# 	gameString1 = "http://www.giantbomb.com/api/game/3030-"
# 	gameString2 = "/?api_key=" + apiKey + "&format=json"
# 	gameFilter = "&field_list=name,deck,description,image,images,original_release_date,genres,platforms,reviews"
# 	for game in v["results"]["developed_games"] :
# 		response = requests.get(gameString1 + str(game["id"]) + gameString2 + gameFilter)
# 		v = json.loads(response.text)
# 		# print(v["results"]["platforms"])
# 		# print(v["results"]["name"])
# 		# for plat in v["results"]["platforms"] :
# 		# 	print(plat["name"])
# 		# if "reviews" in v["results"] :
# 		# 	for rev in v["results"]["reviews"] :
# 		# 		print(rev[""])
# 		print(v)
# 		# print(gameString1 + str(game["id"]) + gameString2 + gameFilter)
# 		print()
	
# 	print()





