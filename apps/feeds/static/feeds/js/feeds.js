var alerts    = $('.messages.alert');
var delayTime = 5000 + (alerts.length * 250);
alerts.each(function() {
    $(this).delay(delayTime).fadeOut('slow');
    delayTime -= 250;
});
