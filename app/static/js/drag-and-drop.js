document.addEventListener("DOMContentLoaded", function() {
    const textAreas = document.querySelectorAll('[data-drag-drop="true"]');
    
    textAreas.forEach((textArea) => {
        textArea.addEventListener('dragover', function(event) {
            event.preventDefault();
        });

        textArea.addEventListener('drop', function(event) {
            event.preventDefault();
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                if (file.type === 'text/plain' || file.type === 'biosequence/fasta') {
                    const reader = new FileReader();
                    reader.readAsText(file);
                    reader.onload = function() {
                        textArea.value = reader.result;
                    };
                } else {
                    alert('Only text files are allowed.');
                }
            }
        });
    });
});
