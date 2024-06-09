document.getElementById('forgotPasswordForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const message = document.getElementById('message');

    
    if (validateEmail(email)) {
        message.textContent = 'A reset link has been sent to your email address.';
        message.style.color = '#28a745';
    } else {
        message.textContent = 'Please enter a valid email address.';
        message.style.color = '#dc3545';
    }
});

function validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@(([^<>()[\]\.,;:\s@"]+.)+[^<>()[\]\.,;:\s@"]{2,})$/i;
    return re.test(String(email).toLowerCase());
}
