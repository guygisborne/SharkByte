var GET_ORDERS_URL = $('input.get_orders_url').val();
var FULFILL_ORDERS_URL = $('input.fulfill_orders_url').val();
var REQUEST_INTERVAL = 5000;

function getButton(color) {
    return $('.' + color, '#controls .buttons');
} 

function getOrder(pk) {
    return $('#order_' + pk);
}

function setOrderSelect(order_ids, toggle) {
    // set the select state of the array of order_ids
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
        order_tag.attr('id', 'order_' + order['pk']);
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

function fulfillOrders(order_ids) {
    $.ajax({
          'url': FULFILL_ORDERS_URL
        , 'type': 'post'
        , 'data': { 'order_ids': JSON.stringify(order_ids) }
        , 'dataType': 'json'
        , 'success': function(response) {
            console.log('success', typeof response, response);
        }
        , 'error': function(response) {
            console.log('error', typeof response, response);
        }
    });
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

    fulfillOrders(order_ids);
});

$(document).ready(function() {
    requestOrders();
});



// some crap
$(document).ajaxSend(function(event, xhr, settings) {
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie != '') {
var cookies = document.cookie.split(';');
for (var i = 0; i < cookies.length; i++) {
var cookie = jQuery.trim(cookies[i]);

if (cookie.substring(0, name.length + 1) == (name + '=')) {
cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
break;
}
}
}
return cookieValue;
}
function sameOrigin(url) {

var host = document.location.host; // host + port
var protocol = document.location.protocol;
var sr_origin = '//' + host;
var origin = protocol + sr_origin;

return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||

!(/^(\/\/|http:|https:).*/.test(url));
}
function safeMethod(method) {
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
}
});
