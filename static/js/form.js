$(document).ready(function () {
    $(".show-btn").on('click', function() {
        if($('#Password').attr("type") == "text"){
        $('#Password').attr('type', 'password');
        }
        else{
        $('#Password').attr('type', 'text');
        }
    });

    $(".show-btna").on('click', function() {
        if($('#ConfirmPassword').attr("type") == "text"){
        $('#ConfirmPassword').attr('type', 'password');
        }
        else{
        $('#ConfirmPassword').attr('type', 'text');
        }
    });

    $(".show-btn2").on('click', function() {
        if($('#password_login').attr("type") == "text"){
        $('#password_login').attr('type', 'password');
        }
        else{
        $('#password_login').attr('type', 'text');
        }
    });
    $('.countrypicker').countrypicker();
    

});
