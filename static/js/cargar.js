$(document).ready(function() {
    $('#cargar_excel').click(function() {
        var excel_file = $('#excel').val();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: 'POST',
            url: '/cargar_leer/',
            headers: { "X-CSRFToken": csrftoken },
            data: { 
                'excel_file': excel_file,
            },
            success: function(data) {
                $('#contenido_resultado').html(data.resultado);
            }
        });
    });

});