document.addEventListener('DOMContentLoaded', function () {
    var logoutModal = document.getElementById('logoutConfirmModal');
    var openLogoutModalBtn = document.getElementById('openLogoutModalBtn');
    var closeLogoutModal = document.getElementById('closeLogoutModal');
    var cancelLogoutBtn = document.getElementById('cancelLogoutBtn');

    // Function to open the modal
    openLogoutModalBtn.addEventListener('click', function () {
        logoutModal.style.display = 'block';
    });

    // Function to close the modal
    closeLogoutModal.addEventListener('click', function () {
        logoutModal.style.display = 'none';
    });

    // Function to cancel and close the modal
    cancelLogoutBtn.addEventListener('click', function () {
        logoutModal.style.display = 'none';
    });

    // Close the modal when the user clicks outside of the modal content
    window.addEventListener('click', function (event) {
        if (event.target == logoutModal) {
            logoutModal.style.display = 'none';
        }
    });
});
