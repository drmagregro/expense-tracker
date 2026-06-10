document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");

    const previewContainer = document.getElementById("preview-container");
    const previewImg = document.getElementById("preview-img");

    const btnAnalyze = document.getElementById("btn-analyze");
    const btnResetUpload = document.getElementById("btn-reset-upload");

    const loader = document.getElementById("loader");
    const formContainer = document.getElementById("form-container");
    const confirmationContainer = document.getElementById("confirmation-container");

    let selectedFile = null;

    // =========================
    // Drag & Drop
    // =========================

    ["dragenter", "dragover"].forEach(eventName => {
        dropZone.addEventListener(eventName, e => {
            e.preventDefault();
            dropZone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropZone.addEventListener(eventName, e => {
            e.preventDefault();
            dropZone.classList.remove("dragover");
        });
    });

    dropZone.addEventListener("drop", e => {
        const files = e.dataTransfer.files;

        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // Clic sur la zone
    dropZone.addEventListener("click", () => {
        fileInput.click();
    });

    // Sélection manuelle
    fileInput.addEventListener("change", e => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // =========================
    // Affichage preview
    // =========================

    function handleFile(file) {
        if (!file.type.startsWith("image/")) {
            alert("Veuillez sélectionner une image.");
            return;
        }

        selectedFile = file;

        const reader = new FileReader();

        reader.onload = e => {
            previewImg.src = e.target.result;

            dropZone.classList.add("hidden");
            previewContainer.classList.remove("hidden");

            formContainer.innerHTML = "";
            confirmationContainer.innerHTML = "";
        };

        reader.readAsDataURL(file);
    }

    // =========================
    // Analyse OCR / IA
    // =========================

    btnAnalyze.addEventListener("click", async () => {

        if (!selectedFile) {
            return;
        }

        loader.classList.remove("hidden");
        btnAnalyze.disabled = true;

        try {

            const formData = new FormData();
            formData.append("file", selectedFile);

            const response = await fetch("/api/analyze", {
                method: "POST",
                body: formData
            });

            const html = await response.text();

            formContainer.innerHTML = html;

            if (window.htmx) {
                htmx.process(formContainer);
            }

        } catch (error) {

            console.error(error);

            confirmationContainer.innerHTML = `
                <div class="error-msg">
                    ❌ Erreur lors de l'analyse.
                </div>
            `;

        } finally {

            loader.classList.add("hidden");
            btnAnalyze.disabled = false;
        }
    });

    // =========================
    // Reset
    // =========================

    btnResetUpload.addEventListener("click", () => {

        selectedFile = null;

        fileInput.value = "";

        previewImg.src = "";

        previewContainer.classList.add("hidden");
        dropZone.classList.remove("hidden");

        formContainer.innerHTML = "";
        confirmationContainer.innerHTML = "";
    });

    // =========================
    // Après soumission HTMX
    // =========================

    document.body.addEventListener("htmx:afterRequest", event => {

        if (event.detail.elt.closest("form")) {

            formContainer.innerHTML = "";

            previewContainer.classList.add("hidden");

            dropZone.classList.remove("hidden");

            selectedFile = null;
            fileInput.value = "";
        }
    });
});