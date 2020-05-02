database_name = "deliverme"
database_path = "postgres://{}@{}/{}".format('postgres', 'localhost:5432', database_name)
AUTH0_DOMAIN = 'andalussoft.au.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'deliver_me_api'