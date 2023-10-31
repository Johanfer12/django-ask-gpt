// Agregar evento click al botón de hamburguesa
document.getElementById("hamburger-button").addEventListener("click", function() {
    const sidebar = document.getElementById("sidebar");
    sidebar.style.left = sidebar.style.left == "0px" ? "-250px" : "0px";
    const menu = sidebar.querySelector(".menu");
    menu.style.display = sidebar.style.left == "0px" ? "block" : "none";
});

// Agregar evento click al botón de usuario
document.getElementById("user-button").addEventListener("click", function () {
    const sidebar = document.getElementById("user-sidebar");
    sidebar.style.right = sidebar.style.right === "0px" ? "-400px" : "0px";
    const menu_user = sidebar.querySelector(".menu_user");
    menu_user.style.display = sidebar.style.right == "0px" ? "block" : "none";
});

document.addEventListener("DOMContentLoaded", function () {
    // Busqueda AJAX
    // Cuando cualquier cuadro de búsqueda cambia, hace una solicitud de búsqueda AJAX.
    $("#atc, #cum, #principio-activo").on('input', function(e) {
        var atcValue = $('#atc').val().trim();
        var cumValue = $('#cum').val().trim();
        var principioActivoValue = $('#principio-activo').val().trim();
    
        if(atcValue || cumValue || principioActivoValue) {
            $.ajax({
                type: 'GET',
                url: '/', 
                data: {
                    'atc': atcValue,
                    'cum': cumValue,
                    'principio_activo': principioActivoValue,
                },
                success: function(data) {
                    var newData = JSON.parse(data);
                    $('#table_body').empty();
                    if(newData.length === 0) {
                        if(atcValue || cumValue || principioActivoValue) {
                            $('#table_body').append('<tr><td colspan="4">No se encontraron resultados.</td></tr>');
                        } else {
                            $('#table_body').append('<tr><td colspan="4">Por favor, ingresa texto en los campos para buscar.</td></tr>');
                        }
                    } else {
                        // Agrega los encabezados a la tabla
                        $('#table_body').append(`
                            <tr>
                                <th>CUM</th>
                                <th>Código ATC</th>
                                <th>ATC</th>
                                <th>Principio Activo</th>
                            </tr>`
                        );
                
                        // Agrega las filas de resultados
                        for(let item in newData){
                            $('#table_body').append(`
                                <tr>
                                    <td>${newData[item].fields.CUM}</td>
                                    <td>${newData[item].fields.codigo_atc}</td>
                                    <td>${newData[item].fields.ATC}</td>
                                    <td>${newData[item].fields.principio_activo}</td>
                                </tr>`
                            );
                        }
                    }
                }
            });
        } else {
            $('#table_body').empty();
            $('#table_body').append('<tr><td colspan="4">Por favor, ingresa texto en los campos para buscar.</td></tr>');
        }
    });        
});    

// Movimiento de resultados al abrir el menú
var sidebar = document.querySelector("#hamburger-button");
var results = document.querySelector("#results");

// Añade un detector de eventos al menú desplegable
sidebar.addEventListener("click", function() {
  if (sidebar.classList.contains("open")) {
    // Si el menú desplegable está abierto, ciérralo y mueve los resultados de nuevo
    sidebar.classList.remove("open");
    results.classList.remove("moved");
  } else {
    // Si el menú desplegable está cerrado, ábrelo y mueve los resultados
    sidebar.classList.add("open");
    results.classList.add("moved");
  }
});