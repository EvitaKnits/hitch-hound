// Wait for the DOM content to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function () {
    // Get the form element
    const form = document.querySelector('form');
    // Get all the checkbox inputs from the form
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    // Add an event listener to each checkbox to submit the form automatically when changed
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            form.submit();
        });
    });
});