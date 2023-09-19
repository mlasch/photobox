let elem = document.getElementById("takePhoto");
elem.addEventListener('click', fetchData);
function fetchData() {
    const preview_img = document.getElementById("preview");
    preview_img.setAttribute('src', '');
    fetch("/photo", {method: "POST"});
}

const evtSource = new EventSource("/listen");
evtSource.onmessage = (event) => {
  // const newElement = document.createElement("li");
  // const eventList = document.getElementById("list");
    document.getElementById("preview").src = "static/images/"+`${event.data}`
    // newElement.textContent = `message: ${event.data}`;
    // eventList.appendChild(newElement);
};
