from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    username = db.Column(db.String(50), unique=True, nullable=False) 
    password = db.Column(db.String(256), unique=True, nullable=False) 

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        print("This is hashed password:",self.password)
        return check_password_hash(self.password, password)