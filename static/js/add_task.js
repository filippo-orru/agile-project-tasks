function handleResponse(response) {

    // TODO: Mit Bootstrap einheitlich gestalten
    // (wie Frontend-Validation)

    console.log(response);
    $("#name").removeClass('is-invalid');
    $("#dueByDate").removeClass('is-invalid');
    $("#createdBy").removeClass('is-invalid');
    $("#assignee").removeClass('is-invalid');
    $("#description").removeClass('is-invalid');

    document.getElementById("error-text-name").innerHTML = "";
    document.getElementById("error-text-dueByDate").innerHTML = "";
    document.getElementById("error-text-createdBy").innerHTML = "";
    document.getElementById("error-text-assignee").innerHTML = "";
    document.getElementById("error-text-description").innerHTML = "";

    response = JSON.parse(response);
    if (response.includes("success")) {
        window.open('/?success=' + true, "_self");
    }

    response.forEach(message => {
        switch (message) {
            case "nameEmpty":
                $("#name").addClass('is-invalid');
                document.getElementById("error-text-name").innerHTML = "Field must not be empty";
                break;
            case "nameTooLong":
                $("#name").addClass('is-invalid');
                document.getElementById("error-text-name").innerHTML = "Input is too long";
                break;

            case "dueByDateEmpty":
                $("#dueByDate").addClass('is-invalid');
                document.getElementById("error-text-dueByDate").innerHTML = "Field must not be empty";
                break;
            case "dueByDateTooLong":
                $("#dueByDate").addClass('is-invalid');
                document.getElementById("error-text-dueByDate").innerHTML = "Input is too long";
                break;

            case "dueByDateInvalid":
                $("#dueByDate").addClass('is-invalid');
                document.getElementById("error-text-dueByDate").innerHTML = "Date format is invalid";
                break;
            case "dueByDateInPast":
                $("#dueByDate").addClass('is-invalid');
                document.getElementById("error-text-dueByDate").innerHTML = "Date must not be set in the past";
                break;

            case "createdByEmpty":
                $("#createdBy").addClass('is-invalid');
                document.getElementById("error-text-createdBy").innerHTML = "Field must not be empty";
                break;
            case "createdByTooLong":
                $("#createdBy").addClass('is-invalid');
                document.getElementById("error-text-createdBy").innerHTML = "Input is too long";
                break;

            case "assigneeEmpty":
                $("#assignee").addClass('is-invalid');
                document.getElementById("error-text-assignee").innerHTML = "Field must not be empty";
                break;
            case "assigneeEmptyTooLong":
                $("#assigneeEmpty").addClass('is-invalid');
                document.getElementById("error-text-assigneeEmpty").innerHTML = "Input is too long";
                break;

            case "descriptionEmpty":
                $("#description").addClass('is-invalid');
                document.getElementById("error-text-description").innerHTML = "Field must not be empty";
                break;
            case "descriptionTooLong":
                $("#description").addClass('is-invalid');
                document.getElementById("error-text-description").innerHTML = "Input is too long";
                break;
            default:
                console.error("An unknown error has accured");
        }
    });

}

function addTask() {

    let name = document.getElementById('name').value;
    let dueByDate = document.getElementById('dueByDate').value;
    let createdBy = document.getElementById('createdBy').value;
    let assignee = document.getElementById('assignee').value;
    let description = document.getElementById('description').value;
    let jsonBody = {
        'name': name,
        'dueByDate': dueByDate.toString().replaceAll("-", ""),
        'createdBy': createdBy,
        'assignee': assignee,
        'description': description,
    }

    let request = new XMLHttpRequest();
    request.open("POST", "/api/tasks", true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            handleResponse(request.response);
        }
    };
    let data = JSON.stringify(jsonBody);
    request.send(data);
}

let addTaskButton = document.getElementById('add-task-button');

addTaskButton.addEventListener('click', function (event) {
    event.preventDefault();
    addTask();
});