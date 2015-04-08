$(function() {


  $( '.quantity' ).change(function() {
      var pid = $(this).attr('data-pid');
      var qty = $(this).val();
      console.log("Here I am!!!")
      console.log(pid)
      console.log(qty)
      $.ajax({
        url: '/homepage/shoppingCart.updateQuantity/' + pid +"/" + qty,
      });//ajax
  });

  $('.remove_btn').on('click', function() {

            var pid = $(this).attr('data-pid');

        console.log("made it");
              $('#shoppingCart').modal('show');
              $.ajax({
              url: '/homepage/shoppingCart.remove/' + pid,
              success: function(data){
                  $('#shoppingCart').find('.modal-body').html(data)
              },//success
          });//ajax
      });//click

});