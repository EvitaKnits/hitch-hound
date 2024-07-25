// Wait until the entire DOM content is loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Get the textarea element where users add their comments
    var commentText = document.getElementById('comment-text');
    
    // Get the submit button for adding comments
    var addCommentButton = document.getElementById('add-comment-btn');

    // Add an event listener to the textarea to monitor user input
    commentText.addEventListener('input', function() {
        // If the textarea is not empty after trimming whitespace, enable the submit button
        if (commentText.value.trim() !== "") {
            addCommentButton.disabled = false;
        } else {
            // Otherwise, disable the submit button
            addCommentButton.disabled = true;
        }
    });
});