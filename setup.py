# Import Needed Libraries
from pathlib import Path
from google import genai
import json
import docx

# --- Helper Functions ---

#1. Load Word Docs
def loadNarrativesFromWordDocs(folderPath: Path) -> list:
    """
    Reads all .docx files from a folder into a list of dictionaries.
    """
    narrativeData = []
    print(f"Loading narratives from: {folderPath}")
    filesFound = list(folderPath.glob("*.docx")) # Get a count upfront

    if not filesFound:
        print("❌ Error: No .docx files found in the specified folder.")
        return [] # Return empty list if no files

    print(f"Found {len(filesFound)} .docx files. Reading content...")
    for file in filesFound:
        try:
            doc = docx.Document(file)
            allParagraphs = [p.text for p in doc.paragraphs]
            fullText = "\n".join(allParagraphs)
            narrativeData.append({'text': fullText})
        except Exception as e:
            print(f"  ⚠️ Warning: Could not read file {file.name}. Error: {e}. Skipping.")

    print(f"Successfully loaded content from {len(narrativeData)} files.")
    return narrativeData


#2.
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


#3. Build Cache
def buildCache(narrativeData: list, cachePath: Path) -> None:
    """Serializes and saves the narrative data to a JSON cache file."""
    if not narrativeData:
        print("No data to save to cache.")
        return

    # Ensure the parent directory exists
    cachePath.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nSaving index to cache file: {cachePath}...")
    try:
        with open(cachePath, "w") as f:
            json.dump(narrativeData, f, indent=4)
        print("✅ Save complete.")
    except Exception as e:
        print(f"❌ Error saving cache file: {e}")


# --- Main Execution Block ---
if __name__ == "__main__":

    client = genai.Client()
    ''''''
    CURRENT_WORD_PATH = Path('./splitBatches/wordNarrativeT-Z')
    CURRENT_EMBEDDING_PATH = Path('./batchWordEmbeddings/wordEmbeddingT-Z.json')
    ''''''

    # set path 
    listOfNarrativeDictionaries = loadNarrativesFromWordDocs(CURRENT_WORD_PATH)


    # embed
    listOfNarrativeDictionariesWithEmbedding = embedNarrativeText(listOfNarrativeDictionaries ,client=client)


    # dump to JSON
    buildCache(listOfNarrativeDictionariesWithEmbedding, CURRENT_EMBEDDING_PATH)
