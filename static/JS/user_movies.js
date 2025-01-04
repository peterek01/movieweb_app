document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-button");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const movieCard = button.closest(".movie-card");
            const details = movieCard.querySelector(".movie-details");
            const actions = movieCard.querySelector(".movie-actions");
            const confirmDelete = movieCard.querySelector(".confirm-delete");

            details.classList.add("hidden");
            actions.classList.add("hidden");
            confirmDelete.style.display = "block";
        });
    });

    const confirmNoButtons = document.querySelectorAll(".confirm-no");
    confirmNoButtons.forEach(button => {
        button.addEventListener("click", function () {
            const movieCard = button.closest(".movie-card");
            const details = movieCard.querySelector(".movie-details");
            const actions = movieCard.querySelector(".movie-actions");
            const confirmDelete = movieCard.querySelector(".confirm-delete");

            details.classList.remove("hidden");
            actions.classList.remove("hidden");
            confirmDelete.style.display = "none";
        });
    });

    const confirmYesButtons = document.querySelectorAll(".confirm-yes");
    confirmYesButtons.forEach(button => {
        button.addEventListener("click", function () {
            window.location.href = button.dataset.deleteUrl;
        });
    });
});
