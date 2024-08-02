// Wait for the DOM content to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {

    // Get the modal element
    var modal = document.getElementById('my-modal');

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
    };

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = 'none';
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    // Redirect based on user choice
    createIssueBtn.onclick = function() {
        window.location.href = createIssueUrl || '/';
    };
    
    // Redirect based on user choice when create project button is clicked
    createProjectBtn.onclick = function() {
        window.location.href = createProjectUrl || '/';
    };
});
