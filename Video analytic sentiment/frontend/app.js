document.addEventListener('DOMContentLoaded', () => {
    const analysisForm = document.getElementById('analysisForm');
    const videoUrlInput = document.getElementById('videoUrl');
    const content_analysis_checkbox = document.getElementById('contentAnalysis');
    const analyzeButton = document.getElementById('analyzeButton');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessageDiv = document.getElementById('errorMessage');
    const reportContentPre = document.getElementById('reportContent');

    analysisForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        errorMessageDiv.textContent = ''; // Clear previous errors
        reportContentPre.textContent = ''; // Clear previous report

        const url = videoUrlInput.value;
        const content_analysis = content_analysis_checkbox.checked; // Changed variable name here

        if (!url) {
            errorMessageDiv.textContent = 'Please enter a video URL.';
            return;
        }

        // Disable input and button, show spinner
        videoUrlInput.disabled = true;
        content_analysis_checkbox.disabled = true; // Use new variable name
        analyzeButton.disabled = true;
        loadingSpinner.style.display = 'inline-block';

        try {
            const response = await fetch('http://127.0.0.1:8000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url, content_analysis }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed.');
            }

            const report = await response.json();
            reportContentPre.textContent = JSON.stringify(report, null, 2);

        } catch (error) {
            console.error('Error:', error);
            let displayMessage = 'An unknown error occurred.';
            if (error.message) {
                displayMessage = `Error: ${error.message}`;
            } else if (typeof error === 'object' && error !== null) {
                displayMessage = `Error: ${JSON.stringify(error, null, 2)}`;
            } else {
                displayMessage = `Error: ${error.toString()}`;
            }
            errorMessageDiv.textContent = displayMessage;
        } finally {
            // Re-enable input and button, hide spinner
            videoUrlInput.disabled = false;
            content_analysis_checkbox.disabled = false;
            analyzeButton.disabled = false;
            loadingSpinner.style.display = 'none';
        }
    });
});