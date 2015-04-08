$(function() {

     var qty = document.getElementById("quantity").value;

    $( "#quantity" ).change(function() {
        qty = document.getElementById("quantity").value;
        console.log(qty)
    });

    console.log(qty);

    $('.add_button').on('click', function() {

            var pid = $(this).attr('data-pid');

            console.log(qty)

              $('#shoppingCart').modal('show');
              $.ajax({
              url: '/homepage/shoppingCart.add/' + pid + '/' + qty,
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