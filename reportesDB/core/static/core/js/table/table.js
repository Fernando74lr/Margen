// $(document).ready(function() {
//     $('#examplexd').DataTable();
//     $('#example2').addClass('table table-striped table-bordered');
//     $('#example2').DataTable();
// } );    

// function setTable(tagId) {
//     document.getElementById(tagId).DataTable();
// }

$(document).ready(function() {
    
    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#reportrange span').html(start.format('MM/DD/YYYY') + ' - ' + end.format('MM/DD/YYYY'));
        console.log(start.format('MM/DD/YYYY') + ' - ' + end.format('MM/DD/YYYY'));
        $("#date").html(start.format('MM/DD/YYYY') + ' - ' + end.format('MM/DD/YYYY'));
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Hoy': [moment(), moment()],
           'Ayer': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Últimos 7 Días': [moment().subtract(6, 'days'), moment()],
           'Últimos 30 Días': [moment().subtract(29, 'days'), moment()],
           'Este Mes': [moment().startOf('month'), moment().endOf('month')],
           'Último Mes': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        locale: {
            'format': 'MM/DD/YYYY',
            'separator': ' - ',
            'applyLabel': 'Aplicar',
            'cancelLabel': 'Cancelar',
            'fromLabel': 'Desde',
            'toLabel': 'Hasta',
            'customRangeLabel': 'Personalizar',
            'daysOfWeek': [
                'Do',
                'Lu',
                'Ma',
                'Mi',
                'Ju',
                'Vi',
                'Sa'
            ],
            'monthNames': [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril',
                'Mayo',
                'Junio',
                'Julio',
                'Agosto',
                'Septiembre',
                'Octubre',
                'Noviembre',
                'Diciembre'
            ],
            'firstDay': 1
        }
    }, cb);
  
    cb(start, end);  
});  
