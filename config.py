class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False