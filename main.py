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
    database = Path("./embeddingDatabase.json")
    searchIndex = loadJSONIndexFromCache(cacheFile=database)

    # Check if loading the cache failed
    if searchIndex is None:
        print("❌ Exiting: Failed to load the search index.")
        return "Error: Could not load data." # Return an error message

    # embed the query
    print(f"\nEmbedding the query: '{USER_QUERY}'...")
    embeddedQuery = embedUserQuery(userQuery=USER_QUERY, client=client)

    # --- THIS IS THE UPDATED SECTION ---
    print("Finding the most relevant narrative...")
    # 1. Unpack the tuple into two separate variables
    mostRelatedNarrativeToQuery, score = findNarrativeUsingDotProduct(
        embeddedQuery=embeddedQuery,
        searchIndex=searchIndex
    )

    # 2. Update the error check to look at the 'score' variable
    if score is None:
        # The 'mostRelatedNarrativeToQuery' variable now holds the error message
        print(f"❌ {mostRelatedNarrativeToQuery}")
        return mostRelatedNarrativeToQuery # Return the error message
    # --- END UPDATED SECTION ---

    # (Optional) You can print the score for debugging here
    print(f"  -> Found narrative with score: {score:.4f}")

    # generate the final output
    print("Generating the final output...")
    # This line now works correctly, as 'mostRelatedNarrativeToQuery' holds only the text
    finalOutput = generateFinalOutput(USER_QUERY, mostRelatedNarrativeToQuery, client)

    return finalOutput


def main():
    """Main function to execute the run logic and print the result."""
    result = run()
    print("\n--- HawkAI Response ---")
    print(result) # Print the string returned by run()

# --- FIX 2: Add this block to actually run main() ---
if __name__ == "__main__":
    main()