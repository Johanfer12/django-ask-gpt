document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const userQuestion = document.getElementById("query-input").value;

    // Muestra el spinner
    document.getElementById("loader").style.display = "block";

    fetch("", {
        method: "POST",
        body: new URLSearchParams({ "user_question": userQuestion }),
        headers: {
            "X-CSRFToken": getCookie("csrftoken") // Obtiene el token CSRF desde las cookies
        },
    })
    .then(response => response.json())
    .then(data => {
        const queryOutput = document.getElementById("query-output");
        // Agregar el contenido de manera que se acumulen las respuestas
        queryOutput.innerHTML += "<div class='user-question'><strong>Tú:</strong> <span class='chat-text'>" + userQuestion + "</span></div>";
        queryOutput.innerHTML += "<div class='bot-response'><strong>Asistente:</strong> <span class='chat-text'>" + data.response + "</div>";
        // Limpia el campo de entrada después de enviar la pregunta
        document.getElementById("query-input").value = '';
        // Desplaza el scroll del chat-box al último mensaje
        queryOutput.scrollTop = queryOutput.scrollHeight;
        // Oculta el spinner
        document.getElementById("loader").style.display = "none";
    });
    });

    // Función para obtener el token CSRF desde las cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }