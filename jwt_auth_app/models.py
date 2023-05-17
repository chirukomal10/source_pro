from database import db
import hashlib

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    permissions = db.Column(db.String(120), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
    
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        # Hash the password using SHA256 algorithm
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.password_hash = hashed_password

    def check_password(self, password):
        # Hash the provided password and compare it with the stored hashed password
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return self.password_hash == hashed_password
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'permissions': self.permissions
        }
