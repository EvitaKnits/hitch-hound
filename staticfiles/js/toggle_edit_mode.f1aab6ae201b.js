function toggleProfileEditMode() {
    const profileFormElements = document.querySelectorAll('#profile-form input, #profile-form select');
    const editBtn = document.getElementById('edit-btn');
    const editModeButtons = document.getElementById('edit-mode-buttons');
    const changePasswordBtn = document.getElementById('change-password-btn');

    profileFormElements.forEach(el => {
        el.disabled = !el.disabled;
    });

    editBtn.classList.toggle('d-none');
    editModeButtons.classList.toggle('d-none');
    changePasswordBtn.classList.toggle('d-none');
}

document.addEventListener('DOMContentLoaded', function() {
    const profileFormElements = document.querySelectorAll('#profile-form input, #profile-form select');

    profileFormElements.forEach(el => {
        el.disabled = true;
    });
});
