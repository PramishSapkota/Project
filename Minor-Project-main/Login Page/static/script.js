// Wait for the page to load and then apply the 'loaded' class to fade in
window.addEventListener('load', function () {
    document.body.classList.add('loaded');
});

// const container = document.querySelector('.container');
// const registerBtn = document.querySelector('.register-btn');
// const loginBtn = document.querySelector('.login-btn');

// registerBtn.addEventListener('click', () => {
//     container.classList.add('active');
// });

// loginBtn.addEventListener('click', () => {
//     container.classList.remove('active');
// });

// script.js
document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".container");
    const registerBtn = document.querySelector(".register-btn");
    const loginBtn = document.querySelector(".login-btn");

    registerBtn.addEventListener("click", () => {
        container.classList.add("active");
    });

    loginBtn.addEventListener("click", () => {
        container.classList.remove("active");
    });
});