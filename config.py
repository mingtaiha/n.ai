import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'nai'

SQLALCHEMY_DATABASE_URI = 'mysql://nai:nai@localhost/nai'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

GOOGLE_MAPS_API_KEY = "AIzaSyC7gFkRVm3oUKLC3ZTNmuSAxSnXxXhGh0M"
GOOGLE_PLACES_API_KEY = "AIzaSyCQENSbRFfd9_lGuqoXf2icRgtSvED-WHI"
