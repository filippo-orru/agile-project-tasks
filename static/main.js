let baseUrl = window.location.origin;
var offset = 0;
var lastSearch = '';

$(() => {
    writeSearchParamToSearchBar();
    loadTasks();
    successModal();
    $('.searchbox').keydown(function (event){
        var key = (event.keyCode ? event.keyCode : event.which);

        if(key == '13'){
            addSearchParamsAndLoadTasks(event.target.value);
        }
    });
});


function loadTasks(limit = 5) {
    console.log("loading tasks");
    const search = getURLSearchParam();
    if(search != lastSearch){
        offset = 0;
    }
    let config = {
        'limit': limit,
        'offset': offset,
        'search': search,
    }
    $.ajax({
        type: "GET",
        url: 'api/tasks',
        dataType: 'json',
        data: config,
        success: function (data) {
            console.log("rendering tasks");
            if(search != lastSearch){
                var rows = $('.row-tasks');
                $.each(rows, function (){
                    $(this).remove();
                })

            }
            var even;
            even = offset % 2 == 0;
            var count = 0;
            $.each(data.tasks, function (_, value) {
                var template = $('.row-template').clone();
                template.removeClass('row-template');
                template.removeClass('d-none');
                if (even) {
                    template.addClass('row-even row-tasks');
                } else {
                    template.addClass('row-odd row-tasks');
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
            offset += count;

            if (!data.more) {
                $('.buttonDiv').addClass('d-none');
            }
            else {
                $('.buttonDiv').removeClass('d-none');
            }
            lastSearch = search;
        },
        error: function (e) {
            console.log("loading failed");
        }

    });
}
function writeSearchParamToSearchBar(){
    const search = getURLSearchParam();
    $('.searchbox').val(search);
}

function successModal() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const success = urlParams.get('success');
    if (success === 'true') {
        $('#successModal').modal('show');
        window.history.replaceState(null, null, window.location.href.substring(0, window.location.href.indexOf("?")));
    }
}
function getURLSearchParam(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const search = urlParams.get('search');
    return search ? search : '';
}

function addSearchParamsAndLoadTasks(data){
    if (data){
        window.history.replaceState(null, null, '/?search=' + encodeURIComponent(data));
    }
    else{
        window.history.replaceState(null, null, '/');
    }
    if(data != lastSearch){
        loadTasks();
    }
}


