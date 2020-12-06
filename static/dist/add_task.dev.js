"use strict";

function addTask() {
  var name = document.getElementById('form-name').value;
  var dueByDate = document.getElementById('form-dueByDate').value;
  var createdBy = document.getElementById('form-createdBy').value;
  var assignee = document.getElementById('form-assignee').value;
  var description = document.getElementById('form-description').value;
  var jsonBody = {
    'name': name,
    'dueByDate': dueByDate.toString().replaceAll("-", ""),
    'createdBy': createdBy,
    'assignee': assignee,
    'description': description
  };
  console.log(jsonBody);
  var request = new XMLHttpRequest();
  request.open("POST", "api/tasks", true);
  request.setRequestHeader("Content-Type", "application/json");

  request.onreadystatechange = function () {
    if (request.readyState === 4) {
      console.log(request.response);
    }
  };

  var data = JSON.stringify(jsonBody);
  request.send(data);
}

var addTaskButton = document.getElementById('add-task-button');
addTaskButton.addEventListener('click', function (event) {
  event.preventDefault();
  addTask();
});