function handleResponse(response) {

    // TODO: Mit Bootstrap einheitlich gestallten
    // (wie Frontend-Validation)

    console.clear();
    document.getElementById("form-name").style.borderColor = "#FFFFFF";
    document.getElementById("form-dueByDate").style.borderColor = "#FFFFFF";
    document.getElementById("form-createdBy").style.borderColor = "#FFFFFF";
    document.getElementById("form-assignee").style.borderColor = "#FFFFFF";
    document.getElementById("form-description").style.borderColor = "#FFFFFF";

    switch (response) {
        // Empty
        case "nameEmpty":
            console.log(response);
            document.getElementById("form-name").style.borderColor = "#FF0000";
            break;
        case "dueByDateEmpty":
            console.log(response);
            document.getElementById("form-dueByDate").style.borderColor = "#FF0000";
            break;
        case "createdByEmpty":
            console.log(response);
            document.getElementById("form-createdBy").style.borderColor = "#FF0000";
            break;
        case "assigneeEmpty":
            console.log(response);
            document.getElementById("form-assignee").style.borderColor = "#FF0000";
            break;
        case "descriptionEmpty":
            console.log(response);
            document.getElementById("form-description").style.borderColor = "#FF0000";
            break;
        // Invalid
        case "dueByDateInvalid":
            console.log(response);
            document.getElementById("form-dueByDate").style.borderColor = "#FF0000";
            break;
        // Success
        case "success":
            console.log("yey");
            break;
        default:
            console.log("Yo, wtf?!");
    }
}

function addTask() {

    let name = document.getElementById('form-name').value;
    let dueByDate = document.getElementById('form-dueByDate').value;
    let createdBy = document.getElementById('form-createdBy').value;
    let assignee = document.getElementById('form-assignee').value;
    let description = document.getElementById('form-description').value;
    let jsonBody = {
        'name': name,
        'dueByDate': dueByDate.toString().replaceAll("-", ""),
        'createdBy': createdBy,
        'assignee': assignee,
        'description': description,
    }

    let request = new XMLHttpRequest();
    request.open("POST", "api/tasks", true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function(){
        if(request.readyState === 4){
            handleResponse(request.response);
        }
    };
    let data = JSON.stringify(jsonBody);
    request.send(data);
}

let addTaskButton = document.getElementById('add-task-button');

addTaskButton.addEventListener('click', function(event){
    event.preventDefault();
    addTask();
});