var GET_ORDERS_URL = $('input.get_orders_url').val();
var FULFILL_ORDERS_URL = $('input.fulfill_orders_url').val();
var REQUEST_INTERVAL = 5000;

var pending_request;

function getButton(color) {
    return $('.' + color, '#controls .buttons');
} 

function getPkOrder(order) {
    return $('.pk', order).text();
}

function getOrder(pk) {
    return $('#order_' + pk, '.order_list');
}

function selectOrders(orders) {
    for (var i = 0; i < orders.length; i++) {
        var order = orders[i];
        var pk = getPkOrder(order);
        $(getOrder(pk)).toggleClass('selected');
    }
}

function clearSelection() {
    $('.order.selected', '.order_list').removeClass('selected');
}

function displayNotice(message) {
    $('.notice').html(message).fadeIn(150).delay(2000).fadeOut(300);
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
    var selected_orders = $('.order.selected', '.order_list');
    var order, order_tag, i, property;
    $('.order_list').html('');

    for (i = 0; i < orders.length; i++) {
        order = orders[i];
        order_tag = $(template).clone();
        order_tag.attr('id', 'order_' + order['pk']).addClass(order['state']);
        for (property in order) {
            $('.' + property, order_tag).html(order[property]);
        }
        $('.order_list').append(order_tag);    
    }

    selectOrders(selected_orders);
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

    // pending_request = setTimeout(function() { 
    //     requestOrders.call();
    // }, REQUEST_INTERVAL);
}

function fulfillOrders(order_ids) {
    $.ajax({
          'url': FULFILL_ORDERS_URL
        , 'type': 'post'
        , 'data': { 'order_ids': JSON.stringify(order_ids) }
        , 'dataType': 'json'
        , 'success': function(response) {
            displayNotice(response.length + ' order' + (response.length === 1 ? '' : 's') + ' fulfilled');
            buttonActive(false);
            clearSelection();
            clearTimeout(pending_request);
            requestOrders();
        }
        , 'error': function(response) {
            displayNotice('An error occured while sending your request');
            console.log('error', typeof response, response);
        }
    });
}

$('.order', '.order_list').live('click', function() {
    selectOrders($(this));
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

    fulfillOrders(order_ids);
});

$(document).ready(function() {
    requestOrders();
});

