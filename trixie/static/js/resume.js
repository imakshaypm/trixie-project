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
        var fileName = document.getElementById("files").value;
        var idxDot = fileName.lastIndexOf(".") + 1;
        var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
        if (extFile == "doc" || extFile == "docx") {
            //TO DO
        } else {
            alert("Only doc/docx and png files are allowed!");
        }
    })
});

let fileInput = document.getElementById("files");
let fileList = document.getElementById("files-list");
let numOfFiles = document.getElementById("num-of-files");
fileInput.addEventListener("change", () => {
    fileList.innerHTML = "";
    numOfFiles.textContent = `${fileInput.files.length} Files Selected`;
    for (i of fileInput.files) {
        let reader = new FileReader();
        let listItem = document.createElement("li");
        let fileName = i.name;
        let fileSize = (i.size / 1024).toFixed(1);
        listItem.innerHTML = `<p>${fileName}</p><p>${fileSize}KB</p>`;
        if (fileSize >= 1024) {
            fileSize = (fileSize / 1024).toFixed(1);
            listItem.innerHTML = `<p>${fileName}</p><p>${fileSize}MB</p>`;
        }
        fileList.appendChild(listItem);
    }
});
$(function () {
    // setTimeout() function will be fired after page is loaded
    // it will wait for 5 sec. and then will fire
    // $(".message_flash").hide() function
    setTimeout(function () {
        $(".message_flash").hide('blind', {}, 500)
    }, 5000);
})   