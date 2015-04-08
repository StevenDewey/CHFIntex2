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