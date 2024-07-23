// Wait for the DOM content to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function () {
    // Get references to the logout confirmation modal, open modal button, close modal button, and cancel button
    var logoutModal = document.getElementById('logout-confirm-modal');
    var openLogoutModalBtn = document.getElementById('open-logout-modal-btn');
    var closeLogoutModal = document.getElementById('close-logout-modal');
    var cancelLogoutBtn = document.getElementById('cancel-logout-btn');

    // Add event listener to Logout button to open the modal
    openLogoutModalBtn.addEventListener('click', function () {
        logoutModal.style.display = 'block';
    });

    // Add event listener to close the modal when the close button is clicked
    closeLogoutModal.addEventListener('click', function () {
        logoutModal.style.display = 'none';
    });

    // Add event listener to cancel the logout when the cancel button is clicked
    cancelLogoutBtn.addEventListener('click', function () {
        logoutModal.style.display = 'none';
    });

    // Close the modal if the user clicks outside of it
    window.addEventListener('click', function (event) {
        if (event.target == logoutModal) {
            logoutModal.style.display = 'none';
        }
    });
});
