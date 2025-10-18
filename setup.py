# Import Needed Libraries
from pathlib import Path
from google import genai
import json
import docx
import time



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

def loadNarrativesFromWordDocs(folderPath: Path) -> list:
    """
    Reads all .docx files from a folder into a list of dictionaries.
    Each dictionary contains the text content.
    """
    narrativeData = []
    # 1. Look for .docx files instead of .txt
    for file in folderPath.glob("*.docx"):
        
        # 2. Open the Word Document file
        doc = docx.Document(file)
        
        # 3. Extract text from all paragraphs
        allParagraphs = []
        for p in doc.paragraphs:
            allParagraphs.append(p.text)
        
        # 4. Join them all into a single text string, separated by newlines
        fullText = "\n".join(allParagraphs)
        
        # 5. Append the dictionary, just like in your original function
        narrativeData.append({
            'text': fullText
        })
        
    return narrativeData


# @params: list of dictionaries; keys=['fileName', 'text']
# @returns: dictionary with key of 'embedded' added
def embedNarrativeText(narrativeData: list, client) -> list:
    '''
    This function adds the embedded value of each text as a key to the dictionary
    '''
    #create a list of all text strings to embed
    toEmbed = []
    for narrative in narrativeData:
        toEmbed.append(narrative['text'])

    # single api call to embed the entire list texts
    result = client.models.embed_content(
        model="gemini-embedding-001", # You might want to update this to "embedding-001"
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

    client = genai.Client()

    #build word doc folder path
    wordDocs = Path("./wordNarrativeB")

    # create dictionary
    narrativeDictionary = loadNarrativesFromWordDocs(folderPath=wordDocs)

    # create narrative embeddings key
    narrativeDictionaryWithEmbeddings = embedNarrativeText(narrativeData=narrativeDictionary, client=client)

    #path to dump json file of embeddings
    pathToDump = Path("./wordDatabaseToCompile/wordNarrativesEmbeddingB")

    buildCache(narrativeData=narrativeDictionary, cachePath=pathToDump)
