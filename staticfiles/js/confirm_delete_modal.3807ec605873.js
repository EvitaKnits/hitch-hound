// Wait for the DOM content to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the delete confirmation modal, modal title, and confirm delete button
    const confirmDeleteModal = document.getElementById('confirmDeleteModal');
    const deleteModalTitle = document.getElementById('deleteModalTitle');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    
    // Variable to store the ID of the item to be deleted
    let deleteId = '';

    // Add event listeners to all delete issue buttons    
    document.querySelectorAll('.delete-issue-button').forEach(button => {
        button.addEventListener('click', function() {
            // Store the ID of the issue to be deleted
            deleteId = this.dataset.id;
            // Set the modal title
            deleteModalTitle.innerText = 'Are you sure you want to delete this issue?';
            // Set the confirm delete button's onclick function to submit the delete form
            confirmDeleteBtn.onclick = function() {
                document.getElementById(`deleteIssueForm_${deleteId}`).submit();
                // Set a session storage item to show an alert after deletion
                sessionStorage.setItem('Alert Type', 'Issue Deleted');
            };
            // Display the deletion modal
            confirmDeleteModal.style.display = 'block';
        });
    });

    // Add event listeners to all delete project buttons
    document.querySelectorAll('.delete-project-button').forEach(button => {
        button.addEventListener('click', function() {
            // Store the ID of the project to be deleted
            deleteId = this.dataset.id;
            // Set the modal title
            deleteModalTitle.innerText = 'Are you sure you want to delete this project?';
            // Set the confirm delete button's onclick function to submit the delete form
            confirmDeleteBtn.onclick = function() {
                document.getElementById(`deleteProjectForm_${deleteId}`).submit();
                // Set a session storage item to show an alert after deletion
                sessionStorage.setItem('Alert Type', 'Project Deleted');
            };
            // Display the deletion modal
            confirmDeleteModal.style.display = 'block';
        });
    });

    // Add event listener to close the modal when the close button is clicked
    document.getElementById('closeModal').addEventListener('click', function() {
        confirmDeleteModal.style.display = 'none';
    });

    // Add event listener to cancel the deletion when the cancel button is clicked
    document.getElementById('cancelDeleteBtn').addEventListener('click', function() {
        confirmDeleteModal.style.display = 'none';
    });

    // Close the modal if the user clicks outside of it
    window.onclick = function(event) {
        if (event.target == confirmDeleteModal) {
            confirmDeleteModal.style.display = 'none';
        }
    };
});
