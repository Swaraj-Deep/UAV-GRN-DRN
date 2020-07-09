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

function init() {
    x = [];
    y = [];
    col = [];
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

var i = 0, j = 1;
var row_lst = [];

function create_grid(event) {
    rows = document.getElementById('rows').value;
    // cols = document.getElementById('cols').value;
    if (!rows) {
        showalert(`Please enter a valid number.`, `danger`);
        return;
    } else {
        init();
        if (rows > 30) {
            showalert(`Very large value entered. Splitting into subgrids.`, `secondary`);
            large = true;
            i = 0, j = 1;
            row_lst = [];
            set_row_list(rows);
            return false;
        }
        cols = rows;
    }
    setup();
    document.getElementById('submit_btn').hidden = false;
}

function load_subgrid() {
    if (!large) {
        showalert(`No subgrid to load.`, `danger`);
    } else {
        num_rows = rows;
        if (row_lst[j + 1] == num_rows && row_lst[i + 1] == num_rows) {
            cols = Math.abs (row_lst[j + 1] - row_lst[j]);
            rows = Math.abs (row_lst[i + 1] - row_lst[i]);
        } else if (row_lst[j + 1] == num_rows) {
            cols = Math.abs (row_lst[j + 1] - row_lst[j]);
            rows = 30;
        } else if (row_lst[i + 1] == num_rows) {
            cols = 30;
            rows = Math.abs (row_lst[i + 1] - row_lst[i]);
        } else {
            rows = 30;
            cols = 30;
        }
        console.log (rows, cols);
    }
}

function save_config() {
    if (large) {
        if (i == row_lst.length - 1) {
            return;
        }
        if (j == row_lst.length - 1) {
            j = 1;
            i++;
        } else {
            j++;
        }
    }
}

function set_row_list(rows) {
    var row = 0;
    while (row <= rows) {
        row_lst.push(row);
        row += 30;
    }
    if (row != rows) {
        row = rows;
        row_lst.push(row);
    }
}
