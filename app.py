from flask import Flask, redirect, render_template, request, url_for
from datamanager.data_manager import SQLiteDataManager
from datamanager.models import db
import requests
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "data/movies.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
data_manager = SQLiteDataManager(db)  # We pass the db instance


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        return render_template('404.html'), 404

    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_details = {
            'name': request.form['name']
        }
        data_manager.add_user(user_details)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.get_user(user_id)
    print(f"User fetched: {user}")
    if not user:
        return render_template('404.html'), 404  # If user does not exist, show 404
    print(f"Rendering add_movie.html with user: {user}")

    if request.method == 'POST':
        # Get movie name from user
        movie_name = request.form['name']

        # Get movie details from OMDb API
        movie_details = data_manager.fetch_movie_details_from_omdb(movie_name)

        # If OMDb API does not return details, use user-provided data
        if not movie_details:
            try:
                movie_details = {
                    "name": movie_name,
                    "director": request.form['director'],
                    "year": int(request.form['year']),
                    "rating": float(request.form['rating']),
                }
            except ValueError as e:
                # Handle error when user input is invalid
                print("Invalid input:", e)
                return render_template('add_movie.html',
                                       user_id=user_id,
                                       user=user,
                                       error="Invalid input data")

        # Remove `user_id` from movie_details if it exists there (for security)
        movie_details.pop("user_id", None)

        # Add movie to database with user association
        data_manager.add_movie(user_id, movie_details)

        # Redirect to user's favorite videos page
        return redirect(url_for('user_movies', user_id=user_id))

    # View the video addition form
    return render_template('add_movie.html', user_id=user_id, user=user)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        try:
            movie_details = {
                "name": request.form['name'],
                "director": request.form['director'],
                "year": int(request.form['year']),
                "rating": float(request.form['rating']),
            }
            data_manager.update_movie(movie_id, movie_details)
        except ValueError as e:
            # When user input needs to be converted to a specific type (e.g. int or float)
            print("Invalid input:", e)
            return "Invalid input data", 400

        return redirect(url_for('user_movies', user_id=user_id))

    movie = data_manager.get_user_movies(movie_id)
    return render_template('update_movie.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
