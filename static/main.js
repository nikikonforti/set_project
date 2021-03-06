/*
TODO:
* try playing to very end of deck to see what happens:
    * the last set doesnt leave 
    * make it so that it is okay with 6 cards instead of 9 at end 
*/


var display_hand = function(gameHand){
    console.log("hello")
    console.log(gameHand)
    //empty old data
    $("#deck").empty()
    //insert all data:
    var wrapper = $('#deck');
    var count = 0;
    var container;
    $.each(gameHand, function(i, datum){
        if(count % 3 == 0){
            container = $('<div class="row"></div>');
            wrapper.append(container)
        }
        count = count+1;
        var img = document.createElement("img");
        img.src = "/static/cards/" + datum + ".png";
        var col = $('<div class="col-md-3 centered"></div>')
        col.append(img)
        container.append(col)
    })
}

var deal_three_more = function(gameHand){
    console.log("game hand in deal3more")
    console.log(gameHand)
    $.ajax({ 
        type: "GET",
        url: "/3more",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({gameHand}),
        success: function(result){
            gameHand = result["gameHand"]
            deckSize = result["deckSize"]
            display_hand(gameHand)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        },
    });
}

var remove_correct_set = function(possibleSet){
    $.ajax({ 
        type: "POST",
        url: "/removeSet",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({possibleSet: possibleSet}),
        success: function(result){
            gameHand = result["gameHand"]
            deckSize = result["deckSize"]
            display_hand(gameHand)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        },
    });
    console.log("gameHand at end of remove")
    console.log(gameHand)
    return gameHand
}

var replace_correct_set = function(possibleSet){
    // first, remove the correct set from gameHand
    gameHand = remove_correct_set(possibleSet)
}

var check_set = function(possibleSet, possibleSetSrc){
    console.log(possibleSet)
    $.ajax({ 
        type: "POST",
        url: "/checkSet",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({possibleSet: possibleSet}),
        success: function(result){
            isSet = result["isSet"]
            playerPoints = result["playerPoints"]
            console.log("player points:")
            console.log(playerPoints)
            document.getElementById("score").innerHTML = playerPoints;
            if(isSet){
                alert("Correct!")
                replace_correct_set(possibleSet)
            }
            else{
                alert("Sorry, that's wrong")
                //unselect the cards
                console.log("incorrect set:")
                console.log(possibleSetSrc)
                for (i = 0; i < possibleSetSrc.length; i++) { 
                    possibleSetSrc[i].toggleClass("selectedCard")
                }
            }
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        },
    }); 
}

var check_set_in_hand = function(gameHand){
    $.ajax({ 
        type: "POST",
        url: "/checkSetInHand",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({gameHand: gameHand}),
        success: function(result){
            isSet = result["isSet"]
            playerPoints = result["playerPoints"]
            console.log("player points after check set IN HAND:")
            console.log(playerPoints)
            document.getElementById("score").innerHTML = playerPoints;
            if(isSet){
                alert("Nope! There is a set on the board - try to find it.")
            }
            else{
                deal_three_more(gameHand)
            }
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        },
    }); 
}

Array.prototype.remove = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

$(document).ready(function(){
    var possibleSet = []
    var possibleSetSrc = []
    display_hand(gameHand)
    $(document).on("click", "img", function(){
        var splitSrc = ($(this).attr('src'));
        var imgName = splitSrc.split("/")[3]
        $( this ).toggleClass( "selectedCard" ); //#TODO: make a border around the cards when selected; right now they are just opaque
        if($.inArray(imgName, possibleSet) == -1){
            possibleSet.push(imgName)
        }
        else{
            possibleSet.remove(imgName)
        }
        if($.inArray($(this), possibleSetSrc) == -1){
            possibleSetSrc.push($(this))
        }
        else{
            possibleSetSrc.remove($(this))
        }
        console.log("src")
        console.log(possibleSetSrc)
        console.log(possibleSet)
        console.log(possibleSet.length)
        if(possibleSet.length == 3){
            console.log("it is three")
            //check if valid set
            var isSet = check_set(possibleSet, possibleSetSrc)
            possibleSet = []
            possibleSetSrc = []
        }
        if(deckSize == 0 && !check_set_in_hand(gameHand)){
            alert("Game over!")
        }
    });

    $(document).on("click", "#deal", function(){
        //check if there was a set in gameHand. If there was a point is deducted. If not, three more cards are added to gameHand
        if(deckSize > 0){
            console.log("more cards to deal")
            console.log(deckSize)
            check_set_in_hand(gameHand)
        }
        else {
            alert("Game over!")
        }
    })

});