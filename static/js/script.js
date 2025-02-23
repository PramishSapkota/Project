const checkbox = document.getElementById('checkbox');
document.addEventListener('DOMContentLoaded', () => {
  const checkbox = document.getElementById('checkbox');
  
  // Check stored theme on load
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    if (checkbox) checkbox.checked = true;
  } else {
    document.body.classList.remove('dark-mode');
    if (checkbox) checkbox.checked = false;
  }
  
  // Listen for changes on the checkbox
  if (checkbox) {
    checkbox.addEventListener('change', () => {
      if (checkbox.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
      } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
      }
    });
  }
});


document.addEventListener('DOMContentLoaded', () => {
  function applyLoaderEffect(formId) {
    const form = document.getElementById(formId);
    if (form) {
      const submitButton = form.querySelector('button[type="submit"]');
      form.addEventListener('submit', () => {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner"></span> Loading...';
      });
    }
  }

  // Apply loader effect to all relevant forms
  applyLoaderEffect('review-form'); 
  applyLoaderEffect('romanized-form'); 
  applyLoaderEffect('devanagari-form'); 
});



