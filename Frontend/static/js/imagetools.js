// Global variables
let currentFile = null;
let originalImage = null;
let originalWidth = 0;
let originalHeight = 0;

// Tab switching
function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

    const tabs = {
        'resize': 0,
        'crop': 1,
        'compress': 2,
        'convert': 3
    };

    document.querySelectorAll('.tab')[tabs[tab]].classList.add('active');
    document.getElementById(`${tab}-tab`).classList.add('active');
}

// File selection handler
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    currentFile = file;
    const reader = new FileReader();

    reader.onload = function (e) {
        const img = new Image();
        img.onload = function () {
            originalImage = img;
            originalWidth = img.width;
            originalHeight = img.height;

            // Show preview
            document.getElementById('previewImage').src = e.target.result;
            document.getElementById('previewContainer').style.display = 'block';

            // Update info
            document.getElementById('infoWidth').textContent = `${img.width}px`;
            document.getElementById('infoHeight').textContent = `${img.height}px`;
            document.getElementById('infoRatio').textContent = (img.width / img.height).toFixed(2);
            document.getElementById('infoSize').textContent = formatFileSize(file.size);
            document.getElementById('infoFormat').textContent = file.type.split('/')[1].toUpperCase();
            document.getElementById('imageInfo').style.display = 'block';

            // Setup resize auto-calculation
            setupResizeListeners();

            // Setup crop canvas
            setupCropCanvas();
        };
        img.src = e.target.result;
    };

    reader.readAsDataURL(file);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Setup resize listeners
function setupResizeListeners() {
    const widthInput = document.getElementById('resizeWidth');
    const heightInput = document.getElementById('resizeHeight');
    const methodSelect = document.getElementById('resizeMethod');

    // Toggle between dimensions and percentage
    methodSelect.addEventListener('change', function () {
        if (this.value === 'percentage') {
            document.getElementById('dimensionsInputs').style.display = 'none';
            document.getElementById('percentageInput').style.display = 'block';
        } else {
            document.getElementById('dimensionsInputs').style.display = 'grid';
            document.getElementById('percentageInput').style.display = 'none';
        }
    });

    // Auto-calculate height when width changes
    widthInput.addEventListener('input', function () {
        if (this.value && originalWidth && originalHeight) {
            const newWidth = parseInt(this.value);
            const aspectRatio = originalHeight / originalWidth;
            const newHeight = Math.round(newWidth * aspectRatio);
            heightInput.value = newHeight;
            heightInput.style.backgroundColor = '#f0f0f0';
        }
    });

    // Auto-calculate width when height changes
    heightInput.addEventListener('input', function () {
        if (this.value && originalWidth && originalHeight) {
            const newHeight = parseInt(this.value);
            const aspectRatio = originalWidth / originalHeight;
            const newWidth = Math.round(newHeight * aspectRatio);
            widthInput.value = newWidth;
            widthInput.style.backgroundColor = '#f0f0f0';
        }
    });
}

// Process resize
function processResize() {
    if (!currentFile) {
        showResult('Please upload an image first!', 'error', 'resizeResult');
        return;
    }

    const method = document.getElementById('resizeMethod').value;
    let width, height;

    if (method === 'percentage') {
        const percent = parseInt(document.getElementById('resizePercent').value);
        if (!percent) {
            showResult('Please enter a percentage!', 'error', 'resizeResult');
            return;
        }
        width = Math.round(originalWidth * (percent / 100));
        height = Math.round(originalHeight * (percent / 100));
    } else {
        width = parseInt(document.getElementById('resizeWidth').value);
        height = parseInt(document.getElementById('resizeHeight').value);

        if (!width && !height) {
            showResult('Please enter width or height!', 'error', 'resizeResult');
            return;
        }

        // If only one dimension provided, calculate the other
        if (!width) width = Math.round(height * (originalWidth / originalHeight));
        if (!height) height = Math.round(width * (originalHeight / originalWidth));
    }

    // Resize using canvas
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(originalImage, 0, 0, width, height);

    canvas.toBlob(function (blob) {
        downloadBlob(blob, `resized_${width}x${height}.jpg`);
        showResult(`✓ Image resized to ${width}×${height}px and downloaded!`, 'success', 'resizeResult');
    }, 'image/jpeg', 0.95);
}

// Setup crop canvas
function setupCropCanvas() {
    const canvas = document.getElementById('cropCanvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size to match image
    const maxWidth = 800;
    const scale = Math.min(1, maxWidth / originalWidth);
    canvas.width = originalWidth * scale;
    canvas.height = originalHeight * scale;

    // Draw image
    ctx.drawImage(originalImage, 0, 0, canvas.width, canvas.height);

    document.getElementById('cropContainer').style.display = 'block';
}

// Update crop dimensions based on ratio
function updateCropDimensions() {
    const ratio = document.getElementById('cropRatio').value;
    const widthInput = document.getElementById('cropWidth');
    const heightInput = document.getElementById('cropHeight');

    if (ratio === 'free') {
        widthInput.value = '';
        heightInput.value = '';
        return;
    }

    const [w, h] = ratio.split(':').map(Number);
    const aspectRatio = w / h;

    // Use original width and calculate height
    widthInput.value = originalWidth;
    heightInput.value = Math.round(originalWidth / aspectRatio);
}

// Process crop
function processCrop() {
    if (!currentFile) {
        showResult('Please upload an image first!', 'error', 'cropResult');
        return;
    }

    let width = parseInt(document.getElementById('cropWidth').value) || originalWidth;
    let height = parseInt(document.getElementById('cropHeight').value) || originalHeight;

    // Crop from center
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    const sx = (originalWidth - width) / 2;
    const sy = (originalHeight - height) / 2;

    ctx.drawImage(originalImage, sx, sy, width, height, 0, 0, width, height);

    canvas.toBlob(function (blob) {
        downloadBlob(blob, `cropped_${width}x${height}.jpg`);
        showResult(`✓ Image cropped to ${width}×${height}px and downloaded!`, 'success', 'cropResult');
    }, 'image/jpeg', 0.95);
}

// Process compress
function processCompress() {
    if (!currentFile) {
        showResult('Please upload an image first!', 'error', 'compressResult');
        return;
    }

    const quality = parseInt(document.getElementById('qualitySlider').value) / 100;
    const targetSize = document.getElementById('targetSize').value;

    const canvas = document.createElement('canvas');
    canvas.width = originalWidth;
    canvas.height = originalHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(originalImage, 0, 0);

    if (targetSize) {
        // Iteratively reduce quality to meet target size
        compressToSize(canvas, parseInt(targetSize) * 1024, function (blob) {
            const reduction = ((1 - blob.size / currentFile.size) * 100).toFixed(1);
            downloadBlob(blob, 'compressed.jpg');
            showResult(`✓ Compressed! ${formatFileSize(currentFile.size)} → ${formatFileSize(blob.size)} (${reduction}% reduction)`, 'success', 'compressResult', true);
        });
    } else {
        canvas.toBlob(function (blob) {
            const reduction = ((1 - blob.size / currentFile.size) * 100).toFixed(1);
            downloadBlob(blob, 'compressed.jpg');
            showResult(`✓ Compressed! ${formatFileSize(currentFile.size)} → ${formatFileSize(blob.size)} (${reduction}% reduction)`, 'success', 'compressResult', true);
        }, 'image/jpeg', quality);
    }
}

// Compress to target size
function compressToSize(canvas, targetSize, callback) {
    let quality = 0.9;

    function tryCompress() {
        canvas.toBlob(function (blob) {
            if (blob.size <= targetSize || quality <= 0.1) {
                callback(blob);
            } else {
                quality -= 0.1;
                tryCompress();
            }
        }, 'image/jpeg', quality);
    }

    tryCompress();
}

// Process convert
function processConvert() {
    if (!currentFile) {
        showResult('Please upload an image first!', 'error', 'convertResult');
        return;
    }

    const format = document.getElementById('convertFormat').value;
    const quality = parseInt(document.getElementById('convertQualitySlider').value) / 100;

    const canvas = document.createElement('canvas');
    canvas.width = originalWidth;
    canvas.height = originalHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(originalImage, 0, 0);

    const mimeType = `image/${format}`;
    const extension = format === 'jpeg' ? 'jpg' : format;

    canvas.toBlob(function (blob) {
        downloadBlob(blob, `converted.${extension}`);
        showResult(`✓ Converted to ${format.toUpperCase()} and downloaded!`, 'success', 'convertResult');
    }, mimeType, quality);
}

// Download blob
function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Show result message
function showResult(message, type, elementId, isHTML = false) {
    const resultDiv = document.getElementById(elementId);
    if (isHTML) {
        resultDiv.innerHTML = message;
    } else {
        resultDiv.textContent = message;
    }
    resultDiv.className = `result ${type}`;
    resultDiv.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        resultDiv.style.display = 'none';
    }, 5000);
}
