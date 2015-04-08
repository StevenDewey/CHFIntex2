$(function() {

     var dur = document.getElementById("duration").value;

    $( "#duration" ).change(function() {
        dur = document.getElementById("duration").value;
        console.log(dur)
    });

    console.log(dur);

    $('.add_button').on('click', function() {

            var pid = $(this).attr('data-pid');

            console.log(dur);
            console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");

              $('#shoppingCart').modal('show');
              $.ajax({
              url: '/homepage/rentalShoppingCart.add/' + pid + '/' + dur,
              success: function(data){
                  $('#shoppingCart').find('.modal-body').html(data)
              },//success
          });//ajax
      });//click

});

/*
function updateQuantity() {
        this.qty = document.getElementById("quantity").value;
        console.log("here!!!!!")
        console.log(this.qty)
    }*/