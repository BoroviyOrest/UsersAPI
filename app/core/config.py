import os

MONGO_DB = os.getenv('MONGO_DB', 'UsersAPI')

MONGODB_URL = os.getenv("MONGODB_URL")  # deploying without docker-compose
if MONGODB_URL is None:
    MONGO_HOST = os.getenv('MONGO_HOST', 'users_mongo')
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
    MONGO_USER = os.getenv('MONGO_USER', 'root')
    MONGO_PASS = os.getenv('MONGO_PASSWORD', 'password')

    MONGODB_URL = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}'

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

database_name = MONGO_DB
jwt_secret = 'Uj8YpWky8UtbogzJbSmrEU9S56gFzqNlKHUtQmRcAltRpSa6H3YFowdMH6zVmQt'
