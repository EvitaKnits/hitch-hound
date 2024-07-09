document.addEventListener('DOMContentLoaded', () => {
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
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

    const alertMessage = sessionStorage.getItem('alert_message');
    const alertType = sessionStorage.getItem('alert_type');
    if (alertMessage && alertType) {
        appendAlert(alertMessage, alertType);
        sessionStorage.removeItem('alert_message');
        sessionStorage.removeItem('alert_type');
    }

    const predefinedAlertType = sessionStorage.getItem('Alert Type');
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
