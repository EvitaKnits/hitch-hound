$(document).ready(function(){
    $('#registrationToast').toast({delay: 10000});
    $('#registrationToast').toast('show');
});

document.addEventListener('DOMContentLoaded', function() {
    var toastEl = document.getElementById('registrationToast');
    if (toastEl) {
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
});