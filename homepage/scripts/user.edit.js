$(function(){

    $('#id_username').on('change', function() {

        // call the server with username
        var username = $('#id_username').val();
        $.ajax({
            url: '/homepage/user.check_username/',
            type: 'POST',
            data: {
                'u': username,
            },//data
            success: function(resp){
                if(resp =='DoesNotExist'){ //unused username (good)
                    $('#id_username_message_valid').show();
                    $('#id_username_message_valid').text("Valid username");
                    $('#create_submit_button').prop("disabled", false);
                    $('#id_username_message_invalid').hide();
                }else{//used username (bad)
                    $('#id_username_message_invalid').show();
                    $('#id_username_message_invalid').text("That username is taken");
                    $('#create_submit_button').prop("disabled", true);
                    $('#id_username_message_valid').hide()
                }
            }
        });//ajax

    });//change


});//ready