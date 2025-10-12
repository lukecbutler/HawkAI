# Import Needed Libraries
from pathlib import Path
from google import genai
import json


client = genai.Client()

#1
'''Get text of all narratives from sampleNarrative folder'''
# input: folder path to txt files
# output: list where each element is the text document data
def loadNarrativesFromFolder(folderPath: Path)-> list:
    """
    Reads all .txt files from a folder and returns a list of dictionaries.
    Each dictionary contains the fileName and the text content.
    """
    narrativeData = []
    for file in folderPath.glob("*.txt"):
        # For each file, create a dictionary and append it to the list
        narrativeData.append({
            'fileName': file.name,
            'text': file.read_text(encoding="utf-8", errors="ignore")
        })
    return narrativeData

#2
def embedNarrativeText(narrativeData: dict) -> dict:

    #loop through narrativeData, to create a list of all text strings to embed
    toEmbed = []
    for narrative in narrativeData:
        toEmbed.append(narrative['text'])

    # make 1 api call to embed the entire list of texts - 
    # (you'll get back a list of all embeddings in the same order)
    result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=toEmbed
    )

    # list of the vectors from the result
    embeddings = []

    for embedding in result.embeddings: # Loop through each embedding returned by the API

        # Get the list of embedding values from the object
        vectors = embedding.values
        # Add that list of numbers to our list
        embeddings.append(vectors)
    
    # Loop through the orignal data and new embeddings together
    for narrative, embedding in zip(narrativeData, embeddings):
        # Add the 'embedding' key to each existing dictionary
        narrative['embedding'] = embedding

    return narrativeData

#3
def buildCache(narrativeData: dict):
    with open('embeddingsCache.json', "w") as fp:
        json.dump(narrativeData, fp)
    return None

if __name__ == "__main__":
    sampleDataDirectory = Path('./sampleNarratives')
    narrativeData = loadNarrativesFromFolder(sampleDataDirectory)
    narrativeDictionaryWithEmbeddings = embedNarrativeText(narrativeData)
    buildCache(narrativeDictionaryWithEmbeddings)