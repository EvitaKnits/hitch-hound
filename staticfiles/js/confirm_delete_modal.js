document.getElementById('deleteButton').addEventListener('click', function() {
    document.getElementById('confirmDeleteModal').style.display = 'block';
});

document.getElementById('closeModal').addEventListener('click', function() {
    document.getElementById('confirmDeleteModal').style.display = 'none';
});

document.getElementById('cancelDeleteBtn').addEventListener('click', function() {
    document.getElementById('confirmDeleteModal').style.display = 'none';
});

document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
    document.getElementById('deleteForm').submit();
});

window.onclick = function(event) {
    if (event.target == document.getElementById('confirmDeleteModal')) {
        document.getElementById('confirmDeleteModal').style.display = 'none';
    }
}

