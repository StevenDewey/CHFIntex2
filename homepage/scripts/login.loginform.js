$(document).ready(function() {

    $('#loginform').ajaxForm(function(data){
        $('#jquery-loadmodal-js-body').html(data);
    });
    console.log("got here");
	$('#login_submit').on('click', function(){
         window.location.href = '/homepage/login.loginform/' + "true" + "/";
    });
});
