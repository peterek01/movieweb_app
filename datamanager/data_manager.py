import os
import requests
from requests import JSONDecodeError
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

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, movie_details):
        if not movie_details.get("name"):
            raise ValueError("Movie name is required.")

        # if 'user_id' in movie_details:
        #     del movie_details['user_id']

        try:
            new_movie = Movie(user_id=user_id, **movie_details)
            self.db.session.add(new_movie)
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            print("Integrity error occurred:", e)
            raise ValueError("A movie with this name already exists.")

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
            # Check if the required key 'name' exists in the dictionary
            new_user = User(name=user_details['name'])

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
        user = User.query.get(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
        else:
            raise ValueError("User not found")

    def fetch_movie_details_from_omdb(self, movie_name):
        api_key = "2e8cb9fe"
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("Response") == "True":
                    return {
                        "name": data.get("Title"),
                        "director": data.get("Director"),
                        "year": int(data.get("Year")) if data.get("Year") else None,
                        "rating": float(data.get("imdbRating")) if data.get("imdbRating") else None,
                    }
                else:
                    return None
            except JSONDecodeError as e:
                # When working with API and processing responses in JSON format
                print("Error decoding JSON response:", e)
                raise ValueError("Invalid JSON response from OMDb API.")
            except Exception as e:
                print("General error fetching data from OMDb:", e)
                raise
        else:
            raise Exception("Error fetching data from OMDb API")

    def initialize_database(self):
        db_path = 'data/movies.db'
        # For file operations such as opening or checking the existence of a file
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file {db_path} not found.")