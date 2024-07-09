document.getElementById('fileUploadBox').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', handleFileSelect);
document.getElementById('fileUploadBox').addEventListener('dragover', handleDragOver);
document.getElementById('fileUploadBox').addEventListener('drop', handleDrop);

function handleFileSelect(event) {
    let file;
    if (event.target.files) {
        file = event.target.files[0];
    } else {
        file = event.dataTransfer.files[0];
    }
    processFile(file);
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    event.dataTransfer.dropEffect = 'copy';
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    handleFileSelect(event);
}

function processFile(file) {
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgElement = document.createElement('img');
            imgElement.src = e.target.result;
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.innerHTML = '';
            imagePreview.appendChild(imgElement);
        };
        reader.readAsDataURL(file);
        document.getElementById('uploadButton').disabled = false;
        submitForm(file);
    }
}

function submitForm(file) {
    showLoading();
    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            const filename = xhr.responseText;
            window.location.href = `/result/${filename}`;
        }
    };
    xhr.send(formData);
}

function showLoading() {
    const preview = document.getElementById('imagePreview');
    const loading = document.createElement('div');
    loading.className = 'loading';
    loading.innerHTML = '<p>Processing...</p>';
    preview.innerHTML = '';
    preview.appendChild(loading);
}
