# from flask_pymongo import pymongo
# from flask_login import UserMixin

# con_string = 'mongodb+srv://umar:umar@cluster0.6qawpcu.mongodb.net/?retryWrites=true&w=majority'
# client = pymongo.MongoClient(con_string)
# db = client.get_database('testdb')
# items = pymongo.collection.Collection(db,'items')
# users = pymongo.collection.Collection(db,'users')
# userr=users.find({'name1':'umar'},{'password_hash':1})
# import json
# from bson import json_util


# class User(UserMixin):
#     def __init__(self, username, email, password, _id):
#         self.username = username
#         self.email = email
#         self.password = password
#         self._id = str(_id)
#         print(self._id)
#     #
#     # def is_authenticated(self):
#     #     return True
#     # def is_active(self):
#     #     return True
#     # def is_anonymous(self):
#     #     return False
#     def get_id(self):
#         return self._id

#     def parse_json(data):
#         return json.loads(json_util.dumps(data))

#     @classmethod
#     def get_by_id(cls, _id):
#         data = users.find_one( {"_id": _id})
#         if data is not None:
#             return cls(**data)
