document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById("checkbox");

    // Initialize default bar chart tab
    const defaultTab = document.querySelector(".tab-link.active");
    if (defaultTab) {
        const defaultTabName = defaultTab.getAttribute("onclick").match(/'(.*?)'/)[1];
        renderGraphForTab(defaultTabName);
    }

    // Theme toggle handler
    checkbox.addEventListener("change", function() {
        setTimeout(() => {
            const activeTab = document.querySelector(".tab-link.active");
            if (activeTab) {
                const activeTabName = activeTab.getAttribute("onclick").match(/'(.*?)'/)[1];
                renderGraphForTab(activeTabName);
            }
        }, 300);
    });

    function openTab(evt, tabName) {
        document.querySelectorAll(".tab-content").forEach(tab => {
            tab.classList.remove("active");
            tab.style.display = "none";
        });
        document.querySelectorAll(".tab-link").forEach(link => link.classList.remove("active"));
        
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.classList.add("active");
        renderGraphForTab(tabName);
    }
    window.openTab = openTab;

    function renderGraphForTab(tabName) {
        switch (tabName) {
            case "english":
                createBarChart("english-graph", ["SVM", "Logistic Regression", "Random Forest"], [82.44, 72.35, 73.26], "English Model Accuracy");
                break;
            case "romanized-nepali":
                createBarChart("romanized-nepali-graph", ["SVM", "Logistic Regression", "Random Forest"], [81.65, 79.92, 72.07], "Romanized Nepali Model Accuracy");
                break;
            case "devanagari-nepali":
                createBarChart("devanagari-nepali-graph", ["NEPBERT"], [87], "Devanagari Nepali Model Accuracy");
                break;
        }
    }

    function createBarChart(elementId, xValues, yValues, title) {
        Plotly.purge(elementId);
        const darkMode = document.body.classList.contains("dark-mode");
        const colors = darkMode ? ['#1ABC9C', '#3498DB', '#F39C12'] : ['#FF6F61', '#FFB347', '#6B5B95'];

        const data = [{ x: xValues, y: yValues, type: 'bar', marker: { color: colors } }];
        const layout = {
            title: title,
            paper_bgcolor: darkMode ? '#2c3e50' : '#ffffff',
            plot_bgcolor: darkMode ? '#2c3e50' : '#ffffff',
            font: { color: darkMode ? '#e0e0e0' : '#000000' },
            autosize: true,
            margin: { l: 50, r: 50, b: 50, t: 50, pad: 4 }
        };
        Plotly.newPlot(elementId, data, layout);
    }

});
