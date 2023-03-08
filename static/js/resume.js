(function () {
    // Add event listener
    document.addEventListener("mousemove", parallax);
    const elem = document.querySelector("#parallax");
    // Magic happens here
    function parallax(e) {
        let _w = window.innerWidth / 2;
        let _h = window.innerHeight / 2;
        let _mouseX = e.clientX;
        let _mouseY = e.clientY;
        let _depth1 = `${50 - (_mouseX - _w) * 0.01}% ${50 - (_mouseY - _h) * 0.01}%`;
        let _depth2 = `${50 - (_mouseX - _w) * 0.02}% ${50 - (_mouseY - _h) * 0.02}%`;
        let _depth3 = `${50 - (_mouseX - _w) * 0.06}% ${50 - (_mouseY - _h) * 0.06}%`;
        let x = `${_depth3}, ${_depth2}, ${_depth1}`;
        elem.style.backgroundPosition = x;
    }

})();



$(document).ready(function () {
    $("#upload-file-btn").click(function () {
        var formData = new FormData();
        formData.append('files', $('#files')[0].files[0]);
        console.log(formData)
        $.ajax({
            type: 'POST',
            url: "/resume_result",
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log('Success!');
            },
        });
    })
});