// Wait for the DOM content to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    // Get the alert placeholder element by its ID
    const alertPlaceholder = document.getElementById('live-alert-placeholder');
    // Function to create and append an alert to the alert placeholder
    const appendAlert = (message, type) => {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible" role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
        ].join('');

        alertPlaceholder.append(wrapper);
    };
    
    // Retrieve alert message and type from session storage
    const alertMessage = sessionStorage.getItem('alert_message');
    const alertType = sessionStorage.getItem('alert_type');
    
    // If alert message and type exist in session storage, append the alert and remove the items from session storage
    if (alertMessage && alertType) {
        appendAlert(alertMessage, alertType);
        sessionStorage.removeItem('alert_message');
        sessionStorage.removeItem('alert_type');
    }
    // Retrieve predefined alert type from session storage
    const predefinedAlertType = sessionStorage.getItem('Alert Type');

    // If predefined alert type exists, append the corresponding alert and remove the item from session storage
    if (predefinedAlertType) {
    if (predefinedAlertType) {
        if (predefinedAlertType === 'Issue Deleted') {
            appendAlert('You deleted this issue.', 'danger');
        } else if (predefinedAlertType === 'Project Deleted') {
            appendAlert('You deleted this project.', 'danger');
        } else if (predefinedAlertType === 'Issue Created') {
            appendAlert('You created a new issue.', 'success');
        } else if (predefinedAlertType === 'Project Created') {
            appendAlert('You created a new project.', 'success');
        } else if (predefinedAlertType === 'Password Changed') {
            appendAlert('You successfully changed your password.', 'success');
        }
        sessionStorage.removeItem('Alert Type');
    }
});
