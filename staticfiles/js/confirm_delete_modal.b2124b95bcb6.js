document.addEventListener('DOMContentLoaded', function() {
    const confirmDeleteModal = document.getElementById('confirmDeleteModal');
    const deleteModalTitle = document.getElementById('deleteModalTitle');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    let deleteId = '';

    document.querySelectorAll('.delete-issue-button').forEach(button => {
        button.addEventListener('click', function() {
            deleteId = this.dataset.id;
            deleteModalTitle.innerText = 'Are you sure you want to delete this issue?';
            confirmDeleteBtn.onclick = function() {
                document.getElementById(`deleteIssueForm_${deleteId}`).submit();
                sessionStorage.setItem('Alert Type', 'Issue Deleted');
            };
            confirmDeleteModal.style.display = 'block';
        });
    });

    document.querySelectorAll('.delete-project-button').forEach(button => {
        button.addEventListener('click', function() {
            deleteId = this.dataset.id;
            deleteModalTitle.innerText = 'Are you sure you want to delete this project?';
            confirmDeleteBtn.onclick = function() {
                document.getElementById(`deleteProjectForm_${deleteId}`).submit();
                sessionStorage.setItem('Alert Type', 'Project Deleted');
            };
            confirmDeleteModal.style.display = 'block';
        });
    });

    document.getElementById('closeModal').addEventListener('click', function() {
        confirmDeleteModal.style.display = 'none';
    });

    document.getElementById('cancelDeleteBtn').addEventListener('click', function() {
        confirmDeleteModal.style.display = 'none';
    });

    window.onclick = function(event) {
        if (event.target == confirmDeleteModal) {
            confirmDeleteModal.style.display = 'none';
        }
    };
});
