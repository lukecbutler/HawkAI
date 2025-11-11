// Wait until the HTML document is fully loaded
document.addEventListener('DOMContentLoaded', function() {

    // Get html elements based on their id's
    const conceptInput = document.getElementById('conceptInput');
    const submitButton = document.getElementById('submitButton');
    const resultsOutput = document.getElementById('resultsOutput');
    const similarityScoreOutput = document.getElementById('similarityScore');

    // Add event listener to the button - run this function when clicked
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
        similarityScoreOutput.innerHTML = ""; // Clear the old score
        submitButton.disabled = true; // Disable button during processing

        // 2. Prepare the data to send to the Flask API
        const dataToSend = {
            concept: userConcept
        };

        // 3. Use the fetch API to send the data to our Flask backend
        fetch('/api/hawkai', {
            method: 'POST', // Specify the post request
            headers: {
                'Content-Type': 'application/json' // Tell the server we're sending JSON
            },
            body: JSON.stringify(dataToSend) // Convert the JavaScript object to a JSON string
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || `Server responded with status: ${response.status}`);
                }); // this 'throw' will trigger the '.catch()' block below
            }
            // If 200 ok, parse the JSON response body
            return response.json();
        })
        .then(data => {
            // data object looks like: { "result": "...", "score": 0.85 }

            // 1. Get the AI-generated text (a string)
            const formattedResult = data.result.replace(/\n/g, '<br>');
            
            // 2. Get the score (a number) and format it
            const formattedScore = data.score.toFixed(4);

            // 3. Populate the two divs separately
            resultsOutput.innerHTML = formattedResult;
            similarityScoreOutput.innerHTML = formattedScore;
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch process
            console.error('Error:', error); // Log the error to the browser console
            resultsOutput.innerHTML = `<p class="text-danger">An error occurred: ${error.message}</p>`; // display user friendly error message
            similarityScoreOutput.innerHTML = '<p class="text-danger">Error</p>'; // Also update score div on error
        })
        .finally(() => { // runs at end, whether successful or not
             submitButton.disabled = false; // Re-enable the button
        });
    });
});