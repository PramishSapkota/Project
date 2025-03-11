document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.getElementById("checkbox");

    function drawPieChart(divId, labels, values) {
        const darkMode = document.body.classList.contains("dark-mode");

        let data = [{
            values: values,
            labels: labels,
            type: 'pie',
            textinfo: "label+percent",
            insidetextorientation: "radial",
            marker: {
                colors: darkMode ? ['#1ABC9C', '#3498DB', '#9B59B6', '#F39C12', '#E74C3C'] : ['#FF6F61', '#FFB347', '#6B5B95', '#88B04B', '#92A8D1']
            }
        }];

        let layout = {
            height: 400,
            width: 400,
            paper_bgcolor: darkMode ? '#2c3641' : '#F9FAFB',
            plot_bgcolor: darkMode ? '#1a1a2e' : '#F9FAFB',
            font: { color: darkMode ? '#e0e0e0' : '#000000' },
            margin: { t: 20, b: 20, l: 20, r: 20 },
            showlegend: true
        };

        Plotly.newPlot(divId, data, layout);
    }

    // Pie chart data
    const englishData = { labels: ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], values: [24559, 7965, 3786, 1967, 2155] };
    const romanizedNepaliData = { labels: ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], values: [2706, 985, 506, 382, 324] };
    const devanagariNepaliData = { labels: ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"], values: [2406, 792, 359, 202, 241] };

    // Initial chart load
    drawPieChart("english-pie-chart", englishData.labels, englishData.values);
    drawPieChart("romanized-nepali-pie-chart", romanizedNepaliData.labels, romanizedNepaliData.values);
    drawPieChart("devanagari-nepali-pie-chart", devanagariNepaliData.labels, devanagariNepaliData.values);

    // Tab switching logic
    function openPieTab(evt, tabId) {
        let i, tabContent, tabLinks;

        tabContent = document.getElementsByClassName("pie-tab-content");
        for (i = 0; i < tabContent.length; i++) {
            tabContent[i].style.display = "none";
        }

        tabLinks = document.getElementsByClassName("tab-link");
        for (i = 0; i < tabLinks.length; i++) {
            tabLinks[i].classList.remove("active");
        }

        document.getElementById(tabId).style.display = "block";
        evt.currentTarget.classList.add("active");
    }

    document.querySelector(".tab-link").click(); // Set default tab
    window.openPieTab = openPieTab;

    // Dark mode toggle for pie charts
    checkbox.addEventListener("change", function () {
        setTimeout(() => {
            drawPieChart("english-pie-chart", englishData.labels, englishData.values);
            drawPieChart("romanized-nepali-pie-chart", romanizedNepaliData.labels, romanizedNepaliData.values);
            drawPieChart("devanagari-nepali-pie-chart", devanagariNepaliData.labels, devanagariNepaliData.values);
        }, 300);
    });
});
