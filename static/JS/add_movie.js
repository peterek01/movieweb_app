$(document).ready(function() {
    $('#name').on('input', function() {
        const query = $(this).val().trim();
        if (query.length > 0) {
            $.getJSON('/search_movies', { q: query }, function(data) {
                const suggestions = $('#suggestions');
                suggestions.empty();
                if (data.length > 0) {
                    data.forEach(function(item) {
                        suggestions.append(
                            `<li onclick="selectSuggestion('${item}')">${item}</li>`
                        );
                    });
                } else {
                    suggestions.append('<li>No matches found</li>');
                }
            }).fail(function() {
                console.error("Error fetching movie suggestions.");
            });
        } else {
            $('#suggestions').empty();
        }
    });
});

function selectSuggestion(value) {
    $('#name').val(value);
    $('#suggestions').empty();
}

function closeDuplicateModal() {
        const modal = document.getElementById('duplicate-movie-modal');
        modal.style.display = 'none';
    }

    document.addEventListener('DOMContentLoaded', () => {
        fetch('/users/{{ user.id }}/add_movie', {
            method: 'POST',
            body: new URLSearchParams(new FormData(document.querySelector('form')))
        }).then(response => {
            if (response.status === 409) {
                const modal = document.getElementById('duplicate-movie-modal');
                modal.style.display = 'block';
            }
        });
    });

function closeErrorModal() {
    const modal = document.getElementById('error-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}
