// script.js
// IMPORTANT: Use the URL and port where your FastAPI server is running
const API_BASE_URL = 'http://127.0.0.1:8000'; 

// Function to handle the form submission and communicate with the backend
async function handleSymptomSubmission(event) {
    event.preventDefault(); // Prevents the page from reloading
    
    const symptomInput = document.getElementById('symptoms-input');
    const resultsDiv = document.getElementById('ai-results');
    
    const symptoms = symptomInput.value.trim();
    
    if (symptoms === "") {
        resultsDiv.innerHTML = '<p class="error">Please enter your symptoms.</p>';
        return;
    }
    
    // Display a loading state while waiting for the API
    resultsDiv.innerHTML = '<p class="loading-state">Processing symptoms with AI...</p>';

    try {
        // 1. Send data to the FastAPI endpoint using a POST request
        const response = await fetch(`${API_BASE_URL}/check-symptoms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // 2. The body must be JSON matching the Pydantic model in main.py
            body: JSON.stringify({ symptoms: symptoms })
        });

        if (!response.ok) {
            throw new Error(`API call failed with status ${response.status}`);
        }

        const data = await response.json();

        // 3. Update the frontend with the response data
        let html = `<h3>AI Response</h3>`;

        // Check if the response contains the Misinformation Alert
        if (data.guidance.includes('Misinformation Alert')) {
             html += `<div class="misinfo-warning">
                         <span style="font-weight: bold; color: var(--pink);">🚨 MISINFORMATION ALERT:</span> 
                         ${data.guidance.replace('**Misinformation Alert:** ', '')}
                      </div>`;
        } else {
             html += `<p>${data.guidance}</p>`;
        }

        resultsDiv.innerHTML = html;
        
    } catch (error) {
        console.error("Error communicating with backend:", error);
        resultsDiv.innerHTML = '<p class="error-state">Could not connect to the AI service. Please ensure your backend is running at ' + API_BASE_URL + '</p>';
    }
}

// Wait for the page to load, then attach the function to the form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('symptom-form');
    if (form) {
        form.addEventListener('submit', handleSymptomSubmission);
    }
});