from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['SECRET_KEY'] = '5e4f9bc49725dcd58b5f6510cbfef6c0'
#client = pymongo.MongoClient('mongodb://localhost:27017')
#db = client.Trixie
#coll = db.Users

app.config["MONGO_URI"] = "mongodb://localhost:27017/Trixie"
db = PyMongo(app)

from trixie import routes

