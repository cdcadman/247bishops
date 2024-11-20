import {Chess} from '/front_end_deps/chess.js-0.13.4/chess.js'

let chess = new Chess();
const canvas = document.getElementById("work_board_canvas");
const context = canvas.getContext("2d");
let scaleFactor = 1;
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
            const piece = piece_on_square(square);
            if (piece != undefined) {
                context.fillStyle = "black";
                context.fillText(piece, 4 + 32*j, 26 + 32*i, 28);
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

function piece_on_square(square) {
    const piece = chess.get(square_name(square));
    if (piece == undefined) {
        return undefined;
    }
    if (piece.color == "b") {
        return pieces[piece.type];
    } else {
        return pieces[piece.type.toUpperCase()];
    }
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
        let move = {from: square_name(from_square), to: square_name(square)};
        const from_piece = piece_on_square(from_square)
        if (from_piece == pieces["P"] || from_piece == pieces["p"]) {
            if (row == 7 || row == 0) {
                move["promotion"] = window.prompt("Promotion piece (q, r, b, or n)?");
            }
        }
        chess.move(move);
        from_square = null;
        calc_scale();
    }
}

window.addEventListener("resize", calc_scale);
canvas.addEventListener("click", handle_click);
window.addEventListener("load", (event) => {calc_scale();})
