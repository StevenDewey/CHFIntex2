$(function() {

  //   $('#search').change(function() {
  //       searchTerms = document.getElementById("search").value;
  //       //window.location.href = '/homepage/shoppingCart.filter/'
  //         console.log(searchTerms);
  //         $.ajax({
  //         url: '/homepage/product.filter/' + searchTerms,
  //         success: function(data){
  //             $('#DisplayProducts').find('.displaystuff').html(data)
  //         },//success
  //     });//ajax
  //         console.log("got here");
  // });//click

  //   $('.filter').on('click', function() {
  //       searchTerms = document.getElementById("search").value;
  //       //window.location.href = '/homepage/shoppingCart.filter/'
  //         console.log(searchTerms);
  //         $.ajax({
  //         url: '/homepage/product.filter/' + searchTerms,
  //         success: function(data){
  //             $('#DisplayProducts').find('.displaystuff').html(data)
  //         },//success
  //     });//ajax
  //         console.log("got here");
  // });//click

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

    // $.loadmodal({
    //     url: "/homepage/product_detail/" + pid,
    //     title: 'Shopping Cart'
    //     width: '700px',
    // });

});