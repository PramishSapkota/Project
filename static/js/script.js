// Wait for the page to load and then apply the 'loaded' class to fade in
window.addEventListener('load', function () {
  document.body.classList.add('loaded');
});

// Toggle between login and register views
const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', () => {
  container.classList.add('active');
});

loginBtn.addEventListener('click', () => {
  container.classList.remove('active');
});

document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll(".star");
  const commentInput = document.querySelector(".text-input");
  const submitButton = document.getElementById("submit-comment");
  const logoutButton = document.getElementById("logout");
  let selectedRating = 0;

  // Rating System
  stars.forEach((star, index) => {
    star.addEventListener("click", () => {
      selectedRating = index + 1;
      updateStars(selectedRating);
    });
  });

  function updateStars(rating) {
    stars.forEach((star, index) => {
      star.classList.toggle("selected", index < rating);
    });
  }

  // Logout Button
  logoutButton.addEventListener("click", function () {
    window.location.href = "login.html"; // Redirect to login page
  });

  // Submit Comment
  submitButton.addEventListener("click", function () {
    const comment = commentInput.value.trim();

    if (selectedRating === 0) {
      alert("Please select a rating before submitting.");
      return;
    }

    if (comment === "") {
      alert("Please leave a comment before submitting.");
      return;
    }

    // Send data to backend
    fetch("/submit-review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: selectedRating, review: comment }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        commentInput.value = ""; // Clear input
        selectedRating = 0; // Reset rating
        updateStars(0);
      })
      .catch((error) => console.error("Error:", error));
  });
});
