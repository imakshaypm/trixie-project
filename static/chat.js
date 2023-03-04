//Requesting permission from chrome to access webcam
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

$(document).ready(function () {
    $('#start-meeting').click(function () {
        var localstream;
        function startVideo() {
            navigator.getUserMedia({
                video: {} },
                function(stream){
                    video.srcObject = stream
                    localstream = stream;
                    console.log(localstream)
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
            //Fetching Video frame from HTML
            const video = document.getElementById("video");
            /****Loading the model ****/
            Promise.all([
                faceapi.nets.tinyFaceDetector.loadFromUri("/static/models/"),
                faceapi.nets.faceLandmark68Net.loadFromUri("/static/models/"),
                faceapi.nets.faceRecognitionNet.loadFromUri("/static/models/"),
                faceapi.nets.faceExpressionNet.loadFromUri("/static/models/"),
                faceapi.nets.ageGenderNet.loadFromUri("/static/models/")
            ]).then(startVideo);


            /****Event Listeiner for the video****/
            video.addEventListener("playing", () => {
                const canvas = faceapi.createCanvasFromMedia(video);
                let container = document.querySelector(".container");
                container.append(canvas);

                const displaySize = { width: video.width, height: video.height };
                faceapi.matchDimensions(canvas, displaySize);

                setInterval(async () => {
                    const detections = await faceapi
                        .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())
                        .withFaceLandmarks()
                        .withFaceExpressions()
                        .withAgeAndGender();

                    const resizedDetections = faceapi.resizeResults(detections, displaySize);
                    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

                    /****Drawing the detection box and landmarkes on canvas****/
                    /*faceapi.draw.drawDetections(canvas, resizedDetections);
                    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

                    /****Setting values to the DOM****/
                    if (resizedDetections && Object.keys(resizedDetections).length > 0) {
                        const gender = resizedDetections.gender;
                        const expressions = resizedDetections.expressions;
                        const maxValue = Math.max(...Object.values(expressions));
                        const emotion = Object.keys(expressions).filter(
                            item => expressions[item] === maxValue
                        );
                        document.getElementById("gender").innerText = `Gender - ${gender}`;
                        document.getElementById("emotion").innerText = `Emotion - ${emotion[0]}`;
                    }
                }, 10);
            });

        }else{
            document.getElementById("start-meeting").value = "Start Meeting"
            document.getElementById("start-meeting").style.background = "#043665"
            cameraoff()
        }
    })
});

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


/*function getResponse() {
    let userText = $("#textInput").val();

    if(userText == "") {
        userText = "I love Code Palace!";
    }

    let userHtml = '<p class="userText"><span>' + userText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById('chatbox').scrollIntoView({ block: "nearest", inline: "nearest" });

    setTimeout(() => {
        getHardRespose(userText);
    }, 1000)
}

function sendButton() {
    getResponse();
}*/

// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});