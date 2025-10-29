// Wait until the HTML document is fully loaded
document.addEventListener('DOMContentLoaded', function() {

    // Get references to the HTML elements we need to interact with
    const conceptInput = document.getElementById('conceptInput');
    const submitButton = document.getElementById('submitButton');
    const resultsOutput = document.getElementById('resultsOutput');

    // Add an event listener to the button - run this function when clicked
    submitButton.addEventListener('click', function() {

        // 1. Get the concept typed by the user from the input field
        const userConcept = conceptInput.value.trim(); // .trim() removes extra spaces

        // Basic check: Make sure the user typed something
        if (!userConcept) {
            resultsOutput.innerHTML = '<p class="text-danger">Please enter a concept.</p>';
            return; // Stop the function here if input is empty
        }

        // Show a loading message while waiting for the API
        resultsOutput.innerHTML = '<p class="text-info">Processing... Please wait.</p>';
        submitButton.disabled = true; // Disable button during processing

        // 2. Prepare the data to send to the Flask API
        const dataToSend = {
            concept: userConcept
        };

        // 3. Use the fetch API to send the data to our Flask backend
        fetch('/api/hawkai', {
            method: 'POST', // Specify the method
            headers: {
                'Content-Type': 'application/json' // Tell the server we're sending JSON
            },
            body: JSON.stringify(dataToSend) // Convert the JavaScript object to a JSON string
        })
        .then(response => {
            // Check if the server responded successfully (status code 200-299)
            if (!response.ok) {
                // If not okay, try to read the error message from the server's JSON response
                return response.json().then(errorData => {
                    throw new Error(errorData.error || `Server responded with status: ${response.status}`);
                });
            }
            // If okay, parse the JSON response body
            return response.json();
        })
        .then(data => {
            // 4. Display the result from the Flask API
            // The JSON from Flask looks like: { "result": "Quote: ... Summary: ..." }
            // We need to handle potential line breaks in the result for HTML
            const formattedResult = data.result.replace(/\n/g, '<br>');
            resultsOutput.innerHTML = formattedResult; // Update the content of the results div
        })
        .catch(error => {
            // 5. Handle any errors that occurred during the fetch process
            console.error('Error:', error); // Log the error to the browser console
            resultsOutput.innerHTML = `<p class="text-danger">An error occurred: ${error.message}</p>`;
        })
        .finally(() => {
             // This always runs, whether successful or failed
             submitButton.disabled = false; // Re-enable the button
        });
    });
});