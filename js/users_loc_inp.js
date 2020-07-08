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
    var cnv = createCanvas(800, 800);
    cnv.parent('grid');
    for (var i = 0; i < rows; i++) {
        x[i] = w + i * w;
        y[i] = w + i * w;
    }
    for (var i = 0; i < rows * cols; i++) {
        col[i] = true;
    }

}

function draw() {
    background(255);
    rectMode(CENTER);
    stroke(0);
    for (var j = 0; j < y.length; j++) {
        for (var i = 0; i < cols; i++) {
            if (col[j * rows + i]) {
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
                col[j * rows + i] = !col[j * rows + i];
                if (col[j * rows + i] == false) {
                    console.log(i, j);
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
    var text_inp = document.getElementById('rows').value;
    if (!text_inp) {
        showalert(`Please enter a valid number.`, `danger`);
        return;
    } else {
        rows = text_inp;
        cols = rows;
        if (rows > 30) {
            showalert(`Very large value entered. Splitting into subgrids.`, `secondary`);
            large = true;
            rows = 30
        }
    }
    setup();
    document.getElementById('submit_btn').hidden = false;
}