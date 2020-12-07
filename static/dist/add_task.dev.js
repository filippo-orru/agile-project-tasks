"use strict";

function handleResponse(response) {
  // TODO: Mit Bootstrap einheitlich gestallten
  // (wie Frontend-Validation)
  console.clear();
  document.getElementById("name").style.borderColor = "#FFFFFF";
  document.getElementById("dueByDate").style.borderColor = "#FFFFFF";
  document.getElementById("createdBy").style.borderColor = "#FFFFFF";
  document.getElementById("assignee").style.borderColor = "#FFFFFF";
  document.getElementById("description").style.borderColor = "#FFFFFF";

  switch (response) {
    // Empty
    case "nameEmpty":
      console.log(response);
      document.getElementById("name").style.borderColor = "#FF0000";
      break;

    case "dueByDateEmpty":
      console.log(response);
      document.getElementById("dueByDate").style.borderColor = "#FF0000";
      break;

    case "createdByEmpty":
      console.log(response);
      document.getElementById("createdBy").style.borderColor = "#FF0000";
      break;

    case "assigneeEmpty":
      console.log(response);
      document.getElementById("assignee").style.borderColor = "#FF0000";
      break;

    case "descriptionEmpty":
      console.log(response);
      document.getElementById("description").style.borderColor = "#FF0000";
      break;
    // Invalid

    case "dueByDateInvalid":
      console.log(response);
      document.getElementById("dueByDate").style.borderColor = "#FF0000";
      break;

    case "dueByDateInPast":
      console.log(response);
      document.getElementById("dueByDate").style.borderColor = "#FF0000";
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
  var name = document.getElementById('name').value;
  var dueByDate = document.getElementById('dueByDate').value;
  var createdBy = document.getElementById('createdBy').value;
  var assignee = document.getElementById('assignee').value;
  var description = document.getElementById('description').value;
  var jsonBody = {
    'name': name,
    'dueByDate': dueByDate.toString().replaceAll("-", ""),
    'createdBy': createdBy,
    'assignee': assignee,
    'description': description
  };
  var request = new XMLHttpRequest();
  request.open("POST", "api/tasks", true);
  request.setRequestHeader("Content-Type", "application/json");

  request.onreadystatechange = function () {
    if (request.readyState === 4) {
      handleResponse(request.response);
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