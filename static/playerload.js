$(document).ready(function(){
    $(document).on("click", ".play_button", function(){
        $.ajax({ 
            type: "GET",
            url: "/play",                
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            success: function(result){
                console.log("worked")
            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            },
        }); 
    })
})