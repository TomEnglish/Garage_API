

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:MYPASSWORD123@localhost/garage_db'
    DEBUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass