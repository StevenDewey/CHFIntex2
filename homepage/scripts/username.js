/**
 * Created by David on 2/28/2015.
 */
$(function(){

    $('#id_username').on('change', function() {

        // call the server with username
        var username = $(this).val();
        $.ajax({
            url: '/homepage/username.check_username/',
            type: 'POST',
            data: {
                'a': '1',
                'b': '2',
                'u': username,
            },//data
            success: function(resp){
                if(resp =='1'){ //unused username (good)
                    $('#id_username_message').text("Valid username")
                }else{//used username (bad)
                    $('#id_username_message').text("That username is taken")
                }
            }
        });//ajax

    });//change


});//ready