function addTask() {
    let name = document.getElementById('form-name');
    let dueByDate = document.getElementById('form-dueByDate');
    let createdBy = document.getElementById('form-createdBy');
    let assignee = document.getElementById('form-assignee');
    let description = document.getElementById('form-description');
    let jsonBody = {
        'name': name,
        'dueByDate': dueByDate,
        'createdBy': createdBy,
        'assignee': assignee,
        'description': description,
    }

    let request = XMLHttpRequest();
    request.addEventListener("load", function () {
        request.statusCode
    });
    request.open("POST", "api/tasks");
    request.send();
}

let addTaskButton = document.getElementById('add-task-button');

addTaskButton.addEventListener('click', () => addTask());