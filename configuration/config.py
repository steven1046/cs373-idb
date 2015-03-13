config = {
    "DATABASE_ADAPTER": "postgresql",
    "DATABASE_NAME": "banana-fish",
    "DATABASE_HOST": "localhost",
    "DATABASE_PORT": "5432",
    "API_VER": "v1",
    "DEBUG": True,
    "SERVER_NAME": "banana-fish"
}


config["ROUTE_PREFIX"] = "/api/" + config["API_VER"] + "/"
config['SQLALCHEMY_DATABASE_URI'] = "%s://%s:%s/%s" % (config["DATABASE_ADAPTER"], config["DATABASE_HOST"],
                                    config["DATABASE_PORT"], config["DATABASE_NAME"])
