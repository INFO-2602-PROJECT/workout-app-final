from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    sex = db.Column(db.String(50), nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    height = db.Column(db.Double, nullable=True)
    weight = db.Column(db.Double, nullable=True)
    gym_experience = db.Column(db.String(120), nullable=True)
    profile_picture_url = db.Column(db.String(255), nullable=True)
    videos = db.relationship('Video', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, password, sex=None, first_name=None, last_name=None, email=None, height=None, weight=None, gym_experience=None, profile_picture_url=None):
      self.username = username
      self.set_password(password)
      self.sex = sex
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.height = height
      self.weight = weight
      self.gym_experience = gym_experience
      self.profile_picture_url = profile_picture_url

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120))
    image = db.Column(db.String(120))
    description = db.Column(db.String(120))
    url = db.Column(db.String(120))

    def __init__(self, title, image, description, url, user_id):
        self.title = title
        self.image = image
        self.description = description
        self.url = url
        self.user_id = user_id





