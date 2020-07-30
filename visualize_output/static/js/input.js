var rows;
var cols;
var UAV_location;
var radius_UAV;
var w = 20;
var col = [];
var edges = [];
var start_drawing = false;
var user_location = [];


function showalert(message, alert_type) {
    $("#alert-wrapper").html(`<div class="alert alert-${alert_type} alert-dismissible fade show" role="alert" id="alertdialog">
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        </button>
        </div>`);
    window.setTimeout(function () { $("#alertdialog").alert('close'); }, 2000);
    document.getElementById("alertdialog").scrollIntoView();
}

function sendresponse(url, data) {
    return fetch(`${window.origin}/${url}`, {
        method: "POST",
        credentials: "include",
        body: data,
        cache: "no-cache"
    });
}

document.getElementById('file_input').addEventListener('change', function (event) {
    let files = event.target.files;
    if (files[0].type !== 'application/json') {
        showalert(`Please choose only json files.`, `danger`);
        document.getElementById('file_input_label').innerHTML = `Select File`;
        return false;
    }
    document.getElementById('file_input_label').innerHTML = files[0].name;
});


$('#upload_btn').on({
    click: function () {
        var fileUpload = $("#file_input").get(0);
        const files = fileUpload.files[0];
        if (files === undefined) {
            showalert(`Select a file first.`, `danger`);
            return false;
        }
        const file = new FormData();
        file.append("file", files, files.filename);
        sendresponse('__verify_upload__', file).then(function (response) {
            if (response.status !== 200) {
                showalert(`Could not save the file. Please try after some time.`, `danger`);
            } else if (response.status === 200) {
                response.json().then(function (data) {
                    rows = data['Data']['N'];
                    cols = data['Data']['M'];
                    radius_UAV = data['Data']['radius_UAV'];
                    edges = data['Data']['edge_UAV'];
                    UAV_location = data['Data']['UAV_location'];
                    user_location = data['Data']['user_loc'];
                    document.getElementById('user_served').innerHTML = `Total Number of user served: ${data['Data']['gusers'].length} <br>Total Number of UAV used: ${Object.keys (UAV_location)['length']}`
                    var canvasid = document.getElementById('canvas1');
                    if (canvasid) {
                        document.getElementById('grid').removeChild(canvasid);
                        var table = document.getElementById('tableDesc');
                        table.innerHTML = "";
                        table.innerHTML = `<thead>
                                               <tr>
                                                   <th scope="col">UAV</th>
                                                   <th scope="col">Users Served</th>
                                               </tr>
                                           </thead>
                                           <tbody>
                                               <tr>
                           
                                               </tr>
                                           </tbody>`;
                    }
                    startSketch();
                    console.log (data);
                    document.getElementById('tableDesc').style.display = 'block';
                    createTable(data);
                });
            } else if (response.status === 500) {
                showalert(`Opps! It's our fault.`, `danger`);
            }
        });
    }
});

// Drawing Function

function startSketch() {
    var sketch = function (p) {
        init();
        p.setup = function () {
            var cnv = p.createCanvas(500, 500);
            cnv.id('canvas1');
            p.background(255);
            cnv.parent('grid');
            for (var i = 0; i < rows; ++i) {
                col[i] = new Array(cols);
                for (var j = 0; j < cols; ++j) {
                    col[i][j] = { 'group': 1, 'UAV': null, 'user': null };
                }
            }
            for (var i in UAV_location) {
                var x = UAV_location[i][0];
                var y = UAV_location[i][1];
                col[x][y] = { 'group': 2, 'UAV': i, 'user': null };
            }
            for (var i in user_location) {
                var x = user_location[i][0];
                var y = user_location[i][1];
                var gp = col[x][y]['group'];
                if (gp == 2) {
                    col[x][y]['group'] = 3;
                } else {
                    col[x][y] = { 'group': 4, 'UAV': null, 'user': i };
                }
            }
        };
        p.draw = function () {
            p.rectMode(p.CENTER);
            p.stroke(0);
            for (var i in col) {
                for (var j in col[i]) {
                    if (col[i][j]['group'] == 1) {
                        p.fill("white");
                        p.rect(w + j * w, w + i * w, w, w);
                    } else if (col[i][j]['group'] == 2) {
                        p.fill('red');
                        p.textAlign(p.CENTER, p.CENTER);
                        p.rect(w + j * w, w + i * w, w, w);
                        p.fill('black');
                        p.text(`${col[i][j]['UAV']}`, w + j * w, w + i * w);
                    } else if (col[i][j]['group'] == 3) {
                        p.fill('blue');
                        p.textAlign(p.CENTER, p.CENTER);
                        p.rect(w + j * w, w + i * w, w, w);
                        p.fill('white');
                        p.text(`${col[i][j]['UAV']}`, w + j * w, w + i * w);
                    } else if (col[i][j]['group'] == 4) {
                        p.fill('black');
                        p.textAlign(p.CENTER, p.CENTER);
                        p.rect(w + j * w, w + i * w, w, w);
                        p.fill('white');
                        p.text(`${col[i][j]['user']}`, w + j * w, w + i * w);
                    }
                }
            }
            for (var i in UAV_location) {
                var x = UAV_location[i][0];
                var y = UAV_location[i][1];
                p.fill(0, 0, 0, 13);
                p.circle(w + y * w, w + x * w, radius_UAV * w * 2.1);
            }
            for (var i in edges) {
                var x = edges[i][0];
                var y = edges[i][1];
                var locx = UAV_location[x];
                var x1 = locx[0];
                var y1 = locx[1];
                var locy = UAV_location[y];
                var x2 = locy[0];
                var y2 = locy[1];
                p.strokeWeight(3);
                p.stroke(0, 0, 255, 100)
                p.line(w + y1 * w, w + x1 * w, w + y2 * w, w + x2 * w);
            }
            p.noLoop();
        };
    };
    var myp5 = new p5(sketch);
    myp5 = null;
}

function init() {
    col = [];
}

function createTable(data) {
    var user_served = data['Data']['UAV_serves'];
    var tableRef = document.getElementById('tableDesc').getElementsByTagName('tbody')[0];
    for (var i in user_served) {
        var newRow = tableRef.insertRow();
        var users = ``;
        for (var j in user_served[i]) {
            users += `${user_served[i][j]}, `;
        }
        var UAV = newRow.insertCell(0);
        var user = newRow.insertCell(1);
        var text = document.createTextNode(`${i}`);
        UAV.appendChild (text);
        text = document.createTextNode(`${users}`);
        user.appendChild(text);
    }
}
