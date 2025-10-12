'''
This files returns the most related narrative to the User Query
'''


# Embedding -> translates the meaning of text into numbers, 
# finds closest relation between two concepts

'''
the purpose of mapping the narrative results, 
and the query result is to see which narrative result 
is closest to the query result
'''

# Import Needed Libraries
from pathlib import Path
from google import genai
import numpy as np

USER_QUERY = "I felt isolated during my first semester."

# Connect to gemini and gather path for narratives
client = genai.Client()
sampleDataDirectory = Path("./sample_narratives")

# input: folder path to txt files (narratives)
# output: list where each element is the text document data
def load_texts(folder_path):
    textsList = []
    for file in folder_path.glob("*.txt"):
        content = file.read_text(encoding="utf-8", errors="ignore")
        textsList.append(content)
    return textsList
narrative_texts = load_texts(sampleDataDirectory)


#Main Program
''''''''''''''''''''''''#API CALLS''''''''''''''''''''''''''''''''
# First API Call, creates embeddings for the narratives
embed_narratives = client.models.embed_content(

        # Select the gemini embedding model
        model="gemini-embedding-001",

        # Set the Content for the model to the list of texts from the text files
        contents= narrative_texts
)

# Second API call to create embedding for the user's query.
embed_query = client.models.embed_content(

        # Set this model to embedding as well
        model="gemini-embedding-001",
        # Contents are set to the user query
        contents= [USER_QUERY]
)
''''''''''''''''''''''''#API CALLS''''''''''''''''''''''''''''''''


"""Numpy Calculation of similarities between two embeddings"""
# input: query result mapping, narrative results & their mappings, list of narrative texts
# output: most relative narrative based on the narrative mapping
def find_most_relevant_narrative(embed_query, embed_narratives, narrative_texts):
    """
    Finds the most relevant narrative text by comparing embedding similarity.
    """
    # 1. Extract the embedding vector for the user's query.
    query_embedding = embed_query.embeddings[0].values

    # 2. Get the list of all narrative embedding vectors.
    narrative_embeddings = [e.values for e in embed_narratives.embeddings]

    # 3. Use the dot product to calculate the similarity score for each narrative.
    # This creates a list of scores, one for each narrative.
    similarity_scores = np.dot(query_embedding, np.transpose(narrative_embeddings))

    # 4. Find the index of the narrative with the highest score.
    best_narrative_index = np.argmax(similarity_scores)

    # 5. Return the text of the best narrative using that index.
    return narrative_texts[best_narrative_index]



# Most relative narrative implementation, set to best_narrative_match variable
# variable is a string of full narrative
best_narrative_match = find_most_relevant_narrative(
    embed_query = embed_query,
    embed_narratives = embed_narratives,
    narrative_texts = narrative_texts
)

print(best_narrative_match)