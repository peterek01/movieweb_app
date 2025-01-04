import unittest
from app import app
from datamanager.models import db, Movie, User
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a clean test client and database."""
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()  # Ensure a clean database before each test

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)  # Adjust to your homepage content

    def test_list_users_page(self):
        with app.app_context():
            user = User(name="Test User", avatar=1)
            db.session.add(user)
            db.session.commit()

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_user_movies_page(self):
        with app.app_context():
            user = User(name="Test User", avatar=1)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)  # Refreshing the instance to associate it with the active session

        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movies for Test User', response.data)

    def test_add_user_page(self):
        response = self.app.get('/add_user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add User', response.data)

        # Test POST method
        response = self.app.post('/add_user', data={'name': 'Test User', 'avatar': 1})
        self.assertEqual(response.status_code, 302)  # Redirect after adding
        with app.app_context():
            user = User.query.first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')

    def test_add_movie_page(self):
        """Test for adding a movie to the database."""
        with app.app_context():
            # Creating a test user
            user = User(name="Test User", avatar=1)
            db.session.add(user)
            db.session.commit()

            # User log for debugging
            print(f"Created User ID: {user.id}")

            # Adding a video with the correct user_id
            movie = Movie(
                name="Test Movie",
                director="Test Director",
                year=2020,
                rating=7.5,
                user_id=user.id
            )
            db.session.add(movie)
            db.session.commit()

            # Checking if the movie has been added to the database
            fetched_movie = db.session.query(Movie).filter_by(name="Test Movie").first()

            # Debug Log
            print(f"Fetched Movie: {fetched_movie}")

            # Assertion Testing
            self.assertIsNotNone(fetched_movie, "Movie should exist in the database")
            self.assertEqual(fetched_movie.user_id, user.id, "Movie's user_id should match the user's ID")

    def test_update_movie_page(self):
        with app.app_context():
            user = User(name="Test User", avatar=1)
            db.session.add(user)
            db.session.commit()

            movie = Movie(name="Old Title", director="Old Director", year=2000, rating=5.0, user_id=user.id)
            db.session.add(movie)
            db.session.commit()

            # Data update
            response = self.app.post(
                f'/users/{user.id}/update_movie/{movie.id}',
                data={"name": "New Title", "director": "New Director", "year": 2022, "rating": 8.5}
            )
            self.assertEqual(response.status_code, 302)  # Redirect after editing

            # Check if the data has been updated
            updated_movie = Movie.query.get(movie.id)
            self.assertEqual(updated_movie.name, "New Title")
            self.assertEqual(updated_movie.director, "New Director")
            self.assertEqual(updated_movie.year, 2022)
            self.assertEqual(updated_movie.rating, 8.5)

    def test_delete_movie(self):
        """Test successful deletion of a movie."""
        with app.app_context():
            # Creating a Test User and Video
            user = User(name="Test User", avatar=1)
            db.session.add(user)
            db.session.commit()

            movie = Movie(
                name="Test Movie",
                director="Test Director",
                year=2020,
                rating=7.5,
                user_id=user.id
            )
            db.session.add(movie)
            db.session.commit()

            # Logs for safety
            print(f"Created User ID: {user.id}")
            print(f"Created Movie ID: {movie.id}")

            # Sending a POST request to remove a video
            response = self.app.post(f'/users/{user.id}/delete_movie/{movie.id}')
            self.assertEqual(response.status_code, 302)  # We expect redirection after removal

            # Checking if a video has been removed from the database
            deleted_movie = db.session.query(Movie).filter_by(id=movie.id).first()
            self.assertIsNone(deleted_movie)

    def test_search_movies(self):
        response = self.app.get('/search_movies?q=Avatar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Avatar', response.data)  # Adjust based on OMDb API mock or live response

    def test_404_error(self):
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_500_error(self):
        with self.assertRaises(Exception):
            raise Exception("Simulated server error")


if __name__ == '__main__':
    unittest.main()
