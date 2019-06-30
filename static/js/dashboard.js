$(document).ready(function (){
    // Heights for scrollbar 
    $('#meds').height(0);
    var parentHeight = $('#profilePic').height();
    var medsTitleHeight = $('#medsTitle').height();
    $('#meds').height(parentHeight - medsTitleHeight - 15);

    $('#foods').height(0);
    var parentHeight = $('#profilePic').height();
    var foodsTitleHeight = $('#foodsTitle').height();
    $('#foods').height(parentHeight - foodsTitleHeight - 15);

    // Take med - Toggle
    function med_toggle_complete(res, status){
        if (status == 'success') {
            var state = res.responseJSON['state'];
            var med_id = res.responseJSON['med_id'];
            var med_button = $(`[med-id=${med_id}]`);

            if (state == 'not_taken') {
                med_button.removeClass('has-text-success');
                med_button.removeClass('has-text-dark');
                med_button.addClass('has-text-danger');
                $('i', med_button).removeClass('fa-check-circle');
                $('i', med_button).removeClass('fa-clock');
                $('i', med_button).addClass('fa-exclamation-circle');
            } else if (state == 'awaiting'){
                med_button.removeClass('has-text-success');
                med_button.removeClass('has-text-danger');
                med_button.addClass('has-text-dark');
                $('i', med_button).removeClass('fa-check-circle');
                $('i', med_button).removeClass('fa-exclamation-circle');
                $('i', med_button).addClass('fa-clock');
            } else {
                med_button.removeClass('has-text-danger');
                med_button.removeClass('has-text-dark');
                med_button.addClass('has-text-success');
                $('i', med_button).removeClass('fa-exclamation-circle');
                $('i', med_button).removeClass('fa-clock');
                $('i', med_button).addClass('fa-check-circle');
            }
        }
    }

    $('.med-toggle').click(function() {
        var data = {
            med_id: $(this).attr('med-id'),
            csrfmiddlewaretoken :$(this).attr('csrf')
        };
        var args = { type:"POST", url:"/meds/toggle/", data:data, complete: med_toggle_complete };
        $.ajax(args);
    })

    // Take med - Icons Change
    $('.med-toggle').hover(function(){
        // Handler in
        if ($(this).hasClass("has-text-success")) {         // Toggle from Taken
            $(this).removeClass('has-text-success');
            $(this).addClass('has-text-danger');
            $("i", this).addClass('fa-ban');
            $("i", this).removeClass('fa-check-circle')
        } else if ($(this).hasClass("has-text-danger")){    // Toggle from Not taken 
            $(this).addClass('has-text-success');
            $(this).removeClass('has-text-danger');
            $("i", this).addClass('fa-check-circle');
            $("i", this).removeClass('fa-exclamation-circle');
        } else {                                            // Toggle from Awaiting due time
            $(this).addClass('has-text-success');
            $("i", this).addClass('fa-check-circle');
            $("i", this).removeClass('fa-clock');
        }
        
    }, function() {
        // Handler Out
        if ($(this).hasClass("has-text-success")) {        
            $(this).removeClass('has-text-success');
            $("i", this).removeClass('fa-check-circle')
            if (! $(this).hasClass("has-text-dark")){     
                $(this).addClass('has-text-danger');
                $("i", this).addClass('fa-exclamation-circle');
            } else {
                $("i", this).addClass('fa-clock');
                $("i", this).removeClass('fa-check-circle');
            }
        } else if ($(this).hasClass("has-text-danger")){   
            $(this).addClass('has-text-success');
            $(this).removeClass('has-text-danger');
            $("i", this).addClass('fa-check-circle');
            $("i", this).removeClass('fa-ban');
        }
    });
})


// Charts 
var ctx = document.getElementById('medChartBPM').getContext('2d');
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

var ctx = document.getElementById('medChartPre').getContext('2d');
ctx.height = 100;
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto'],
        datasets: [{
            label: 'Pressão Sistólica',
            yAxisID: 'S',
            backgroundColor: 'rgba(255, 99, 132, 0.0)',
            borderColor: '#F44336',
            data: [120, 115, 130, 110, 112, 114, 95, 130]
        },
        {
            label: 'Pressão Diastólica',
            yAxisID: 'D',
            backgroundColor: 'rgba(0, 99, 255, 0.0)',
            borderColor: '#0288D1',
            data: [72, 65, 72, 60, 75, 80, 70, 80]
        }
        ]
    },

    // Configuration options go here
    options: {
        scales: {
            yAxes: [{
                id: 'S',
                type: 'linear',
                position: 'left',
                ticks: {
                    min: 80,
                    max: 180
                }
            }, {
                id: 'D',
                type: 'linear',
                position: 'right',
                ticks: {
                    min: 60,
                    max: 110
                }
            }]
        },
        responsive: true,
        mantainAspectRatio: false
    }
});