import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False)
    followers = db.Column(db.Integer, default=0)
    followings = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User {self.name}>"
