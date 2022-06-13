function showDefault() {
    document.getElementById('default_add').style.visibility = "visible";
    document.getElementById("default_btn").classList.add("active");

    document.getElementById('auto_add').style.visibility = "hidden";
    document.getElementById("auto_btn").classList.remove("active");

    document.getElementById('parser_add').style.visibility = "hidden";
    document.getElementById("parser_btn").classList.remove("active");

}
function showAuto() {
    document.getElementById('default_add').style.visibility = "hidden";
    document.getElementById("default_btn").classList.remove("active");

    document.getElementById('auto_add').style.visibility = "visible";
    document.getElementById("auto_btn").classList.add("active");

    document.getElementById('parser_add').style.visibility = "hidden";
    document.getElementById("parser_btn").classList.remove("active");
}

function showParser() {
    document.getElementById('default_add').style.visibility = "hidden";
    document.getElementById("default_btn").classList.remove("active");

    document.getElementById('auto_add').style.visibility = "hidden";
    document.getElementById("auto_btn").classList.remove("active");

    document.getElementById('parser_add').style.visibility = "visible";
    document.getElementById("parser_btn").classList.add("active");
}

function startTimer() {                                                         // ожидание ответа от сервера
    document.getElementById('safeTimer').style.visibility = "visible"
    var sec = 5;
    var timer = setInterval(function(){
        document.getElementById('safeTimerDisplay').innerHTML='00:0'+sec;
        sec--;
        if (sec < 0) {
            clearInterval(timer);                                               // после ответа от сервера переходим по той ссылке
            window.location.href='/test/add/add.html'                           // которую получили от него
        }
    }, 1000)
}
