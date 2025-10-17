# Import Needed Libraries
from pathlib import Path
from google import genai
import json



#1.
def loadNarrativesFromFolder(folderPath: Path)-> list:
    """Reads all .txt files from a folder into a list of dictionaries.

    Args:
        folderPath: A pathlib.Path object pointing to the source folder.

    Returns:
        A list of dictionaries, where each dictionary has two keys:
        'fileName' (str) and 'text' (str).
    """
    narrativeData = []
    for file in folderPath.glob("*.txt"):
        # For each file, create a dictionary and append it to the list
        narrativeData.append({
            #'fileName': file.name
            'text': file.read_text(encoding="utf-8", errors="ignore")
        })
    return narrativeData

#2. 
def embedNarrativeText(narrativeData: list, client) -> list:
    """
    This function takes a list of narratives, makes a single batch API call
    to embed all their texts, and adds the embedding vector back into each
    corresponding dictionary.

    Args:
        narrativeData: A list of dictionaries, where each dict has at least a 'text' key.
        client: The initialized Gemini API client.

    Returns:
        The same list of dictionaries, now with an 'embedding' key added to each one.
    """
    #create a list of all text strings to embed
    toEmbed = []
    for narrative in narrativeData:
        toEmbed.append(narrative['text'])

    # single api call to embed the entire list texts
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=toEmbed
    )

    # list of the vectors from the result
    embeddings = []
    for embedding in result.embeddings: # Loop through each embedding returned by the API
        vectors = embedding.values # Get the list of embedding values from the object
        embeddings.append(vectors) # Add that list of numbers to our list
    
    # Loop through the orignal data and new embeddings together
    for narrative, embedding in zip(narrativeData, embeddings):
        # Add the 'embedding' key to each existing dictionary
        narrative['embedding'] = embedding

    return narrativeData

#3
def buildCache(narrativeData: list, cachePath: Path) -> None:
    """Serializes and saves the narrative data to a JSON cache file.

    Args:
        narrativeData: The list of narrative dictionaries to save.
        cachePath: A pathlib.Path object for the output JSON file.
    """
    print(f"Saving index to cache file: {cachePath.name}...")
    with open(cachePath, "w") as f:
        # Use indent=4 to make the JSON file human-readable
        json.dump(narrativeData, f, indent=4)
    print("\n-> Save complete.")


if __name__ == "__main__":
    # Create client
    client = genai.Client()

    # Create path object - to sample narratives
    sampleDataDirectory = Path('./sampleNarratives') # cache path

    # pull narratives
    narrativeData = loadNarrativesFromFolder(sampleDataDirectory)

    # create narrative embeddings key
    narrativeDictionaryWithEmbeddings = embedNarrativeText(narrativeData, client=client)
    

    # build path object to dump to
    embeddingCache = Path('./embeddingCache.json')
    # dump dictionary to json
    buildCache(narrativeDictionaryWithEmbeddings, embeddingCache)