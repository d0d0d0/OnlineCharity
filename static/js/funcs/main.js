$(document).ready(function() {

    var grid = null;
    var need = [];

    $("#sidemenu ul li").click(function() {
        $("#sidemenu ul li").each(function() {
            $(this).css('background', '#f1f1f1');
            $(this).css('color', 'black');
        });
        $(this).css('background', '#4CAF50');
        $(this).css('color', 'white');
    });

    function refreshErrorList() {
        $( "#error_list").children('li').each(function() {
            $(this).remove();
        });
    }

    function refrestAddPanel() {
        $(".add_input").each(function () {
            $(this).val('');
        });
    }

    function writeErrorList(error_list) {
        for(var i=0; i < error_list.length; i++) {
            $( "#error_list" ).append( "<li>" + error_list[i] + "</li>" );
        }
    }

    function hidePanels() {
        $("#edit_panel").css('visibility','hidden');
        $("#add_panel").css('visibility','hidden');
    }

    function sendAJAX(request, url, data, type) {
        var csrftoken = $.cookie('csrftoken');

        function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain)
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }

        });

        $.ajax({
            traditional: true, type: request, url: url,
            data: data,

            success: function (response) {
                refreshErrorList();

                if(type == 'initGrid') {
                    createGrid(response['data']);
                }

                if(type == 'addRow') {
                    if(response['availability']) {
                        addRow('.add_input');
                        refrestAddPanel();
                    }
                    else {
                        hidePanels();
                        writeErrorList(response['errors']);
                    }
                }

                if(type == 'editRow') {
                    if(response['availability']) {
                        grid.row('.selected').remove().draw( false );
                        addRow('.edit_input');
                    }
                    else {
                        hidePanels();
                        writeErrorList(response['errors']);
                    }
                }

                if(type == 'deleteRow') {
                    if(response['availability']) {
                        grid.row('.selected').remove().draw( false );
                    }
                    else {
                        hidePanels();
                        writeErrorList(response['errors']);
                    }
                }

                if(type == 'editCharity') {
                    return response;
                }

                return response;
            },
            failed: function (response) {
                return false;
            }
        });
    }

    $(function getTableData() {
        var request = 'GET',
            url = '/API/Person/',
            data = null,
            type = 'initGrid';
        sendAJAX(request, url, data, type);
    });

    function createGrid(dataSet) {
        grid = $('#person_list').DataTable({
            data: dataSet,
            columns: [
                {title: "TC Kimlik No"},
                {title: "Ad - Soyad"},
                {title: "İhtiyaç"},
                {title: "Açıklama"},
                {title: "Öncelik"}
            ]
        });
    }

    function addRow(input) {
        var input_array = [];
        $(input).each(function () {
            input_array.push($(this).val());
        });
        grid.row.add([
            input_array[0],
            input_array[1],
            need,
            input_array[3],
            input_array[4]

        ]).draw(false);
    }

    function isEmpty(input) {
        var is_empty = false;
        $(input).each(function() {
            if($(this).val().length == 0 && $(this).is('.dropdown') == false) {
                is_empty = true;
            }
        });
        return is_empty;
    }

    function prepareInput(input) {
        var input_array = [];
        $(input).each(function () {
            input_array.push($(this).val());
        });
        need = [];
        if(input == '.add_input') {
            $('.add_dd_panel').each(function() {
                if($(this).is(':checked')) {
                    need.push($(this).val());
                }
            });
            need = need.join(',');
        }
        else {
            $('.edit_dd_panel').each(function() {
                if($(this).is(':checked')) {
                    need.push($(this).val());
                }
            });
            if(need.length == 0) {
                need = $('.edit_hida').text();
            }
            else {
                need = need.join(',');
            }
        }
        return {'tc_no': input_array[0], 'name': input_array[1],
                'need': need, 'description': input_array[3],
                'priority': input_array[4]};
    }

    function hideToggle(t1, t2, is_toggle) {
        $( "#error_list").children('li').each(function() {
            $(this).remove();
        });
        if($(t1).css("visibility") == 'hidden') {
            $(t1).css('visibility','visible');
            $(t2).css('visibility','hidden');
        }
        else if(is_toggle){
            $(t1).css('visibility','hidden');
        }
    }

    $("#about_company_menu").click(function() {
        hideToggle('#about_company_container', '#person_list_container', false);
        hidePanels();
    });

    $("#person_list_menu").click(function() {
        hideToggle('#person_list_container', '#about_company_container', false);
    });

    $("#person_list" ).click(function(event) {
        var t = event.target;
        if ( $(t).is( "td" ) ) {
            var row = event.target.closest('tr');
            if ($(row).hasClass('selected') ) {
                $(row).removeClass('selected');
            }
            else {
                grid.$('tr.selected').removeClass('selected');
                $(row).addClass('selected');
            }
        }
    });

    $('#delete_button').click(function () {
        hidePanels();
        var id = (grid.$('tr.selected').children('td')).html() ;
        var request = 'DELETE',
            url = '/API/Person/' + id,
            data = '',
            type = 'deleteRow';
        sendAJAX(request, url, data, type);
    } );

    $('#edit_charity_button').click(function () {
        var data = {'address': $('#c_address').html(), 'description': $('#c_description').html()};
        var request = 'PUT',
            url = '/API/Charity/' + $('#c_name_span').html(),
            type = 'editCharity';
        sendAJAX(request, url, data, type);
    } );


    $('#add_panel_button').click(function () {
        hideToggle('#add_panel', '#edit_panel', true);
        refrestAddPanel();
    } );

    $('#edit_panel_button').click(function () {
        refrestAddPanel();
        var selected = grid.$('tr.selected');
        if(selected.length > 0) {
            var values = [];
            selected.children('td').each(function() {
                values.push($(this).text());
            });
            $('.edit_hida').text(values[2]);
            $('.edit_input').each(function() {
                $(this).val(values.shift());
            }
            );
            hideToggle('#edit_panel', '#add_panel', false);
        }
        else {
            alert('Kişi seçin.')
        }
    } );

    $( "#add_button" ).click(function() {
        if(isEmpty('.add_input')) {
            alert('Tüm alanları doldurmalısınız.');
        }
        else {
            var request = 'POST',
                url = '/API/Person/',
                data = prepareInput('.add_input'),
                type = 'addRow';
            sendAJAX(request, url, data, type);
        }
    });

    $( "#edit_button" ).click(function() {
        if(isEmpty('.edit_input')) {
            alert('Tüm alanları doldurmalısınız.');
        }
        else {
            var id = (grid.$('tr.selected').children('td')).html() ;
            var request = 'PUT',
                url = '/API/Person/' + id,
                data = prepareInput('.edit_input'),
                type = 'editRow';
            sendAJAX(request, url, data, type);
        }
    });

    $('.add_input').click(function() {
        $(this).val('');
        $(this).css('color', 'black');
    });

    $('.edit_input').click(function() {
        $(this).css('color', 'black');
    });
});