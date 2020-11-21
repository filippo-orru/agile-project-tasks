$(() => printSite());

function printSite() {
    let config = { 'limit': -1 }

    $.ajax({
        type: 'GET',
        url: 'tasks',
        dataType: 'json',
        data: config,
        success: function (data) {
            var even;
            even = false;
            var count = 0;
            $.each(data.tasks, function (key, value) {
                var template = $('.row-template').clone();
                template.removeClass('row-template');
                template.removeClass('d-none');
                if (even) {
                    template.addClass('row-even');
                } else {
                    template.addClass('row-odd');
                }
                var templateItems = template.children('div');
                $(templateItems[0]).html(value.name);
                $(templateItems[1]).html(value.assignee);
                var dateString = value.dueByDate;
                var year = dateString.substr(0, 4);
                var month = dateString.substr(4, 2);
                var day = dateString.substr(6, 2);
                $(templateItems[2]).html(day + '.' + month + '.' + year);
                var stateColumn = $(templateItems[3]).children('div');
                $(stateColumn[0]).addClass(value.state);
                $(stateColumn[0]).html(value.state);
                $('#task-table').append(template);
                even = !even;
                count++;
            })
        },
        complete: () => {
            window.print();
        },
    });
}