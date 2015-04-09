$(function(){

    $('#loginform').ajaxForm(function(data){
        //$('#jquery-loadmodal-js-body').html(data);
        $('#loginform_container').html(data);
    });
    // $('#LogInID').on('click', function(){
    //      window.location.href = '/homepage/login.logincheckout/';
    // });
});

