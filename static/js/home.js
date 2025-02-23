document.addEventListener('DOMContentLoaded', function() {
    // Mock user login status (replace with actual authentication)
    const isLoggedIn = false; // Set to true to simulate logged-in state
    const username = "TestUser"; // Replace with actual username

    const loginLink = document.getElementById('login-link');
    const userInfo = document.getElementById('user-info');
    const usernameDisplay = document.getElementById('username-display');
    const settingsIcon = document.querySelector('.settings-icon');
    const dropdown = document.querySelector('.dropdown');
    const logoutOption = document.getElementById('logout-option');
    const settingsOption = document.getElementById('settings-option');

    if (isLoggedIn) {
        loginLink.style.display = 'none';
        userInfo.style.display = 'flex';
        usernameDisplay.textContent = `Hello, ${username}`;
    } else {
        loginLink.style.display = 'block';
        userInfo.style.display = 'none';
    }

    settingsIcon.addEventListener('click', function(event) {
        event.preventDefault();
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });

    logoutOption.addEventListener('click', function(event) {
        event.preventDefault();
        // Implement logout functionality here (e.g., clear session, redirect to login)
        alert('Logout clicked'); // Replace with actual logout logic
        // After logout, you might want to reload the page or update the UI
    });

     settingsOption.addEventListener('click', function(event) {
        event.preventDefault();
        // Implement settings functionality  (e.g., redirect to settings page)
        alert('Settings clicked'); // Replace with actual settings logic
        
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!userInfo.contains(event.target) && dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
        }
    });
});


// Tab functionality
function openTab(evt, tabName) {
    const tabContents = document.querySelectorAll(".tab-content");
    const tabLinks = document.querySelectorAll(".tab-link");

    tabContents.forEach(tab => tab.classList.remove("active"));
    tabLinks.forEach(link => link.classList.remove("active"));

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}


function openPieTab(evt, tabName) {
    let i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("pie-tab-content");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].classList.remove("active");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");
  }





  document.addEventListener("DOMContentLoaded", function () {
    function isDarkMode() {
        return document.body.classList.contains("dark-mode");
    }

    function createPieChart(elementId, labels, values) {
        let darkMode = isDarkMode();
        let data = [{
            values: values,
            labels: labels,
            type: 'pie',
            marker: {
                colors: darkMode ? ['#1ABC9C', '#E74C3C', '#F39C12', '#8E44AD', '#2980B9'] 
                                 : ['#FF6F61', '#6B5B95', '#88B04B', '#F2D7D5', '#F4A300']
            }
        }];
        let layout = {
            margin: { t: 20, b: 20, l: 20, r: 20 },
            height: 400,
            width: 400,
            paper_bgcolor: darkMode ? '#2c3e50' : '#ffffff',
            plot_bgcolor: darkMode ? '#2c3e50' : '#ffffff',
            font: {
                color: darkMode ? '#e0e0e0' : '#000000'
            }
        };
        Plotly.newPlot(elementId, data, layout);
    }

    function createBarChart(elementId, xValues, yValues, title) {
        let darkMode = isDarkMode();
        let data = [{
            x: xValues,
            y: yValues,
            type: 'bar',
            marker: {
                color: darkMode ? ['#1ABC9C', '#3498DB', '#F39C12'] : ['#FF6F61', '#FFB347', '#6B5B95']

            }
        }];
        let layout = {
            title: title,
            paper_bgcolor: darkMode ? '#2c3e50' : '#ffffff',
            plot_bgcolor: darkMode ? '#2c3e50' : '#ffffff',
            font: {
                color: darkMode ? '#e0e0e0' : '#000000'
            }
        };
        Plotly.newPlot(elementId, data, layout);
    }

    createPieChart("english-pie-chart", ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], [24559, 7965, 3786, 1967, 2155]);
    createPieChart("romanized-nepali-pie-chart", ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], [2447, 828, 369, 211, 259]);
    createPieChart("devanagari-nepali-pie-chart", ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], [2406, 792, 359, 202, 241]);

    createBarChart("english-graph", ["SVM", "Logistic Regression", "Random Forest"], [82.44, 72.35 , 73.26], "English Model Accuracy");
    createBarChart("romanized-nepali-graph", ["SVM", "Logistic Regression", "Random Forest"], [82.70, 81.85, 71.86], "Romanized Nepali Model Accuracy");
    createBarChart("devanagari-nepali-graph", ["NEPBERT"], [87], "Devanagari Nepali Model Accuracy");

    // Re-render charts when dark mode toggles
    document.getElementById("checkbox").addEventListener("change", function () {
        setTimeout(() => {
            createPieChart("english-pie-chart", ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], [24559, 7965, 3786, 1967, 2155]);
            createPieChart("romanized-nepali-pie-chart", ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], [55, 45]);
            createPieChart("devanagari-nepali-pie-chart", ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], [2406, 792, 359, 202, 241]);

            createBarChart("english-graph", ["SVM", "Logistic Regression", "Random Forest"], [82, 73, 71], "English Model Accuracy");
            createBarChart("romanized-nepali-graph", ["SVM", "Logistic Regression", "Random Forest"], [78, 82, 85], "Romanized Nepali Model Accuracy");
            createBarChart("devanagari-nepali-graph", ["NEPBERT"], [92], "Devanagari Nepali Model Accuracy");
        }, 300);
    });
});





// Flip card animation
document.querySelectorAll('.flip-card').forEach(card => {
    card.addEventListener('click', () => {
        card.querySelector('.flip-card-inner').classList.toggle('flipped');
    });
});