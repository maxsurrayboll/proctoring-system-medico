navigator.mediaDevices.getUserMedia({ video: true, audio: true })
.then(stream => {
    document.getElementById("video").srcObject = stream;
})
.catch(error => {
    console.log("Error al acceder a la cámara", error);
});
