import requests
from flask import Flask, redirect, render_template, request, url_for
from datamanager.data_manager import SQLiteDataManager
from datamanager.models import db
from flask import jsonify
from flask_migrate import Migrate
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(BASE_DIR, "data/movies.db")}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(app)
migrate = Migrate(app, db)
data_manager = SQLiteDataManager(db)  # We pass the db instance

print(f"SQLAlchemy URI: {app.config['SQLALCHEMY_DATABASE_URI']}")


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
    return render_template('user_movies.html', user=user, movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_details = {
            'name': request.form['name'],
            'avatar': request.form['avatar']
        }
        data_manager.add_user(user_details)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        return render_template('404.html'), 404  # Error handling when user does not exist

    if request.method == 'POST':
        movie_name = request.form['name']
        # Check if the video already exists in the user's database
        existing_movie = data_manager.get_user_movie_by_name(user_id, movie_name)
        if existing_movie:
            return render_template(
                'add_movie.html',
                user=user,
                user_id=user_id,
                error="This movie is already in your collection"
            )

        # Get movie details from OMDb
        movie_details = data_manager.fetch_movie_details_from_omdb(movie_name)
        if not movie_details:
            try:
                movie_details = {
                    "name": movie_name,
                    "director": request.form['director'],
                    "year": int(request.form['year']),
                    "rating": float(request.form['rating']),
                }
            except ValueError:
                return render_template(
                    'add_movie.html',
                    user=user,
                    user_id=user_id,
                    error="Invalid input data"
                )

        # Add a movie to the database
        movie_details['user_id'] = user_id
        data_manager.add_movie(user_id, movie_details)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user, user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    # Download movie details
    movie = data_manager.get_movie(movie_id)

    if not movie:
        return "Movie not found", 404  # Handling the case where the movie doesn't exist

    if request.method == 'POST':
        try:
            # Downloading data from the form
            movie_details = {
                "name": request.form['name'],
                "director": request.form['director'],
                "year": int(request.form['year']),
                "rating": float(request.form['rating']),
            }
            # Update movie in database
            data_manager.update_movie(movie_id, movie_details)
            return redirect(url_for('user_movies', user_id=user_id))
        except ValueError as e:
            # Handling invalid input data
            print("Invalid input:", e)
            return render_template(
                'update_movie.html',
                movie=movie,
                user_id=user_id,
                error="Invalid input data. Please check the values and try again."
            )

    # Displaying a form with movie data for editing
    return render_template('update_movie.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    if not movie:
        return jsonify({'success': False, 'error': 'Movie not found'}), 404

    try:
        data_manager.delete_movie(movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        print(f"Error deleting movie: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    try:
        # Checking if user exists
        user = data_manager.get_user(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Deleting a user
        data_manager.delete_user(user_id)
        return jsonify({'success': True}), 200

    except ValueError as ve:
        # Handling specific exceptions such as user not present
        print(f"ValueError: {ve}")
        return jsonify({'success': False, 'error': str(ve)}), 400

    except Exception as e:
        # Logging general errors
        print(f"Error deleting user: {e}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500


@app.route('/search_movies', methods=['GET'])
def search_movies():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])  # Return an empty list if no query

    OMDB_API_KEY = "2e8cb9fe"
    url = f"http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            # Extract movie titles from the response
            movie_titles = [movie.get("Title", "Unknown") for movie in data.get("Search", [])]
            return jsonify([movie['Title'] for movie in data.get('Search', [])])

    return jsonify([])  # Return empty list if no matches


@app.route('/movies/<int:movie_id>/details', methods=['GET'])
def get_movie_details(movie_id):
    movie = data_manager.get_movie(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    # If the data is already in the database, return it
    if movie.description and movie.cast:
        return jsonify({
            'title': movie.name,
            'description': movie.description,
            'cast': movie.cast,
            'poster_url': movie.poster_url
        })

    # If data is missing, please download it from OMDb API
    omdb_data = data_manager.fetch_movie_details_from_omdb(movie.name)
    if not omdb_data:
        return jsonify({'error': 'Unable to fetch movie details from OMDb API'}), 500

    # Database update with new data
    movie.description = omdb_data.get('description', 'No description available.')
    movie.cast = omdb_data.get('cast', 'No cast information available.')
    db.session.commit()

    return jsonify({
        'title': movie.name,
        'description': movie.description,
        'cast': movie.cast,
        'poster_url': movie.poster_url
    })


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
