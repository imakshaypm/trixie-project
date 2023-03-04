function getBotResponse(input) {
    //rock paper scissors
    console.log("Text you entered", input)
    $.ajax({
        url: "/interview",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            inputs: input
        }),
        success: function (data) {
            console.log(data.value)
        },
        error: function () {
            console.log('Error')
        }
    });
    if (input == "rock") {
        return "paper";
    } else if (input == "paper") {
        return "scissors";
    } else if (input == "scissors") {
        return "rock";
    }

    // Simple responses
    if (input == "hello") {
        return "Hello there!";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else {
        return "Try asking something else!";
    }
}