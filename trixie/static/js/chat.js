var que = JSON.parse(questions);
var job_id = JSON.parse(job_id);
function getBotResponse(input) {
    //rock paper scissors
    console.log("Text you entered", input)
    $.ajax({
        url: "/interview_answer",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ "answer": input }, null, '\t'),
    });
    for (let i = 0; i < que.length; i++) {
        if (input) {
            console.log("Inside if", que.length)
            return que[i] && que.shift()
        }
    }
    if (que.length === 0) {
        document.getElementById("start-meeting").value = "Go to Second Round"
        document.getElementById("start-meeting").style.background = "#32CD32"
        $.ajax({
            url: "/interview_second",
            type: "POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({ "round_1": "completed", 'job_id': job_id }, null, '\t'),
        });
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
                    // console.log(localstream)
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
        if (document.getElementById("start-meeting").value == "Start Meeting") {
            document.getElementById("start-meeting").value = "Stop Meeting"
            document.getElementById("start-meeting").style.background = "#F1414F";
            startVideo()
            /****Loading the model ****/
            // Promise.all([
            //     faceapi.nets.tinyFaceDetector.loadFromUri("/static/models/"),
            //     faceapi.nets.faceLandmark68Net.loadFromUri("/static/models/"),
            //     faceapi.nets.faceRecognitionNet.loadFromUri("/static/models/"),
            //     faceapi.nets.faceExpressionNet.loadFromUri("/static/models/"),
            //     faceapi.nets.ageGenderNet.loadFromUri("/static/models/")
            // ]).then(startVideo);


            // /****Event Listeiner for the video****/
            // video.addEventListener("playing", () => {
            //     const canvas = faceapi.createCanvasFromMedia(video);
            //     let container = document.querySelector(".container");
            //     container.append(canvas);

            //     const displaySize = { width: video.width, height: video.height };
            //     faceapi.matchDimensions(canvas, displaySize);

            //     setInterval(async () => {
            //         const detections = await faceapi
            //             .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())
            //             .withFaceLandmarks()
            //             .withFaceExpressions()
            //             .withAgeAndGender();

            //         const resizedDetections = faceapi.resizeResults(detections, displaySize);
            //         canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

            //         /****Drawing the detection box and landmarkes on canvas****/
            //         /*faceapi.draw.drawDetections(canvas, resizedDetections);
            //         faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

            //         /****Setting values to the DOM****/
            //         if (resizedDetections && Object.keys(resizedDetections).length > 0) {
            //             const gender = resizedDetections.gender;
            //             const expressions = resizedDetections.expressions;
            //             const maxValue = Math.max(...Object.values(expressions));
            //             const emotion = Object.keys(expressions).filter(
            //                 item => expressions[item] === maxValue
            //             );
            //             document.getElementById("gender").innerText = `Gender - ${gender}`;
            //             document.getElementById("emotion").innerText = `Emotion - ${emotion[0]}`;
            //         }
            //     }, 10);
            // });

        }else{
            clearInterval(myInterval);
            document.getElementById("start-meeting").value = "Start Meeting"
            document.getElementById("start-meeting").style.background = "#043665"
            cameraoff()
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
        url: "/interview_answer",
        type: "POST",
        // contentType: "application/json; charset=utf-8",
        data: { imageBase64 : dataURL},
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
    let firstMessage = "How's it going?"
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