import {Chess, SQUARES} from '/front_end_deps/chess.js-0.13.4/chess.js'

let chess = new Chess();
const move_list = document.getElementById("move_list");
const fen = document.getElementById("fen");
let from_square = null;
const piece_dir = "/front_end_deps/pieces/"
const pieces = {
    "K": "Chess_klt45.svg",
    "Q": "Chess_qlt45.svg",
    "R": "Chess_rlt45.svg",
    "B": "Chess_blt45.svg",
    "N": "Chess_nlt45.svg",
    "P": "Chess_plt45.svg",
    "k": "Chess_kdt45.svg",
    "q": "Chess_qdt45.svg",
    "r": "Chess_rdt45.svg",
    "b": "Chess_bdt45.svg",
    "n": "Chess_ndt45.svg",
    "p": "Chess_pdt45.svg",
}

function draw_board(){
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const square = 8*i + j;
            const img = document.getElementById("work_board_" + square);
            if ((i + j) % 2 == 0) {
                if (square == from_square) {
                    img.setAttribute("background-color", "yellow");
                } else {
                    context.fillStyle = "white";
                }
                context.fillRect(1 + 32*j, 1 + 32*i, 30, 30);
            } else if (square == from_square) {
                context.fillStyle = "aqua";
                context.fillRect(1 + 32*j, 1 + 32*i, 30, 30);
            }
            const piece = chess.get(SQUARES[square]);
            if (piece != undefined) {
                context.fillStyle = "black";
                context.fillText(piece_character(piece), 4 + 32*j, 26 + 32*i, 28);
            }
        }
    }
    move_list.innerHTML = chess.pgn();
    fen.setAttribute("value", chess.fen());
}

function calc_scale() {
    const dimension = Math.min(window.innerHeight*0.75, window.innerWidth*0.75);
    for (let i=0; i<64; i++) {
        const img = document.getElementById("work_board_" + i);
        img.setAttribute("width", dimension / 8);
        img.setAttribute("height", dimension / 8);
    }
    move_list.style.height = dimension + 'px';
    fen.style.width = dimension + 'px';
    draw_board();
}

function piece_character(piece) {
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
        let square = 8*row + column;
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
        let move = {from: SQUARES[from_square], to: SQUARES[square]};
        const from_piece = chess.get(SQUARES[from_square])
        if (from_piece.type == "p") {
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
document.getElementById("work_board_back").addEventListener(
    "click",
    () => {chess.undo(); calc_scale();}
)
