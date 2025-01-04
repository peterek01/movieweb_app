
function showConfirmation(userId) {
    const modal = document.getElementById(`confirmation-modal-${userId}`);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeConfirmation(userId) {
    const modal = document.getElementById(`confirmation-modal-${userId}`);
    if (modal) {
        modal.style.display = 'none';
    } else {
        console.error(`Modal not found for user ID: ${userId}`);
    }
}

function confirmDelete(userId) {
    $.ajax({
        url: `/users/${userId}/delete`,
        type: 'POST',
        success: function(response) {
            if (response.success) {
                $(`#user-card-${userId}`).remove();
            } else {
                alert('Error deleting user: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('Error deleting user');
        }
    });
}

