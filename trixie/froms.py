import codecs
from flask_login import UserMixin
from trixie import mongo, grid_fs

class User(UserMixin):
    def __init__(self, username):
        self.username = username
    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details

    def c_or_u(self):
        uorc = mongo.db.Users.find_one({"username": self.username}) or mongo.db.Company.find_one({"username": self.username})
        if "job_lists" in uorc:
            return "company"
        else:
            return "user"
    
    def profile_pic(self):
        uorc = mongo.db.Users.find_one({"username": self.username}) or mongo.db.Company.find_one({"username": self.username})
        image = grid_fs.get(uorc['profile_id'])
        base64_data = codecs.encode(image.read(), 'base64')
        image = base64_data.decode('utf-8')
        return image

    def get_id(self):
        return self.username