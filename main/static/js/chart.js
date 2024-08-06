// Your data
var chartData = [
  { date: "2024-07-16", count: 115 },
  { date: "2024-07-17", count: 100 },
  { date: "2024-07-18", count: 120 },
];

// Extract dates and counts from chartData
var dates = chartData.map((entry) => entry.date);
var counts = chartData.map((entry) => entry.count);

// Get canvas element
var ctx = document.getElementById("lineChart").getContext("2d");

// Create chart
var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: dates,
    datasets: [
      {
        label: "Clicks",
        data: counts,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(drawChart);

// Draw the chart and set the chart values
function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ["Browser", "Percentage"],
    ["Chrome", 114],
    ["Firefox", 8],
    ["Safari", 5],
    ["Opera", 2],
    ["Others", 2],
  ]);

  var devicedata = google.visualization.arrayToDataTable([
    ["Device", "Percentage"],
    ["Desktop", 174],
    ["Mobile", 75],
    ["Tablet", 55],
    ["Others", 75],
  ]);

  var countrydata = google.visualization.arrayToDataTable([
    ["Country", "Percentage"],
    ["India", 41],
    ["USA", 42],
    ["UK", 56],
    ["Others", 77],
  ]);

  new google.visualization.PieChart(document.getElementById("piechart")).draw(
    data,
    { title: "Browser", width: 550, height: 400 }
  );

  new google.visualization.PieChart(document.getElementById("piechart-devices")).draw(
    devicedata,
    { title: "Device", width: 550, height: 400 }
  );

  new google.visualization.PieChart(document.getElementById("piechart-countries")).draw(
    countrydata,
    { title: "Country", width: 550, height: 400 }
  );
}
