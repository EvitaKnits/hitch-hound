const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

const alertType = sessionStorage.getItem('Alert Type');
if (alertType != undefined) {
    if (alertType === 'Issue Deleted') {
        appendAlert('You deleted this issue.', 'danger');
        sessionStorage.removeItem('Alert Type')
    } else if (alertType === 'Project Deleted') {
        appendAlert('You deleted this project.', 'danger');
        sessionStorage.removeItem('Alert Type')
    } else if (alertType === 'Issue Created') {
        appendAlert('You created a new issue.', 'success');
        sessionStorage.removeItem('Alert Type')
    } else if (alertType === 'Project Created') {
        appendAlert('You created a new project.', 'success');
        sessionStorage.removeItem('Alert Type')
    }
}
