$(document).ready(function () {
    $("#div1").hide();
    $("#vendor").click(function(){
        $("#div1").slideDown();
    });
    $("#customer").click(function(){
        $("#div1").slideUp();
    });
});