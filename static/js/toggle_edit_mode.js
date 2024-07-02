function toggleEditMode() {
    const formElements = document.querySelectorAll('#profile-form input, #profile-form select');
    const editBtn = document.getElementById('edit-btn');
    const editModeButtons = document.getElementById('edit-mode-buttons');

    formElements.forEach(el => {
        el.disabled = !el.disabled;
    });

    editBtn.classList.toggle('d-none');
    editModeButtons.classList.toggle('d-none');
}

document.addEventListener('DOMContentLoaded', function() {
    const formElements = document.querySelectorAll('#profile-form input, #profile-form select');
    formElements.forEach(el => {
        el.disabled = true;
    });
});