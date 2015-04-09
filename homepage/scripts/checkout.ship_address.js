$(function () {
    $(document).ready(function () {
        $('#checkout_login').modal('show');
        $.ajax({
            url: '/homepage/login.loginformcheckout/',
            success: function (data) {
                $('#checkout_login').find('.modal-body').html(data)
            },//success

        });//ajax
    });//load
    $('#login_submit').on('click', function(){
        $('#checkout_login').modal({
            show: false,
        })
    });

    $('#checkout_next_btn').on('click', function() {
        window.location.href = '/homepage/checkout.payment_info/';
    });
});//ready