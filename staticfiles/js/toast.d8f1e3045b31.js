// Wait for the DOM content to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Get the toast element by its ID
    var toastEl = document.getElementById('registration-toast');
    // If the toast element exists, initialize and show the toast
    if (toastEl) {
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
});