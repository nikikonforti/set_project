$(document).ready(function(){
    // sending a connect request to the server.
    // var socket = io.connect('http://localhost:5000');

    // // An event handler for a change of value 
    // $('input.sync').on('input', function(event) {
    //     socket.emit('Slider value changed', {who: $(this).attr('id'), data: $(this).val()});
    //     console.log("who: ")
    //     console.log($(this).attr('id')) //this gets you the slider that is moving, not which tab / user 
    //     console.log("data: ")
    //     console.log($(this).val())
    //     return false;
    // });

    // socket.on('after connect', function(msg){
    //     console.log('After connect', msg);
    // });

    // socket.on('update value', function(msg) {
    //     console.log('Slider value updated');
    //     $('#'+msg.who).val(msg.data);
    //     console.log("who? " + $('#'+msg.who).val(msg.data))
    //     console.log("who update " + msg.who)
    //     console.log("data update " + msg.data)
    // });

    // $(document).on("click", ".play_button", function(){
    //     console.log("play button clicked")
    //     window.location = "/play"
    // })
})