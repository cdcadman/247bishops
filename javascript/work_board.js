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

for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
        const square = 8*i + j;
        const img = document.getElementById("work_board_" + square);
        if ((i + j) % 2 == 0) {
            img.classList.add("light");
        } else {
            img.classList.add("dark");
        }
    }
}

function draw_board(){
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const square = 8*i + j;
            const img = document.getElementById("work_board_" + square);
            if (square == from_square) {
                img.classList.add("from");
            } else {
                img.classList.remove("from");
            }
            const piece = chess.get(SQUARES[square]);
            img.setAttribute("src", piece_url(piece));
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

function piece_url(piece) {
    if (piece == undefined) {
        return "/images/blank.png";
    } else if (piece.color == "b") {
        return piece_dir + pieces[piece.type];
    } else {
        return piece_dir + pieces[piece.type.toUpperCase()];
    }
}

function handle_click(event) {
    const square = parseInt(event.target.id.split("_")[2]);
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
        let row = square % 8;
        if (row == 7 || row == 0) {
            move["promotion"] = window.prompt("Promotion piece (q, r, b, or n)?");
        }
    }
    chess.move(move);
    from_square = null;
    calc_scale();
}

window.addEventListener("resize", calc_scale);
for (let i = 0; i < 64; i++) {
    const img = document.getElementById("work_board_" + i);
    img.addEventListener("click", handle_click);
}
window.addEventListener("load", (event) => {calc_scale();})
document.getElementById("work_board_back").addEventListener(
    "click",
    () => {chess.undo(); calc_scale();}
)
