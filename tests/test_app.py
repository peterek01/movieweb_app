import unittest
from app import app, db
from ..datamanager.models import User, Movie


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Tworzenie bazy danych
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Czyszczenie bazy danych po każdym teście
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)  # Adjust to your homepage content

    def test_list_users_page(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Users', response.data)  # Adjust based on your template content

    def test_user_movies_page(self):
        with app.app_context():
            user = User(name="Test User", avatar=1)
            db.session.add(user)
            db.session.commit()

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
        with app.app_context():
            user = User(name="Test User", avatar=1)
            db.session.add(user)
            db.session.commit()

        response = self.app.get(f'/users/{user.id}/add_movie')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Movie for Test User', response.data)

    def test_update_movie_page(self):
        with app.app_context():
            user = User(name="Test User", avatar=1)
            movie = Movie(name="Test Movie", director="Test Director", year=2020, rating=7.5, user_id=1)
            db.session.add(user)
            db.session.add(movie)
            db.session.commit()

        response = self.app.get(f'/users/{user.id}/update_movie/{movie.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Test Movie', response.data)  # Adjust based on your template content

    def test_delete_movie(self):
        with app.app_context():
            user = User(name="Test User", avatar=1)
            movie = Movie(name="Test Movie", director="Test Director", year=2020, rating=7.5, user_id=1)
            db.session.add(user)
            db.session.add(movie)
            db.session.commit()

        response = self.app.get(f'/users/{user.id}/delete_movie/{movie.id}')
        self.assertEqual(response.status_code, 302)  # Redirect after deleting
        with app.app_context():
            self.assertIsNone(Movie.query.get(movie.id))

    def test_search_movies(self):
        response = self.app.get('/search_movies?q=Avatar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Avatar', response.data)  # Adjust based on OMDb API mock or live response

    def test_404_error(self):
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_500_error(self):
        with app.app_context():
            @app.route('/error_test')
            def error_test():
                raise Exception("Test Error")

        response = self.app.get('/error_test')
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
