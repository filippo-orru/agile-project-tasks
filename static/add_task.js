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

    console.log(jsonBody);

    let request = new XMLHttpRequest();
    request.open("POST", "api/tasks", true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function(){
        if(request.readyState === 4){
            console.log(request.response);
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