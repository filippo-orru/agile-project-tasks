let baseUrl = window.location.origin;
var offset = 0;

$(function (){
        loadTasks();
});

function loadTasks(){
    let config = {
        'limit' : 5,
        'offset' : offset,
    }
    $.ajax({
        type: "GET",
        url: baseUrl + '/tasks',
        dataType: 'json',
        data: config,
        success: function (data){
            var even;
            even = offset % 2 == 0;
            var count = 0;
            $.each(data.tasks, function (key, value){
                var template = $('.row-template').clone();
                template.removeClass('row-template');
                template.removeClass('d-none');
                if(even){
                  template.addClass('row-even');
                }
                else{
                    template.addClass('row-odd');
                }
                var templateItems = template.children('div');
                $(templateItems[0]).html(value.name);
                $(templateItems[1]).html(value.assignee);
                var dateString = value.dueByDate;
                var year = dateString.substr(0,4);
                var month = dateString.substr(4,2);
                var day = dateString.substr(6,2);
                $(templateItems[2]).html(day + '.' + month + '.' + year);
                var stateColumn = $(templateItems[3]).children('div');
                $(stateColumn[0]).addClass(value.state);
                $(stateColumn[0]).html(value.state);
                $('#task-table').append(template);
                even = !even;
                count++;
            })
            offset += count;
            if(!data.more){
                $('.buttonDiv').css('display', 'none');
            }
        }

    });
}