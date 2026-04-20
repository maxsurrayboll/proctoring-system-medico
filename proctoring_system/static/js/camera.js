// ------------------ FUNCIÓN ALERTA ------------------
function showAlert(msg) {
    const alerta = document.getElementById("alerta");
    alerta.innerText = msg;
    alerta.style.display = "block";
}

// ------------------ INICIAR CÁMARA ------------------
navigator.mediaDevices.getUserMedia({ video: true, audio: false })
.then(stream => {
    const video = document.getElementById("video");
    video.srcObject = stream;

    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    // Esperar a que el video esté listo
    video.onloadedmetadata = () => {
        video.play();

        // Capturar frame cada 5 segundos
        setInterval(() => {
            // Evitar capturas vacías
            if (video.videoWidth === 0 || video.videoHeight === 0) {
                console.warn("Video no listo aún");
                return;
            }

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            context.drawImage(video, 0, 0);

            canvas.toBlob(blob => {
                if (!blob) {
                    console.error("No se pudo generar imagen");
                    return;
                }

                const formData = new FormData();
                formData.append("frame", blob, "frame.png");

                fetch("/exam/upload_frame", {
                    method: "POST",
                    body: formData
                })
                .then(res => res.json())
                .then(data => {
                    // 🔴 ALERTA POR MÚLTIPLES PERSONAS
                    if (data.alert) {
                        showAlert("⚠️ Múltiples personas detectadas");
                    }
                })
                .catch(err => {
                    console.error("Error enviando frame:", err);
                });

            }, "image/png");

        }, 5000); // cada 5 segundos
    };

})
.catch(error => {
    console.error("Error al acceder a la cámara:", error);
});


// ------------------ DETECCIÓN DE TRAMPA (EVENTOS) ------------------

// Cambio de pestaña
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        sendEvent("tab_switch");
    }
});

// Pérdida de foco (salirse de la ventana)
window.addEventListener("blur", () => {
    sendEvent("window_blur");
});


// ------------------ ENVÍO DE EVENTOS ------------------
function sendEvent(type) {
    fetch("/exam/log_event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            event_type: type,
            details: "Detectado desde frontend"
        })
    })
    .then(res => res.json())
    .then(data => {
        // 🔴 ALERTA POR RIESGO ACUMULADO
        if (data.risk_score >= 5) {
            showAlert("⚠️ Alto riesgo de comportamiento sospechoso");
        }
    })
    .catch(err => {
        console.error("Error enviando evento:", err);
    });
}