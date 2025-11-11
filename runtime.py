from pathlib import Path
from google import genai
import numpy as np
import json

'''This file takes the text & embedding text database, embedds the user query, 
finds the most similar narrative, and generates output using gemini flash'''

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


# In runtime.py

def findNarrativeUsingDotProduct(embeddedQuery: list, searchIndex: list): # Note: No -> str return type
    """
    Finds the most relevant narrative and its similarity score.
    Filters out narratives with missing or invalid embeddings.

    Args:
        embeddedQuery: A list of floats representing the query vector.
        searchIndex: A list of dictionaries, where each dict *should* contain
                     a narrative's text and its corresponding 'embedding' vector.

    Returns:
        A tuple of (narrative_text, score) on success.
        A tuple of (error_string, None) on failure.
    """

    # 1. Extract all the narrative embeddings from the search index
    narrativeEmbeddings = []
    originalTexts = [] # Keep a parallel list of the text

    for narrative in searchIndex:
        embedding = narrative.get('embedding')
        # Check if the embedding exists AND is a list (a valid vector)
        if embedding is not None and isinstance(embedding, list):
            narrativeEmbeddings.append(embedding)
            originalTexts.append(narrative['text'])

    if not narrativeEmbeddings:
        return "Error: No valid narrative embeddings found in the search index.", None

    # 2. Use numpy's dot product to calculate all similarity scores at once.
    try:
        similarityScores = np.dot(embeddedQuery, np.transpose(narrativeEmbeddings))
    except ValueError as e:
        return f"Error: Dot product failed. Check embedding dimensions. {e}", None

    # 3. Find the index (position) of the highest score.
    bestNarrativeIndex = np.argmax(similarityScores)

    # 4. Get the actual score value from that index.
    bestScore = similarityScores[bestNarrativeIndex]

    # 5. Use that index to get the corresponding text.
    bestNarrativeText = originalTexts[bestNarrativeIndex]

    # 6. Return BOTH the text and the score as a tuple.
    return bestNarrativeText, bestScore


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

    Quote from Student Narrative:
    Find a single, powerful passage of 3 to 5 sentences from the narrative where the author expresses the feelings or experiences most relevant to the concept. Quote it word-for-word.

    Brief Summary of Narrative:
    Write a brief summary of the narrative that provides the necessary context to understand the emotional weight of the quote. Format this summary as exactly 3 bullet points.

    Description of Sociological Concept:
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