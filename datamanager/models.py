from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(15), nullable=False, default='1')

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    poster_url = db.Column(db.String(300), nullable=True)

    # representation method for better debugging
    def __repr__(self):
        return f"<Movie(id={self.id}, name={self.name}, user_id={self.user_id})>"
