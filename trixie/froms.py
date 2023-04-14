from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username):
        self.username = username
    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details

    def get_id(self):
        return self.username