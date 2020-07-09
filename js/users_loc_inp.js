var large = false;
var rows;
var cols;
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
}


function setup() {
    var cnv = createCanvas(500, 500);
    cnv.parent('grid');
    for (var i = 0; i < rows; i++) {
        y[i] = w + i * w;
    }
    for (var i = 0; i < cols; ++i) {
        x[i] = w + i * w;
    }
    for (var i = 0; i < rows; ++i) {
        col[i] = new Array(cols);
        for (var j = 0; j < cols; ++j) {
            col[i][j] = true;
        }
    }
}

function draw() {
    background(255);
    rectMode(CENTER);
    stroke(0);
    for (var j = 0; j < y.length; j++) {
        for (var i = 0; i < cols; i++) {
            if (col[j][i]) {
                fill("white");
            } else {
                fill("red");
            }
            rect(x[i], y[j], w, w);
        }
    }
}

function mousePressed() {
    for (var j = 0; j < rows; j++) {
        for (var i = 0; i < cols; i++) {
            var dis = dist(mouseX, mouseY, x[i], y[j]);
            if (dis < w / 2) {
                col[j][i] = !col[j][i];
                if (col[j][i] == false) {
                    console.log(j, i);
                }
            }
        }
    }
}

function validateNum(evt) {
    var theEvent = evt || window.event;
    if (theEvent.type === 'paste') {
        key = event.clipboardData.getData('text/plain');
    } else {
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
    }
    var regex = /[0-9]|\./;
    if (!regex.test(key)) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}

function create_grid(event) {
    rows = document.getElementById('rows').value;
    // cols = document.getElementById('cols').value;
    if (!rows) {
        showalert(`Please enter a valid number.`, `danger`);
        return;
    } else {
        if (rows > 30) {
            showalert(`Very large value entered. Splitting into subgrids.`, `secondary`);
            large = true;
            split_grid(rows);
            return false;
        }
        cols = rows;
    }
    setup();
    document.getElementById('submit_btn').hidden = false;
}

function split_grid(rows) {
    var row = 0;
    var row_lst = [];
    while (row <= rows) {
        row_lst.push (row);
        row += 30;
    }
    if (row != rows) {
        row = rows;
        row_lst.push (row);
    }
    for (var i = 0; i < row_lst.length; ++i) {
        rows = row_lst[i];
        cols = row_lst[1];
        setup();
        // console.log(row_lst[i], row_lst[1]);
        for (var j = 1; j < row_lst.length - 1; ++j) {
            console.log (-(row_lst[j] - row_lst[j + 1]));
        }
    }
}
