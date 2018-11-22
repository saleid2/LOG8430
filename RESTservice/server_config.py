_CONFIG_MONGO_SCHEMA = "mongodb://"              # e.g. "mongodb://"

_CONFIG_MONGO_URL = "127.0.0.1"                  # e.g. "ds1234567.mlab.com" or "127.0.0.1"
_CONFIG_MONGO_PORT = "27017"                     # e.g. "15154"

_CONFIG_MONGO_DBNAME = "log8430"                 # e.g. "log8430"
_CONFIG_MONGO_COLLECTION = "receipts"            # e.g. "receipts"

_CONFIG_MONGO_USERNAME = ""                      # Database username. If none, leave empty
_CONFIG_MONGO_PASSWORD = ""                      # Database password. If none, leave empty


'''

DO NOT EDIT BELOW THIS LINE

'''


def _format_user_pass():
    if len(_CONFIG_MONGO_USERNAME) == 0:
        return ""
    else:
        return _CONFIG_MONGO_USERNAME + ":" + _CONFIG_MONGO_PASSWORD + "@"


def get_mongo_url():
    return _CONFIG_MONGO_SCHEMA + _format_user_pass() + _CONFIG_MONGO_URL + ":" + _CONFIG_MONGO_PORT


# TODO: Test to see if port is missing
def get_mongo_spark_url():
    # If port is needed use this instead
    # return get_mongo_url() +  "/" + CONFIG_MONGO_DBNAME + "." + CONFIG_MONGO_COLLECTION
    return _CONFIG_MONGO_SCHEMA + _format_user_pass() + _CONFIG_MONGO_URL + "/" + _CONFIG_MONGO_DBNAME + "." + _CONFIG_MONGO_COLLECTION
