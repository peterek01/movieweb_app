import os
import requests
from sqlalchemy.exc import OperationalError, IntegrityError
from .data_manager_interface import DataManagerInterface
from .models import User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        self.db = db  # Now we use the passed db instance

    def get_all_users(self):
        try:
            return User.query.all()
        # there is a risk of connection interruption or database problem
        except OperationalError as e:
            print("Database operation failed:", e)
            return []

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_movie(self, movie_id):
        return Movie.query.get(movie_id)

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def get_user_movie_by_name(self, user_id, movie_name):
        return Movie.query.filter_by(user_id=user_id, name=movie_name).first()

    def add_movie(self, user_id, movie_details):
        # Remove 'user_id' from movie_details if it exists
        if 'user_id' in movie_details:
            del movie_details['user_id']

        try:
            # Create new movie object
            new_movie = Movie(user_id=user_id, **movie_details)
            self.db.session.add(new_movie)
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            print("Integrity error occurred:", e)
            raise ValueError("Movie already exists in the database.")
        except Exception as e:
            self.db.session.rollback()
            print("An error occurred while adding the movie:", e)
            raise ValueError("Error adding movie to the database.")

    def update_movie(self, movie_id, movie_details):
        # Download movie from database
        movie = Movie.query.get(movie_id)
        if not movie:
            raise ValueError(f"Movie with ID {movie_id} not found.")

        # Update movie fields
        for key, value in movie_details.items():
            # Check if the input data is of the correct type
            if key == "year" and not isinstance(value, int):
                raise TypeError(f"The value for 'year' must be an integer, got {type(value).__name__}.")
            if key == "rating" and not isinstance(value, (int, float)):
                raise TypeError(f"The value for 'rating' must be a number, got {type(value).__name__}.")

            setattr(movie, key, value)

        self.db.session.commit()

    def delete_movie(self, movie_id):
        try:
            # Download movie from database
            movie = Movie.query.get(movie_id)
            if not movie:
                raise ValueError(f"Movie with ID {movie_id} not found.")

            self.db.session.delete(movie)
            self.db.session.commit()
            print(f"Movie with ID {movie_id} has been deleted.")

        except ValueError as e:
            print(f"ValueError: {e}")
            raise e  # Optional: We can return HTTP 400 response in Flask

    def add_user(self, user_details):
        try:
            if not user_details.get('name', '').strip():
                raise ValueError("User name cannot be empty.")

            avatar = user_details.get('avatar', '1')
            new_user = User(name=user_details['name'], avatar=avatar)

            # Create a new user and add it to the database
            self.db.session.add(new_user)
            self.db.session.commit()

        except KeyError as e:
            # Handle missing key in dictionary
            print(f"KeyError: Missing key in user details: {e}")
            raise ValueError(f"User details must include the field '{e.args[0]}'.")

        except IntegrityError as e:
            # Handle data integrity violations (e.g. duplicates)
            self.db.session.rollback()  # Undo failed changes
            print("IntegrityError: Duplicate entry or missing required field:", e)
            raise ValueError("A user with this name already exists.")

    def update_user(self, user_id, user_details):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in user_details.items():
            if key == "name" and not isinstance(value, str):
                raise TypeError(f"Invalid type for 'name': {type(value).__name__}. Expected str.")
            setattr(user, key, value)

        self.db.session.commit()

    def delete_user(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")

            self.db.session.delete(user)
            self.db.session.commit()
        except Exception as e:
            # Undo operation in case of error
            self.db.session.rollback()
            print(f"Error deleting user: {e}")
            raise ValueError(f"Error deleting user: {str(e)}")

    def fetch_movie_details_from_omdb(self, movie_name):
        api_key = "2e8cb9fe"
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                # Year range support
                year = data.get("Year")
                if year and '–' in year:
                    year = year.split('–')[0].strip()  # Select the first year from the range
                try:
                    year = int(year) if year else None
                except ValueError:
                    year = None  # If conversion fails, set to None

                return {
                    "name": data.get("Title"),
                    "director": data.get("Director"),
                    "year": year,
                    "rating": float(data.get("imdbRating")) if data.get("imdbRating") else None,
                    "poster_url": data.get("Poster") if data.get("Poster") != "N/A" else None,
                }
        return None

    def initialize_database(self):
        db_path = 'data/movies.db'
        # For file operations such as opening or checking the existence of a file
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file {db_path} not found.")