// New Item Modal

document.addEventListener('DOMContentLoaded', function() {

    // Get the modal
    var modal = document.getElementById('myModal');

    // Get the button that opens the modal
    var btn = document.getElementById('open-modal-btn');

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName('close')[0];

    // Get the buttons inside the modal
    var createIssueBtn = document.getElementById('create-issue-btn');
    var createProjectBtn = document.getElementById('create-project-btn');

    // When the user clicks the button, open the modal 
    btn.onclick = function() {
        modal.style.display = 'block';
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = 'none';
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // Redirect based on user choice
    createIssueBtn.onclick = function() {
        window.location.href = createIssueUrl || '/';
    }

    createProjectBtn.onclick = function() {
        window.location.href = createProjectUrl || '/';
    }
});

// Confirm Delete Modal

document.getElementById('deleteButton').addEventListener('click', function() {
    document.getElementById('confirm-delete-modal').style.display = 'block';
});

document.getElementById('close-modal').addEventListener('click', function() {
    document.getElementById('confirm-delete-modal').style.display = 'none';
});

document.getElementById('cancel-delete-btn').addEventListener('click', function() {
    document.getElementById('confirm-delete-modal').style.display = 'none';
});

document.getElementById('confirm-delete-btn').addEventListener('click', function() {
    document.getElementById('deleteForm').submit();
});

window.onclick = function(event) {
    if (event.target == document.getElementById('confirm-delete-modal')) {
        document.getElementById('confirm-delete-modal').style.display = 'none';
    }
}
