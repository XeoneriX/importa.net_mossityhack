downloaded_data = ''

async function search() {
    data = document.getElementById('search_input').value

    let obj = {
        "search": data
    }

    response = await postRequestJson('http://148.253.62.46:8080/okved/search_category', obj)
    if (response.ok) { 
        let json = await response.json();
        downloaded_data = json
        clearCatTable();
        printCatHead()
        clearCompTable();
        printToTable(json);
        printSerachCompBtn();
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
    
}


async function searchComp() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]'); // сбор данных отмеченых категорий
    let data = Array.from(checkboxes) 
    .map(elem => {if (elem.checked) return elem.value})
    .filter(elem => elem) 

    response = await postRequestJson('http://148.253.62.46:8080/okved/search_company', data) 

    if (response.ok) { 
        let json = await response.json();
        downloaded_data = json
        clearCompTable();
        printCopmTableHead(json.heading)
        printCopmTableBody(json.heading, json.body)
        printDownloadBtn()
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

async function postRequestJson(url, data) {
    
    let response = await fetch(url, {
        method: 'POST', 
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    // let response = await fetch('http://148.253.62.46:8080/okved/list_category'); //test
    // let response = await fetch('http://localhost:3000/'+url); //test
    return response
}



function printToTable(json) {
    var table = document.getElementById("categories_list");

    heading = ["Number", "CategoryName", "Count"]
    for (var i = 0; i < json.length; i++) {
        tr = document.createElement("tr");

        td_check = document.createElement("td") // создаю чекбокс
        td_check.innerHTML = '<input type="checkbox" name="cat_num" value="' + json[i].Number + '" onchange="checkTR(this)"/>';
        tr.appendChild(td_check);

        for (var j = 0; j < Object.keys(json[i]).length; j++) {
            if (Object.keys(json[i])[j] != 'Subcategories') {
                td = document.createElement("td");
                td.innerHTML = json[i][heading[j]]
                tr.appendChild(td)
            }
        }
        table.appendChild(tr);

        if (json[i].Subcategories) { // рекурсия
            printToTable(json[i].Subcategories)
        }
    }
}

function printCopmTableHead(data) {
    table_head = document.getElementById('comp_list_head')
    tr = document.createElement("tr");
    var width_col = ["190","600","300","275"] // TO DO
    for (var i = 0; i < data.length; i++) {
        th = document.createElement("th");
        th.innerHTML = data[i]
        th.setAttribute('width', width_col[i])
        tr.appendChild(th)
    }
    table_head.appendChild(tr)
}

function printCopmTableBody(heading ,data) {
    table_body = document.getElementById('comp_list_body')
    table_head = document.getElementById('comp_list_head')
    for (var i = 0; i < data.length; i++) {
        tr = document.createElement("tr")
        for (var j = 0; j < Object.keys(data[i]).length; j++) {
            td = document.createElement("td");
            td.innerHTML = data[i][heading[j]]
            tr.appendChild(td)
        }
        table_body.appendChild(tr)
    }
}



function clearCompTable() {
    let table = document.getElementById('comp_list_table')
    table.innerHTML = '<thead id="comp_list_head"></thead><tbody id="comp_list_body"></tbody>'
    hideDownloadBtn();
}

function clearCatTable() {
    var table = document.getElementById("categories_list");
    table.innerHTML = '';
}



function printSerachCompBtn() {
    document.getElementById('searchComp_btn').style.visibility='visible'
}
function printDownloadBtn() {
    document.getElementById('download_btn').style.visibility = 'visible'
}
function hideDownloadBtn() {
    document.getElementById('download_btn').style.visibility = 'hidden'
}

function printCatHead() {
    document.getElementById('cat_head').style.visibility = 'visible'
}
function hideCatHead() {
    document.getElementById('cat_head').style.visibility = 'hidden'
}



function checkTR(element) {
    if (element.checked) {
        element.closest('tr').style.backgroundColor='#C3CFE2'
    } else {
        element.closest('tr').style.backgroundColor='#E9F1FE'
    }
}

function OBJtoCSV(json) {
    var fields = Object.keys(json[0])
    var replacer = function(key, value) { return value === null ? '' : value } 
    var csv = json.map(function(row){
        return fields.map(function(fieldName){
            return JSON.stringify(row[fieldName], replacer)
        }).join(';')
    })
    csv.unshift(fields.join(';')) // добавляет heading
    csv = csv.join('\r\n');
    return csv
}


function downloadData() {
    data = OBJtoCSV(downloaded_data.body)
    console.log(data);
    var bb = new Blob(["\ufeff", data], { type: 'text/plain' });
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(bb);
    a.download = 'Отчёт.csv';
    a.click();
}

