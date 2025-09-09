from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, email='N/A', default_base_currency=1, is_admin=False, created_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.default_base_currency = default_base_currency
        self.is_admin = is_admin
        self.created_at = created_at