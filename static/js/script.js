const form = document.getElementById('uploadForm');
const dropZone = document.getElementById('dropZone');
const imageInput = document.getElementById('imageInput');
const chooseButton = document.getElementById('chooseButton');
const removeButton = document.getElementById('removeButton');
const emptyUpload = document.getElementById('emptyUpload');
const selectedUpload = document.getElementById('selectedUpload');
const imagePreview = document.getElementById('imagePreview');
const generateButton = document.getElementById('generateButton');
const captionBox = document.getElementById('captionBox');
const statusMessage = document.getElementById('statusMessage');
let selectedFile = null;
let previewUrl = null;
let captionGenerated = false;

chooseButton.addEventListener('click', (event) => {
    event.stopPropagation();
    imageInput.click();
});

dropZone.addEventListener('click', () => imageInput.click());
dropZone.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        imageInput.click();
    }
});

imageInput.addEventListener('change', () => handleFile(imageInput.files[0]));

['dragenter', 'dragover'].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.add('dragging');
    });
});

['dragleave', 'drop'].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.remove('dragging');
    });
});

dropZone.addEventListener('drop', (event) => handleFile(event.dataTransfer.files[0]));
removeButton.addEventListener('click', (event) => {
    event.stopPropagation();
    resetUpload();
});

function handleFile(file) {
    if (!file || !file.type.startsWith('image/')) {
        showStatus('Please choose a valid image file.');
        return;
    }
    if (file.size > 16 * 1024 * 1024) {
        showStatus('Please choose an image smaller than 16MB.');
        return;
    }

    if (previewUrl) URL.revokeObjectURL(previewUrl);
    selectedFile = file;
    captionGenerated = false;
    previewUrl = URL.createObjectURL(file);
    imagePreview.src = previewUrl;
    emptyUpload.hidden = true;
    selectedUpload.hidden = false;
    generateButton.disabled = false;
    generateButton.classList.remove('analyze-button');
    generateButton.textContent = 'Generate Caption';
    captionBox.textContent = 'Your caption will appear here...';
    captionBox.classList.remove('has-caption');
    statusMessage.hidden = true;
}

function resetUpload() {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = null;
    selectedFile = null;
    imageInput.value = '';
    imagePreview.removeAttribute('src');
    emptyUpload.hidden = false;
    selectedUpload.hidden = true;
    generateButton.disabled = true;
    captionGenerated = false;
    generateButton.classList.remove('analyze-button');
    generateButton.textContent = 'Generate Caption';
}

function showStatus(message) {
    statusMessage.textContent = message;
    statusMessage.hidden = false;
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!selectedFile) return;
    if (captionGenerated) {
        resetUpload();
        captionBox.textContent = 'Your caption will appear here...';
        captionBox.classList.remove('has-caption');
        return;
    }

    generateButton.disabled = true;
    generateButton.textContent = 'Generating...';
    statusMessage.hidden = true;

    try {
        const formData = new FormData(form);
        formData.set('image', selectedFile, selectedFile.name);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'The image could not be processed.');
        }
        captionBox.textContent = data.caption;
        captionBox.classList.add('has-caption');
        captionGenerated = true;
        generateButton.disabled = false;
        generateButton.classList.add('analyze-button');
        generateButton.innerHTML = '<span class="button-icon" aria-hidden="true">&#8635;</span>Analyze Another';
    } catch (error) {
        showStatus(error.message || 'The image could not be processed.');
    } finally {
        if (!captionGenerated) {
            generateButton.disabled = !selectedFile;
            generateButton.classList.remove('analyze-button');
            generateButton.textContent = 'Generate Caption';
        }
    }
});
