function showToast(message, type) {
    const toastContainer = document.createElement('div');
    toastContainer.className = `toast bg-${type}`;
    toastContainer.role = 'alert';
    toastContainer.ariaLive = 'assertive';
    toastContainer.ariaAtomic = 'true';
    toastContainer.dataset.delay = '5000';

    toastContainer.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">Notification</strong>
            <small class="text-muted">just now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;

    document.body.appendChild(toastContainer);
    const toast = new bootstrap.Toast(toastContainer);
    toast.show();

    toastContainer.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toastContainer);
    });
}

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
                showToast('Issue deleted successfully', 'success');
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
                showToast('Project deleted successfully', 'success');
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
