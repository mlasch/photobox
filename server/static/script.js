const take_photo_elem = document.getElementById("takePhoto");
take_photo_elem.addEventListener('click', takePhotoEvent);

photoTimeout = () => {
    fetch("/photo", {method: "POST"});
    const preview_img = document.getElementById("preview");
    preview_img.setAttribute('src', '');
    preview_img.style.display = "none";
};

function takePhotoEvent() {
    const preview_img = document.getElementById("preview");
    preview_img.setAttribute('src', 'static/countdown.gif');
    setTimeout(photoTimeout, 7000);
}

const print_photo_elem = document.getElementById("printPhoto");
print_photo_elem.addEventListener('click', printPhoto);
function printPhoto() {
    const preview_img = document.getElementById("preview");
    const filename = preview_img.getAttribute('src');
    console.log(filename)
    fetch("/print?filename="+filename, {method: "POST"});
}

let loadPhotoSSE;

loadPhotoSSEInit = () => {
    loadPhotoSSE = new EventSource("/listen");
    loadPhotoSSE.onmessage = (event) => {
        if (event.data === "init") {
            // Server sends a first reply in order to establish the connection
            return null;
        } else {
            const preview_img = document.getElementById("preview")
            preview_img.src = "static/images/" + `${event.data}`
            preview_img.style.display = "inline";
            print_photo_elem.style.display = "inline";
        }
    };

    loadPhotoSSE.onerror = () => {
        loadPhotoSSE.close();
    }
};
loadPhotoSSEInit();

setInterval(() => {
    if (loadPhotoSSE.readyState === EventSource.OPEN) {
        return null;
    } else {
        loadPhotoSSEInit();
    }
}, 5000);