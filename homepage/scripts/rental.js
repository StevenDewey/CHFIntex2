$(function() {

    $('.sweetPics').slick({
      autoplay: true,
      autoplaySpeed: 2000,
      dots: true,
      infinite: true,
      speed: 500,
      fade: true,
      cssEase: 'linear'
    });

    $('.add_button').on('click', function() {

        var qty = $(this).attr('data-qty');
        var pid = $(this).attr('data-pid');

        console.log("the rental.js add method is working #1");
        $('#shoppingCart').modal('show');
        console.log("the rental.js add method is working #2");
        $.ajax({
            url: '/homepage/rentalShoppingCart.add/' + pid + '/' + 1,
            success: function(data){
                $('#shoppingCart').find('.modal-body').html(data)
            },//success
        });//ajax
        console.log("the rental.js add method is working #3");
    });//click

    $('#rent_shop_cart_btn').on('click', function() {
        $('#shoppingCart').modal('show');
        $.ajax({
            url: '/homepage/rentalShoppingCart/',
            success: function(data){
                $('#shoppingCart').find('.modal-body').html(data)
            },//success
        });//ajax
    });//click
    // $.loadmodal({
    //     url: "/homepage/product_detail/" + pid,
    //     title: 'Shopping Cart'
    //     width: '700px',
    // });

});