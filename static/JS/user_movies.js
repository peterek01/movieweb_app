function showConfirmation(button) {
    const movieActions = button.closest('.movie-actions');
    const confirmBox = movieActions.querySelector('.confirm-delete');
    const editButton = movieActions.querySelector('.button.edit');

    confirmBox.style.display = 'block';

    button.style.display = 'none';

    if (editButton) {
        editButton.disabled = true;
    }
}

function hideConfirmation(button) {
    const confirmBox = button.closest('.confirm-delete');
    const movieActions = confirmBox.closest('.movie-actions');
    const deleteButton = movieActions.querySelector('.button.danger');
    const editButton = movieActions.querySelector('.button.edit');

    confirmBox.style.display = 'none';

    deleteButton.style.display = 'inline-block';

    if (editButton) {
        editButton.disabled = false;
    }
}

function confirmDeletion(button) {
    const movieActions = button.closest('.movie-actions');
    const form = movieActions.querySelector('.delete-form');

    form.submit();
}

function openModal(movieId, posterElement) {
    fetch(`/movies/${movieId}/details`)
        .then(response => response.json())
        .then(data => {
            if (!data || data.error) {
                alert(data ? data.error : 'Unable to fetch movie details.');
                return;
            }

            const modal = document.getElementById('movie-details-modal');
            const rect = posterElement.getBoundingClientRect();

            modal.style.setProperty('--modal-start-x', `${rect.left + rect.width / 2}px`);
            modal.style.setProperty('--modal-start-y', `${rect.top + rect.height / 2}px`);
            document.getElementById('modal-poster').src = data.poster_url || '/static/images/default-poster.jpg';
            document.getElementById('modal-title').textContent = data.title || 'No title available';
            document.getElementById('modal-description').textContent = data.description || 'No description available.';
            document.getElementById('modal-cast').textContent = data.cast || 'No cast information available.';

            modal.classList.add('visible');
        })
        .catch(error => {
            console.error('Error fetching movie details:', error);
            alert('Unable to fetch movie details.');
        });
}

function closeModal() {
    const modal = document.getElementById('movie-details-modal');
    modal.classList.remove('visible');
}

document.querySelectorAll('.movie-poster').forEach(poster => {
    poster.addEventListener('click', function () {
        const movieId = this.getAttribute('data-movie-id');
        openModal(movieId, this);
    });
});

