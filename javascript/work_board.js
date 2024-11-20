const canvas = document.getElementById("work_board_canvas");
const context = canvas.getContext("2d");
const orig_font = context.font;
let scaleFactor = 1;
let board = {
    0: "R", 1: "N", 2: "B", 3: "Q", 4: "K", 5: "B", 6: "N", 7: "R", 8: "P", 9: "P", 10: "P", 11: "P", 12: "P", 13: "P", 14: "P", 15: "P",
    63: "r", 62: "n", 61: "b", 60: "k", 59: "q", 58: "b", 57: "n", 56: "r", 55: "p", 54: "p", 53: "p", 52: "p", 51: "p", 50: "p", 49: "p", 48: "p"
};
let move_number = 0; // This is ply - it increments by one for each white and black move.
let last_move_square = null;
let from_square = null;
const pieces = {
    "K": "\u2654",
    "Q": "\u2655",
    "R": "\u2656",
    "B": "\u2657",
    "N": "\u2658",
    "P": "\u2659",
    "k": "\u265A",
    "q": "\u265B",
    "r": "\u265C",
    "b": "\u265D",
    "n": "\u265E",
    "p": "\u265F",
}

function draw_board(){
    for (let x = 0; x <= 256; x += 32) {
        context.moveTo(x, 0);
        context.lineTo(x, 256);
    }

    for (let x = 0; x <=256; x += 32) {
        context.moveTo(0, x);
        context.lineTo(256, x);
    }
    context.strokeStyle = "black";
    context.font = "30px FreeSerif";
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            let square = 8*(7 - i) + j;
            let highlight_square = last_move_square;
            if (from_square != null) {
                highlight_square = from_square;
            }
            if ((i + j) % 2 == 0) {
                if (square == highlight_square) {
                    context.fillStyle = "yellow";
                } else {
                    context.fillStyle = "white";
                }
                context.fillRect(1 + 32*j, 1 + 32*i, 30, 30);
            } else if (square == highlight_square) {
                context.fillStyle = "aqua";
                context.fillRect(1 + 32*j, 1 + 32*i, 30, 30);
            }
            if (board[square] != undefined) {
                context.fillStyle = "black";
                context.fillText(pieces[board[square]], 4 + 32*j, 26 + 32*i, 28);
            }
        }
    }
}

function calc_scale() {
    const dimension = Math.min(window.innerHeight*0.75, window.innerWidth*0.75);
    scaleFactor = dimension / 256;
    canvas.setAttribute("width", dimension);
    canvas.setAttribute("height", dimension);
    context.scale(scaleFactor, scaleFactor);
    draw_board();
}

function square_name(square) {
    const column = square % 8;
    const row = (square - column) / 8;
    return String.fromCharCode(97 + column) + String.fromCharCode(49 + row);
}

function handle_click(event) {
    const scaleX = event.offsetX / scaleFactor;
    const scaleY = event.offsetY / scaleFactor;
    const column = Math.floor(scaleX / 32);
    const row = Math.floor(scaleY / 32);
    if (row >= 0 && row <= 7 && column >= 0 && column <= 7) {
        let square = 8*(7 - row) + column;
        if (from_square == null) {
            from_square = square;
            calc_scale();
            return;
        }
        if (from_square == square) {
            from_square = null;
            calc_scale();
            return;
        }
        context.fillStyle = "black";
        context.fillText(pieces[board[from_square]], 4 + 32*column, 26 + 32*row, 28);
        promote = "";
        if (board[from_square] == "P" || board[from_square] == "p") {
            if (row == 7 || row == 0) {
                promote = window.prompt("Promotion piece (q, r, b, or n)?");
            }
        }
        uci = square_name(from_square) + square_name(square) + promote;
        from_square = null;
    }
}

window.addEventListener("resize", calc_scale);
canvas.addEventListener("click", handle_click);
window.addEventListener("load", (event) => {calc_scale();})
