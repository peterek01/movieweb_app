document.addEventListener('DOMContentLoaded', () => {
    const chooseAvatarButton = document.getElementById('choose-avatar');
    const avatarModal = document.getElementById('avatar-modal');
    const closeModalButton = document.querySelector('.close-modal');
    const avatarPreview = document.getElementById('selected-avatar');
    const avatarInputs = document.querySelectorAll('.avatars input[type="radio"]');
    const hiddenAvatarInput = document.getElementById('hidden-avatar');

    chooseAvatarButton.addEventListener('click', () => {
        avatarModal.classList.remove('hidden');
    });

    closeModalButton.addEventListener('click', () => {
        avatarModal.classList.add('hidden');
    });

    avatarInputs.forEach(input => {
        input.addEventListener('change', () => {
            const selectedAvatar = input.value;
            const avatarImage = input.nextElementSibling.src;
            avatarPreview.src = avatarImage;
            hiddenAvatarInput.value = selectedAvatar;
            avatarModal.classList.add('hidden');
        });
    });
});

function openAvatarModal() {
    document.getElementById('avatar-modal').style.display = 'flex';
}

function closeAvatarModal() {
    document.getElementById('avatar-modal').style.display = 'none';
}

function selectAvatar(avatarId) {
    document.getElementById('hidden-avatar').value = avatarId;

    const selectedAvatarImg = document.getElementById('selected-avatar-img');
    selectedAvatarImg.src = `/static/images/avatars/avatar_${avatarId}.png`;

    closeAvatarModal();
}

