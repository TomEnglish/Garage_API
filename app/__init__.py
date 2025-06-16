from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.customers import customers_db
from .blueprints.mechanics import mechanics_db
from .blueprints.service_tickets import tickets_db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')


    #initialize extensions 
    ma.init_app(app) 
    db.init_app(app)




    #register blueprint
    app.register_blueprint(customers_db, url_prefix='/customers')
    app.register_blueprint(mechanics_db, url_prefix='/mechanics')
    app.register_blueprint(tickets_db, url_prefix='/tickets')




    return app

