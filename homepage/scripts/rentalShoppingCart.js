$(function() {


  $( '.quantity' ).change(function() {
      var pid = $(this).attr('data-pid');
      var dur = $(this).val();
      console.log("Here I am!!!")
      console.log(pid)
      console.log(dur)
      $.ajax({
        url: '/homepage/rentalShoppingCart.updateDuration/' + pid +"/" + dur,
      });//ajax
  });

  $('.remove_btn').on('click', function() {

            var pid = $(this).attr('data-pid');

        console.log("made it");
              $('#shoppingCart').modal('show');
              $.ajax({
              url: '/homepage/rentalShoppingCart.remove/' + pid,
              success: function(data){
                  $('#shoppingCart').find('.modal-body').html(data)
              },//success
          });//ajax          
      });//click

});