# MovieWeb

MovieWeb is a web application designed to manage users and their favorite movies. The project is built with Flask, 
SQLAlchemy, and integrates with the OMDb API for fetching movie details.

## Features

- **User Management**: Add, update, and delete users.
- **Movie Management**: Add, edit, and remove movies for users.
- **Integration with OMDb API**: Automatically fetch movie details (e.g., director, release year, rating) 
from OMDb when adding movies.
- **Database Management**: Built using SQLite for local storage of users and movies.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- OMDb API
- HTML/CSS for templates and styling

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/peterek01/movieweb_app.git
   cd movieweb_app

2. **Set Up a Virtual Environment Create and activate a Python virtual environment to isolate dependencies:**
python -m venv venv
source venv/bin/activate  # On Windows, use:
`venv\Scripts\activate`

3. **Install Dependencies Use pip to install the required dependencies listed in requirements.txt:**
pip install -r requirements.txt

4. **Initialize the Database Ensure the database file and tables are created:**
python
>>> from app import db
>>> db.create_all()
>>> exit()

5. **Run the Application Start the Flask development server:**
python app.py

6. **Access the Application Open your browser and navigate to:**
http://127.0.0.1:5000/

Usage
Add Users: Navigate to /add_user to create new users.
Manage Movies: Access /users/<user_id> to view and manage a user's favorite movies.
OMDb Integration: Use the OMDb API to automatically fetch movie details when adding movies.
Error Pages: Custom error pages for 404, 400, and 500 errors.

Project Structure
movieweb_app/
├── app.py                        # Main Flask application
├── .gitignore                    # Git ignore file for sensitive or unnecessary files
├── README.md                     # Project documentation
├── data/                         # Data directory
│   ├── movies.db                 # SQLite database for movies
├── datamanager/                  # Data management modules
│   ├── __init__.py               # Initialization for the datamanager package
│   ├── data_manager.py           # Core data management logic
│   ├── data_manager_interface.py # Interface for data management
│   ├── models.py                 # SQLAlchemy ORM models
├── templates/                    # HTML templates
│   ├── home.html                 # Home page
│   ├── add_movie.html            # Form for adding a movie
│   ├── update_movie.html         # Form for editing a movie
│   ├── user_movies.html          # User's movie collection
│   ├── add_user.html             # Form for adding a user
│   ├── list_users.html           # List of users
│   ├── 400.html                  # 400 error page
│   ├── 403.html                  # 403 error page
│   ├── 404.html                  # 404 error page
│   ├── 500.html                  # 500 error page
├── static/                       # Static files (CSS, JS, images)
│   ├── CSS/
│   │   ├── home_style.css        # Styling for the home page
│   │   ├── add_movie_style.css   # Styling for adding movies
│   │   ├── update_movie_style.css# Styling for editing movies
│   │   ├── user_movies_style.css # Styling for user's movie collection
│   │   ├── add_user_style.css    # Styling for adding a user
│   │   ├── users_style.css       # Styling for the list of users
│   │   ├── error_style.css       # Styling for error pages
│   │   ├── list_users_style.css  # Styling for the user list
│   │   ├── style.css             # General application styles
│   ├── JS/
│   │   ├── add_movie.js          # JavaScript for adding movies
│   │   ├── user_movies.js        # JavaScript for user's movie collection
│   │   ├── add_user.js           # JavaScript for adding users
│   │   ├── users.js              # JavaScript for managing the user list
│   ├── images/
│   │   ├── film.jpg              # Background image for home and user pages
│   │   ├── avatars/
│   │   │   ├── avatar_1.png      # Avatar 1
│   │   │   ├── avatar_2.png      # Avatar 2
│   │   │   ├── avatar_3.png      # Avatar 3
│   │   │   ├── avatar_4.png      # Avatar 4
├── tests/                        # Test suite
    ├── test_app.py               # Tests for the Flask application
    ├── test_data_manager.py      # Tests for data management logic
    ├── test_models.py            # Tests for SQLAlchemy models



API Integration
This project uses the OMDb API to fetch movie details. Replace api_key in the fetch_movie_details_from_omdb 
function in data_manager.py with your own API key.

Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

