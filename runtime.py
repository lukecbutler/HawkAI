from pathlib import Path
from google import genai
import numpy as np
import json


# 1.
def loadJSONIndexFromCache(cacheFile: Path) -> list:
    """Loads the search index from a JSON cache file.
    Args:
        cacheFile: The Path object pointing to the JSON cache file.

    Returns:
        A list of dictionaries representing the search index.

    Raises:
        FileNotFoundError: If the cache file does not exist at the given path.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    searchIndex = None

    try:
        with open(cacheFile, "r") as f:
            searchIndex = json.load(f)
        print("Successfully loaded data from JSON file")
    except FileNotFoundError:
        print(f"❌ Error: The file '{cacheFile.name}' was not found.")
    except json.JSONDecodeError:
        print(f"❌ Error: The file '{cacheFile.name}' contains invalid JSON and could not be read.")

    return searchIndex

# 2.
def embedUserQuery(userQuery: str, client) -> list:
    """Embeds a single user query string using the Gemini API.

    Args:
        userQuery: The string of text to embed.
        client: The initialized Gemini API client.

    Returns:
        A list of floats representing the embedding vector for the query.
    """
    embed_query = client.models.embed_content(

        # Set this model to embedding as well
        model="gemini-embedding-001",
        # Contents are set to the user query
        contents= [userQuery]
    )
    return embed_query.embeddings[0].values


#3
def findNarrativeUsingDotProduct(embeddedQuery: list, searchIndex: list) -> str:
    """
    Finds the most relevant narrative by calculating the dot product
    between a concept embedding and all narrative embeddings in the index.

    Args:
        embeddedQuery: A list of floats representing the query vector.
        searchIndex: A list of dictionaries, where each dict contains a narrative's
                     text and its corresponding 'embedding' vector.

    Returns:
        The text of the most similar narrative as a string, or an empty string if not found.
    """

    # 1. Extract all the narrative embeddings from the search index
    # Create an empty list to hold the embeddings.
    narrativeEmbeddings = []

    #Loop through each narrative dictionary in the searchIndex.
    for narrative in searchIndex:

        # Get the embedding vector from the dictionary
        embedding = narrative['embedding']

        # Add that vector to our new list
        narrativeEmbeddings.append(embedding)

    # 2. Use numpy's dot product to calculate all similarity scores at once.
    similarityScores = np.dot(embeddedQuery, np.transpose(narrativeEmbeddings))

    # 3. Find the index (position) of the highest score in the results
    bestNarrativeIndex = np.argmax(similarityScores)

    # 4. Use that index to get the winning narrative dictionary from the searchIndex
    bestNarrative = searchIndex[bestNarrativeIndex]

    # 5. Return the text of that narrative.
    return bestNarrative['text']


if __name__ == "__main__":

    USER_QUERY = 'Structure in Society'
    client = genai.Client()

    # pull cache file (ie. Narrative database)
    cacheFile = Path("./embeddingsCache.json")
    searchIndex = loadJSONIndexFromCache(cacheFile=cacheFile)
    
    # embed the query
    embeddedQuery = embedUserQuery(userQuery=USER_QUERY, client=client)

    # match the embeded query to the embedded narrative
    mostRelatedNarrativeToQuery = findNarrativeUsingDotProduct(embeddedQuery=embeddedQuery, searchIndex=searchIndex)
    
    print(mostRelatedNarrativeToQuery)