config = {
    "DATABASE_ADAPTER": "postgresql",
    "DATABASE_NAME": "banana-fish",
    "DATABASE_HOST": "localhost",
    "DATABASE_PORT": "5432",
    "API_VER": "v1",
    "DEBUG": True,
    "HOST": "0.0.0.0",
    "PORT": 80
}


config["ROUTE_PREFIX"] = "/api/" + config["API_VER"] + "/"
config['SQLALCHEMY_DATABASE_URI'] = "%s://%s:%s/%s" % (config["DATABASE_ADAPTER"], config["DATABASE_HOST"],
                                    config["DATABASE_PORT"], config["DATABASE_NAME"])


test_config = {
    "DATABASE_ADAPTER": "sqlite",
    "DATABASE": "test.db",
    "DATABASE_HOST": "",
    "DATABASE_NAME": "test.db",
    "SECRET_KEY": "dev key",
    "USERNAME": "admin",
    "PASSWORD": "password",
    "API_VER": "v1",
    "DEBUG": True
}


test_config["ROUTE_PREFIX"] = "/api/" + test_config["API_VER"] + "/"
test_config['SQLALCHEMY_DATABASE_URI'] = "%s://%s/%s" % (test_config["DATABASE_ADAPTER"], test_config["DATABASE_HOST"],
                                                         test_config["DATABASE_NAME"])


