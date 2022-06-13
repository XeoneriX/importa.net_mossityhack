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
        printToTable(json);
        printCatHead()
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

function clearCatTable() {
    var table = document.getElementById("categories_list");
    table.innerHTML = '';
}

function printDownloadBtn() {
    document.getElementById('download_btn').style.visibility = 'visible'
}

function printCatHead() {
    document.getElementById('cat_head').style.visibility = 'visible'
}
function hideCatHead() {
    document.getElementById('cat_head').style.visibility = 'hidden'
}


function OBJtoCSV(json) {
    var fields = Object.keys(json[0])
    delete fields[3];
    console.log(fields); 
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
    data = OBJtoCSV(downloaded_data)
    console.log(data);
    var bb = new Blob(["\ufeff", data], { type: 'text/plain' });
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(bb);
    a.download = 'Отчёт.csv';
    a.click();
}
