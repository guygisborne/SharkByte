$('.message').slideDown(500).delay(2500).slideUp(800);

$('input, textarea, select', '.expired').attr('disabled', 'disabled');
$('.buttons button', '.expired').attr('class', 'inactive thinandtall').removeAttr('type');
$('.buttons button', '.expired').removeAttr('onclick');

$('.open_quick_stats').click(function() {
    var container = $(this).parent().parent();
    $('.quick_stats', container).toggle();
    return false;
});
