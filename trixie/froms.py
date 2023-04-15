from flask_login import UserMixin
from trixie import mongo

class User(UserMixin):
    def __init__(self, username):
        self.username = username
    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details

    def c_or_u(self):
        uorc = u = mongo.db.Users.find_one({"username": self.username}) or mongo.db.Company.find_one({"username": self.username})
        if "job_lists" in uorc:
            return "company"
        else:
            return "user"

    def get_id(self):
        return self.username