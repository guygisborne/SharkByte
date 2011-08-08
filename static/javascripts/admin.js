var GET_ORDERS_URL = $('input.get_orders_url').val();
var FULFILL_ORDERS_URL = $('input.fulfill_orders_url').val();
var REQUEST_INTERVAL = 5000;

function getButton(color) {
    return $('.' + color, '#controls .buttons');
} 

function buttonActive(active) {
    active ? getButton('green').removeClass('hidden')
           : getButton('green').addClass('hidden');

    active ? getButton('grey').addClass('hidden')
           : getButton('grey').removeClass('hidden');
}

function setButtonLabel(count) {
    var label = 'Fulfill ' + count + ' Order' + (count === 1 ? '' : 's');
    getButton('green span').html(label);
}

function displayOrders(orders) {
    var template = $('.order.labels').clone().removeClass('labels');
    var order, order_tag, i, property;
    $('.order_list').html('');

    for (i = 0; i < orders.length; i++) {
        order = orders[i];
        order_tag = $(template).clone();
        for (property in order) {
            $('.' + property, order_tag).html(order[property]);
        }
        $('.order_list').append(order_tag);    
    }
}

function requestOrders() {
    $.ajax({
          'url': GET_ORDERS_URL
        , 'type': 'get'
        , 'success': function(response) {
            orders = JSON.parse(response);
            displayOrders(orders);
        }
    });

    setTimeout(function() { 
        requestOrders.call();
    }, REQUEST_INTERVAL);
}

$('.order', '.order_list').live('click', function() {
    $(this).toggleClass('selected');
    var selected = $('.order.selected');
    buttonActive(selected.length > 0);
    setButtonLabel(selected.length);
});

getButton('green').click(function() {
    var orders = $('.order.selected');
    var order_ids = [];
    var order_id, i; 

    for (i = 0; i < orders.length; i++) {
        order_id = parseInt($('.pk', orders[i]).text());
        order_ids.push(order_id);
    }

    // send ajax request to change orders -- give needed data (array of pk's?)     
});

$(document).ready(function() {
    requestOrders();
});

