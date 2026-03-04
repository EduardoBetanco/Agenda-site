document.addEventListener("DOMContentLoaded", function () {

    var button = document.getElementById("toggle-btn");
    var statusParagraph = document.getElementById("task-status");

    if (!button) {
        return;
    }

    button.addEventListener("click", function () {

        var taskId = button.getAttribute("data-task-id");
        var csrfToken = button.getAttribute("data-csrf");

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/task/" + taskId + "/toggle-ajax/", true);

        xhr.setRequestHeader("X-CSRFToken", csrfToken);

        xhr.onreadystatechange = function () {

            if (xhr.readyState === 4 && xhr.status === 200) {

                var data = JSON.parse(xhr.responseText);

                if (data.status) {
                    button.textContent = "Marquer non fait";
                } else {
                    button.textContent = "Marquer fait";
                }

                statusParagraph.textContent = "";

                var strong = document.createElement("strong");
                strong.appendChild(document.createTextNode("Statut : "));
                statusParagraph.appendChild(strong);

                var text;

                if (data.status) {
                    text = document.createTextNode("Fait");
                } else {
                    text = document.createTextNode("Non fait");
                }

                statusParagraph.appendChild(text);
            }
        };

        xhr.send();
    });

});
