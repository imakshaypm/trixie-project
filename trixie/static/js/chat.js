var que = JSON.parse(questions);
var job_id = JSON.parse(job_id);
var round = JSON.parse(round);
function getBotResponse(input) {
    console.log("Text you entered", input)
    if( round === "First Round"){
        $.ajax({
            url: "/interview_keyword",
            type: "POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({ "answer": input }, null, '\t'),
        });
    }
    for (let i = 0; i < que.length; i++) {
        if (input) {
            return que[i] && que.shift()
        }
    }
    if (que.length === 0 && round == "First Round") {
        document.getElementById("start-meeting").value = "Go to Second Round"
        document.getElementById("start-meeting").style.background = "#32CD32"
    }else{
        document.getElementById("start-meeting").value = "Finish Meeting"
        document.getElementById("start-meeting").style.background = "#32CD32"
    }

    // Simple responses
    if (input == "hello") {
        return "Hello there!";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else {
        if (round == "First Round") {
            return "Round One is completed click on the button to go to second round!";
        }else{
            return "Round Two is completed click on the button to go to end the interview!";
        }
    }
}

$('#start-meeting').click(function () {
    console.log("Outside the button condition")
    if (document.getElementById("start-meeting").value === "Go to Second Round") {
        window.location.href = '/interview_second/' + job_id;
    }
    if (document.getElementById("start-meeting").value === "Finish Meeting") {
        window.location.href = '/interview_finish/' + job_id;
    }
});

//Requesting permission from chrome to access webcam
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
$(document).ready(function () {
    var myInterval = null
    $('#start-meeting').click(function () {
        var localstream;
        function startVideo() {
            myInterval = setInterval(imageFetching, 10000)
            navigator.getUserMedia({
                video: {} },
                function(stream){
                    video.srcObject = stream
                    localstream = stream;
                },
                function(error){
                    console.error(error)
                }
            );
        }
        function cameraoff() {
            const stream = video.srcObject;
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(function (track) {
                    track.stop();
                });
                video.srcObject = null;
            }
        }


        if (document.getElementById("start-meeting").value == "Start Meeting" && round == 'First Round') {
            $('#myModal').modal('show');
            $("#accept").click(function () {
                document.getElementById("start-meeting").value = "Stop Meeting"
                document.getElementById("start-meeting").style.background = "#F1414F";
                document.getElementById("mic-icon").className = "bi bi-mic-mute-fill"
                document.getElementById("mic-button").style.background = "#F1414F"
                startVideo()
                cheack()
                $('#myModal').modal('toggle');
            });
        }else if (document.getElementById("start-meeting").value == "Start Meeting" && round == 'Second Round') {
            document.getElementById("start-meeting").value = "Stop Meeting"
            document.getElementById("start-meeting").style.background = "#F1414F";
            document.getElementById("mic-icon").className = "bi bi-mic-mute-fill"
            document.getElementById("mic-button").style.background = "#F1414F"
            startVideo()
            cheack()
        }else{
            clearInterval(myInterval);
            document.getElementById("start-meeting").value = "Start Meeting"
            document.getElementById("start-meeting").style.background = "#043665"
            document.getElementById("mic-icon").className = "bi bi-mic-fill"
            document.getElementById("mic-button").style.background = "#043665"
            cameraoff()
            cheack()
        }
    })
});

//Fetching Video frame from HTML
function imageFetching() {
    const video = document.getElementById("video");
    const canvas = document.createElement("canvas");
    // scale the canvas accordingly
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    // draw the video at that frame
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    // convert it to a usable data URL
    let dataURL = canvas.toDataURL("image/png");
    dataURL = dataURL.replace('data:image/png;base64,','')
    $.ajax({
        url: "/interview_reaction",
        type: "POST",
        // contentType: "application/json; charset=utf-8",
        data: { round : round, imageBase64: dataURL },
        // success: function (data) {
        //     console.log(data.value)
        // },
        // error: function () {
        //     console.log('Error')
        // }
    });
}



/*$.ajax({
    url: "/interview",
    type: "POST",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({
        clicked: true
    }),
    success: function (data) {
        console.log(data.value)
    },
    error: function () {
        console.log('Error')
    }
});*/

//DONT EVER TOUCH THIS SECTION OF CODE.
//##
var recognition = null
function cheack(){
    init()
    if (document.getElementById("mic-icon").className === "bi bi-mic-mute-fill") {
        document.getElementById("mic-icon").className = "bi bi-mic-fill"
        document.getElementById("mic-button").style.background = "#043665"
        window.SpeechRecognition = window.webkitSpeechRecognition;
        recognition = new window.SpeechRecognition();
        recognition.lang = "en-IN";
        if ('SpeechRecognition' in window) {
            console.log('supported speech')
        } else {
            console.error('speech not supported')
        }
        recognition.continuous = true;
        recognition.start()
        recognition.onstart = () => {
            console.log("Started")
        }
        recognition.onresult = (event) => {
            UserText = event.results[event.results.length - 1][0].transcript
            let userHtml = '<p class="userText"><span>' + UserText + '</span></p>';
            $("#chatbox").append(userHtml);
            var objDiv = document.getElementById("chatbox");
            objDiv.scrollTop = objDiv.scrollHeight;
            setTimeout(() => {
                getHardRespose(UserText.trim());
            }, 1000)
            //document.getElementById('textInput').value = event.results[event.results.length - 1][0].transcript
            console.log('transscript: ', UserText);
        }
    } else {
        document.getElementById("mic-icon").className = "bi bi-mic-mute-fill"
        document.getElementById("mic-button").style.background = "#F1414F"
        console.log("Else")
        recognition.stop();
        recognition.onresult = function (event) {
            if (typeof (event.results) == 'undefined') {
                recognition.onend = null;
                recognition.stop();
                upgrade();
                return;
            }
        }
    }
}
//##

function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if(hours < 10) {
        hours = '0' + hours;
    }

    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    let time = hours + ':' + minutes;
    return time;
}

function firstBotMessage() {
    let firstMessage
    if (round == 'First Round'){
        firstMessage = "If you are ready you can start the first round by saying hello after clicking start meeting button."
    }else{
        firstMessage = "If you are ready you can start the second round by saying hello after clicking start meeting button."
    }
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>'

    let time = getTime();

    $("#chat-timestamp").append(time);
    //document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

function getHardRespose(userText) {
    let botResponse = getBotResponse(userText);
    let botHtml = '<p class="botText"><span>' + botResponse + '</span></p>';

    $("#chatbox").append(botHtml);
    var objDiv = document.getElementById("chatbox");
    objDiv.scrollTop = objDiv.scrollHeight;
}

// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});