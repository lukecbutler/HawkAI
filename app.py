import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from google import genai
# Import your existing functions from runtime.py
from runtime import loadJSONIndexFromCache, embedUserQuery, findNarrativeUsingDotProduct, generateFinalOutput

# --- Configuration ---
CACHE_FILE = Path("./embeddingDatabase.json") # Path to your cached index

# --- Flask App Setup ---
app = Flask(__name__)
client = genai.Client() # Assumes GOOGLE_API_KEY is set as env var
searchIndex = None # Global variable to hold the loaded index

# --- Load Data On Startup ---
def load_data():
    """Loads the search index from the cache file into memory."""
    global searchIndex
    print("Loading search index...")
    # Using your existing function from runtime.py
    searchIndex = loadJSONIndexFromCache(CACHE_FILE)
    if searchIndex is None:
        print("❌ CRITICAL ERROR: Failed to load search index. Exiting.")
        # In a real app, you might raise an exception or handle this differently
        exit() # Stop the app if data doesn't load
    print(f"✅ Search index loaded with {len(searchIndex)} items.")

# --- Routes ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/hawkai', methods=['POST'])
def handle_hawkai_query():
    """API endpoint to process a concept and return results."""
    if searchIndex is None: # ensure database was loaded on startup
        return jsonify({"error": "Search index not loaded"}), 500

    data = request.get_json() # get json data from js fetch request
    userConcept = data.get('concept') # extract concept from json data

    if not userConcept: # return error if no user concept was provided
        return jsonify({"error": "No concept provided"}), 400

    try:
        # Embed the query
        print(f"Embedding query: '{userConcept}'")
        embeddedQuery = embedUserQuery(userQuery=userConcept, client=client) # embed user query

        # Find the most relevant narrative based on dot product
        print("Finding relevant narrative...")
        mostRelatedNarrative = findNarrativeUsingDotProduct(
            embeddedQuery=embeddedQuery,
            searchIndex=searchIndex
        )

        # Check if findNarrative returned an error string
        if isinstance(mostRelatedNarrative, str) and mostRelatedNarrative.startswith("Error:"):
             print(f"❌ Error during search: {mostRelatedNarrative}")
             return jsonify({"error": mostRelatedNarrative}), 500

        # Generate the final output
        print("Generating final output...")
        finalOutput = generateFinalOutput(
            userConcept=userConcept,
            narrativeText=mostRelatedNarrative,
            client=client
        )

        # Return the result as JSON - containing final output string
        print("✅ Request processed successfully.")
        return jsonify({"result": finalOutput})

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        # Log the full error in a real application
        return jsonify({"error": "An internal server error occurred"}), 500

# --- Run the App ---
if __name__ == '__main__':
    load_data() # Load embedded database before starting the server
    app.run(debug=True, host='0.0.0.0', port=5001)