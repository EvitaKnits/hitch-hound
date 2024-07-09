    document.addEventListener("DOMContentLoaded", function() {
        // Submit the form automatically when checkboxes are changed
        const form = document.querySelector("form");
        const checkboxes = form.querySelectorAll("input[type='checkbox']");
        checkboxes.forEach(function(checkbox) {
            checkbox.addEventListener("change", function() {
                form.submit();
            });
        });
    });
