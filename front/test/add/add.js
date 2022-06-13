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

function setTypeDefault() {
    var formData = new FormData(document.forms.default_form);
    formData.append("type", "default");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:3000/login");
    xhr.send(formData);
}
function setTypeAuto() {
    var formData = new FormData(document.forms.auto_form);
    formData.append("type", "auto");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:3000/login");
    xhr.send(formData);
}
function setTypeParser() {
    var formData = new FormData(document.forms.parser_form);
    formData.append("type", "parser");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:3000/login");
    xhr.send(formData);
}
