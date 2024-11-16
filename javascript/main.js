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

