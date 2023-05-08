import { connect as _connect } from "mongodb";
const url = 'mongodb://localhost:27017/';
const databasename = "Trixie";  // Database name
_connect(url).then((client) => {

    const connect = client.db(databasename);

    // Connect to collection
    const collection = connect
        .collection("InterviewQuestions");

    // Fetching the records having 
    // name as saini
    collection.find({ "_id": job })
        .toArray().then((ans) => {
            console.log(ans);
        });
}).catch((err) => {

    // Printing the error message
    console.log(err.Message);
})

console.log(job)

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