const take_photo_elem = document.getElementById("takePhoto");
take_photo_elem.addEventListener('click', takePhotoEvent);
function takePhotoEvent() {
    const preview_img = document.getElementById("preview");
    preview_img.setAttribute('src', '');
    fetch("/photo", {method: "POST"});
}

const print_photo_elem = document.getElementById("printPhoto");
print_photo_elem.addEventListener('click', printPhoto);
function printPhoto() {
    const preview_img = document.getElementById("preview");
    const filename = preview_img.getAttribute('src');
    console.log(filename)
    fetch("/print?filename="+filename, {method: "POST"});
}

const evtSource = new EventSource("/listen");
evtSource.onmessage = (event) => {
  // const newElement = document.createElement("li");
  // const eventList = document.getElementById("list");
    document.getElementById("preview").src = "static/images/"+`${event.data}`
    print_photo_elem.style.display = "inline";

    // newElement.textContent = `message: ${event.data}`;
    // eventList.appendChild(newElement);
};
