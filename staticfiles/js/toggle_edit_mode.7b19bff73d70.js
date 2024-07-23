// Function to toggle the edit mode of the user details on the profile page
function toggleProfileEditMode() {
    // Get all input and select elements within the profile form
    const profileFormElements = document.querySelectorAll('#profile-form input, #profile-form select');
    // Get the edit button, edit mode buttons, and change password buttons
    const editBtn = document.getElementById('edit-btn');
    const editModeButtons = document.getElementById('edit-mode-buttons');
    const changePasswordBtn = document.getElementById('change-password-btn');

    // Toggle the disabled property of each form element
    profileFormElements.forEach(el => {
        el.disabled = !el.disabled;
    });

    // Toggle the visibility of the edit button, edit mode buttons, and change password button
    editBtn.classList.toggle('d-none');
    editModeButtons.classList.toggle('d-none');
    changePasswordBtn.classList.toggle('d-none');
}

// Wait for the DOM content to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Get all input and select elements within the profile form
    const profileFormElements = document.querySelectorAll('#profile-form input, #profile-form select');

    // Disable all form elements initially
    profileFormElements.forEach(el => {
        el.disabled = true;
    });
});
