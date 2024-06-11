document.addEventListener('DOMContentLoaded', (event) => {
    const container = document.getElementById('container');
    const loginButton = document.getElementById('login');
    const registerButton = document.getElementById('register');
    const registerBtn = document.getElementById('registerBtn');
    const loginBtn = document.getElementById('loginBtn');

    loginButton.addEventListener('click', () => {
        container.classList.remove('right-panel-active');
    });

    registerButton.addEventListener('click', () => {
        container.classList.add('right-panel-active');
    });

    registerBtn.addEventListener('click', () => {
        
    });

    loginBtn.addEventListener('click', () => {
        
    });
});
