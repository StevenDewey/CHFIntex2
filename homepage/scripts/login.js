$(function(){

    $('#loginform').ajaxForm(function(data){
        //$('#jquery-loadmodal-js-body').html(data);
        $('#loginform_container').html(data);
    });
});
