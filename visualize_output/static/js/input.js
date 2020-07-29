var rows;
var cols;
var UAV_location;
var x = [];
var y = [];
var w = 15;
var col = [];


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
                    rows = data['Data']['N']
                    cols = data['Data']['M']
                    UAV_location = data['Data']['UAV_location']
                    init();
                    setup();
                });
            } else if (response.status === 500) {
                showalert(`Opps! It's our fault.`, `danger`);
            }
        });
    }
});

// Drawing Function

function setup() {
    var cnv = createCanvas(500, 500);
    cnv.parent('grid');
    for (var i = 0; i < rows; ++i) {
        col[i] = new Array(cols);
        for (var j = 0; j < cols; ++j) {
            col[i][j] = 1;
        }
    }
    for (var i = 0; i < rows; i++) {
        y[i] = w + i * w;
    }
    for (var i = 0; i < cols; ++i) {
        x[i] = w + i * w;
    }    
}

function draw() {
    background(255);
    rectMode(CENTER);
    stroke(0);
    for (i in UAV_location) {
        x = UAV_location[i][0]
        y = UAV_location[i][1]
        cols[x][y] = 2;
    }
    for (var j = 0; j < y.length; j++) {
        for (var i = 0; i < cols; i++) {
            if (col[j][i] == 1) {
                fill("white");
            } else if (col[i][j] == 2) {
                fill("red");
            }
            rect(x[i], y[j], w, w);
        }
    }
}

// function mousePressed() {
//     for (var b = 0; b < rows; b++) {
//         for (var a = 0; a < cols; a++) {
//             var dis = dist(mouseX, mouseY, x[a], y[b]);
//             if (dis < w / 2) {
//                 col[b][a] = !col[b][a];
//                 if (col[b][a] == false) {
//                     console.log('hi');
//                 }
//             }
//         }
//     }
// }

function init() {
    x = [];
    y = [];
    col = [];
}



