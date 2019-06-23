var ctx = document.getElementById('medChart').getContext('2d');
ctx.height = 100;
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto'],
        datasets: [{
            label: 'BPM',
            backgroundColor: 'rgba(255, 99, 132, 0.7)',
            borderColor: 'rgb(255, 99, 132)',
            data: [72, 65, 72, 90, 75, 80, 70, 80]
        }]
    },

    // Configuration options go here
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMin: 60,
                    suggestedMax: 100
                }
            }]
        },
        responsive: true,
        mantainAspectRatio: false
    }
});