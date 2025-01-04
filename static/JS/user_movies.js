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
