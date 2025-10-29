# Import functions from your other modules
from runtime import loadJSONIndexFromCache, embedUserQuery, findNarrativeUsingDotProduct, generateFinalOutput
# Note: You don't actually need anything from setup.py here
from pathlib import Path
from google import genai

def run():
    """Contains the core logic for running the AI query."""

    USER_QUERY = 'Pay among genders' # Or get input: input("Enter a sociological concept: ")
    client = genai.Client()

    # pull cache file (ie. Narrative database)
    database = Path("./narrativeEmbeddingsDbFinal.json")
    searchIndex = loadJSONIndexFromCache(cacheFile=database)

    # Check if loading the cache failed
    if searchIndex is None:
        print("❌ Exiting: Failed to load the search index.")
        return "Error: Could not load data." # Return an error message

    # embed the query
    print(f"\nEmbedding the query: '{USER_QUERY}'...")
    embeddedQuery = embedUserQuery(userQuery=USER_QUERY, client=client)

    # match the embedded query to the embedded narrative
    print("Finding the most relevant narrative...")
    mostRelatedNarrativeToQuery = findNarrativeUsingDotProduct(embeddedQuery=embeddedQuery, searchIndex=searchIndex)

    # Check if the search returned an error message
    if mostRelatedNarrativeToQuery.startswith("Error:"):
        print(f"❌ {mostRelatedNarrativeToQuery}")
        return mostRelatedNarrativeToQuery # Return the error message

    # generate the final output
    print("Generating the final output...")
    finalOutput = generateFinalOutput(USER_QUERY, mostRelatedNarrativeToQuery, client)

    # --- FIX 1: Return the output string ---
    return finalOutput


def main():
    """Main function to execute the run logic and print the result."""
    result = run()
    print("\n--- HawkAI Response ---")
    print(result) # Print the string returned by run()

# --- FIX 2: Add this block to actually run main() ---
if __name__ == "__main__":
    main()