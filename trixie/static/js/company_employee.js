$(document).ready(function () {
    var elem = document.getElementsByTagName("header")[0]
    var elem1 = document.getElementsByTagName("footer")[0]
    var elem2 = document.getElementsByTagName("body")[0]
    elem2.style.marginTop = '0px'
    elem.remove();
    elem1.remove();
});

var password = document.getElementById("floatingPassword")
    , confirm_password = document.getElementById("floatingPasswordConfirm");

function validatePassword() {
    if (password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Passwords Don't Match");
    } else {
        confirm_password.setCustomValidity('');
    }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;