// $(document).ready(function() {
//     $('#examplexd').DataTable();
//     $('#example2').addClass('table table-striped table-bordered');
//     $('#example2').DataTable();
// } );    

// function setTable(tagId) {
//     document.getElementById(tagId).DataTable();
// }

function myFunction(inputID, tableID) {
    var input, filter, table, tr, td, cell, i, j;
    input = document.getElementById(inputID);
    filter = input.value.toUpperCase();
    table = document.getElementById(tableID);
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
      // Hide the row initially.
      tr[i].style.display = "none";
    
      td = tr[i].getElementsByTagName("td");
      for (var j = 0; j < td.length; j++) {
        cell = tr[i].getElementsByTagName("td")[j];
        if (cell) {
          if (cell.innerHTML.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
            break;
          } 
        }
      }
    }
  }

$(document).ready(function() {
    // Date Range Picker
    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        let rangeDate = start.format('MM/DD/YYYY') + ' - ' + end.format('MM/DD/YYYY');
        $('#reportrange span').html(rangeDate);

        console.log(rangeDate);
        let url = rangeDate.split(' - ');
        let beginDate = formatDate(url[0]);
        let endDate = formatDate(url[1]);

        $("#getDataButton").attr('href', `/reports/clients/${beginDate}/${endDate}`);
    }

    function formatDate(date) {
        let beginDate = date.split('/');
        return `${beginDate[2]}-${beginDate[0]}-${beginDate[1]}`;
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
