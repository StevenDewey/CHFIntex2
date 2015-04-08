/**
 * Created by David on 2/22/2015.
 */
$(function () {

    $('#show_login_dialog').on('click', function () {
        $.loadmodal({
            url: '/homepage/login.loginform/',
            title: 'Sign In',
        });
    });

    $('#checkout_button').on('click', function(){
        window.location.href = '/homepage/checkout/'
    });//click


//mouse-over nav bar drop-downs
    //$('li.dropdown').hover(
    //    function() {
    //        $('ul', this).show();
    //        $(this).addClass('dark_hover')
    //    },
    //    function(){
    //        $('ul', this).hide();
    //        $(this).removeClass('dark_hover')
    //});

});