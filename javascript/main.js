function current_page() {
    for (const div of document.getElementsByClassName("page")) {
        if (!div.classList.contains("hidden")) {
            return div.id;
        }
    }
}

function switch_to(page_id) {
    cpage = current_page();
    document.getElementById(cpage).classList.add("hidden");
    if (cpage == page_id) {
        document.getElementById("landing_content").classList.remove("hidden");
    } else {
        document.getElementById(page_id).classList.remove("hidden");
    }
}

document.getElementById("about").addEventListener('click',
    () => {
        document.getElementById("about_popup").classList.add("show");
        document.getElementById("content").classList.add("blur");
    }
);
document.getElementById("close_about_popup").addEventListener('click',
    () => {
        document.getElementById("about_popup").classList.remove("show");
        document.getElementById("content").classList.remove("blur");
    }
);
document.getElementById("work_board").addEventListener('click',
    () => {
        switch_to("work_board_content");
    }
)
