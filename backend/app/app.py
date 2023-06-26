from flask import Flask, jsonify
from . import visualization

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config')

  register_blueprints(app)

  return app

# Blueprints
def register_blueprints(app: Flask):
  app.register_blueprint(visualization.routes.blueprint)
  





