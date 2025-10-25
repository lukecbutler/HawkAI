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




#4. Construct output
def generateFinalOutput(userConcept: str, narrativeText: str, client) -> str:
    """
    Generates a structured final response using a generative LLM.

    Args:
        userConcept: The sociological concept the user asked about.
        narrativeText: The full text of the most relevant narrative.
        client: The initialized Gemini API client.

    Returns:
        A formatted string containing the Quote, Summary, and Concept,
        or an error message.
    """
    
    # 1. Construct the detailed prompt for the LLM.
    prompt = f"""
    You are a helpful sociological assistant. Your task is to explain a concept using a relevant personal story.

    The user wants to understand this sociological concept:
    ---
    {userConcept}
    ---

    Here is a relevant personal narrative that illustrates this concept:
    ---
    {narrativeText}
    ---

    Based on the provided concept and narrative, generate a response with exactly these three parts, formatted as follows:

    **Quote:**
    Find a single, powerful passage of 3 to 5 sentences from the narrative where the author expresses the feelings or experiences most relevant to the concept. Quote it word-for-word.

    **Summary:**
    Write a brief summary of the narrative that provides the necessary context to understand the emotional weight of the quote. Format this summary as exactly 3 bullet points.

    **Concept:**
    Provide a clear, academic description of the sociological concept '{userConcept}'. Format this description as exactly 4 bullet points.
    """ 
    
    try:
        # 2. Call the generative model.
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # 3. Return the clean text from the response.
        return response.text
        
    except Exception as e:
        # Handle potential API errors
        print(f"❌ An error occurred during AI generation: {e}")
        return "Sorry, an error occurred while generating the response."

if __name__ == "__main__":

    USER_QUERY = 'Social Inequality'
    client = genai.Client()

    # pull cache file (ie. Narrative database)
    database = Path("./narrativeEmbeddingsDbFinal.json")
    searchIndex = loadJSONIndexFromCache(cacheFile=database)
    
    # embed the query
    embeddedQuery = embedUserQuery(userQuery=USER_QUERY, client=client)

    # match the embeded query to the embedded narrative
    mostRelatedNarrativeToQuery = findNarrativeUsingDotProduct(embeddedQuery=embeddedQuery, searchIndex=searchIndex)
    
    print(generateFinalOutput(USER_QUERY, mostRelatedNarrativeToQuery, client))