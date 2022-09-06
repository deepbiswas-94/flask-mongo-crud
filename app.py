from flask import Flask
from flask_mongoengine import MongoEngine
from routes import router
import sys

db = MongoEngine()
app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
app.register_blueprint(router)
sys.dont_write_bytecode = True

if __name__ == "__main__":
    app.run(debug=True)