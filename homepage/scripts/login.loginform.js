$(document).ready(function() {

    $('#loginform').ajaxForm(function(data){
        $('#jquery-loadmodal-js-body').html(data);
    });
 
});
