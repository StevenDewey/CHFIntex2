$(function() {


    $( '.quantity' ).change(function() {
        var pid = $(this).attr('data-pid');
        var dur = $(this).val();
        $.ajax({
            url: '/homepage/rentalShoppingCart.updateDuration/' + pid +"/" + dur,
        });//ajax
    });

    $('.remove_btn').on('click', function() {

        var pid = $(this).attr('data-pid');

        $('#shoppingCart').modal('show');
        $.ajax({
            url: '/homepage/rentalShoppingCart.remove/' + pid,
            success: function(data){
                $('#shoppingCart').find('.modal-body').html(data)
            },//success
        });//ajax
    });//click
});