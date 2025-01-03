from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """Retrieve all users from the data source."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies associated with a specific user."""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_details):
        """Add a new movie to the user's list."""
        pass

    @abstractmethod
    def update_movie(self, movie_id, movie_details):
        """Update the details of a specific movie."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a specific movie from the data source."""
        pass

    @abstractmethod
    def add_user(self, user_details):
        """Add a new user to the data source."""
        pass

    @abstractmethod
    def update_user(self, user_id, user_details):
        """Update the details of a specific user."""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Delete a specific user from the data source."""
        pass
