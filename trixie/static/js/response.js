var que = JSON.parse(questions);
function getBotResponse(input) {
    //rock paper scissors
    console.log("Text you entered", input)
    $.ajax({
        url: "/interview_answer",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({"answer":input}, null, '\t'),
        // success: function (data) {
        //     console.log(data.value)
        // },
        // error: function () {
        //     console.log('Error')
        // }
    });
    for(let i = 0;i < que.length;i++){
        if (input){
            console.log("Inside if", que.length)
            return que[i] && que.shift()
        }
    }
    // if (input == "rock") {
    //     return "paper";
    // } else if (input == "paper") {
    //     return "scissors";
    // } else if (input == "scissors") {
    //     return "rock";
    // }

    // Simple responses
    if (input == "hello") {
        return "Hello there!";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else {
        return "Try asking something else!";
    }
}