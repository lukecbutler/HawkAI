# Import Needed Libraries
from pathlib import Path
from google import genai
import numpy as np

# Gather user query and connect to Gemini
USER_QUERY = "I felt isolated during my first semester, everyone else around me seems to be doing so much better socially."
client = genai.Client()


'''Get Narratives from folder'''
# input: folder path to txt files (narratives)
# output: list where each element is the text document data
def load_texts(folder_path):
    textsList = []
    for file in folder_path.glob("*.txt"):
        content = file.read_text(encoding="utf-8", errors="ignore")
        textsList.append(content)
    return textsList
sampleDataDirectory = Path("./sample_narratives")
narrative_texts = load_texts(sampleDataDirectory)

'''Embed Narratives'''
"""embedded_narratives = client.models.embed_content(
    model = "gemini-embedding-001", 
    contents = narrative_texts
)"""

'''Embed Query'''
"""embedded_query = client.models.embed_content(
    model = "gemini-embedding-001",
    contents = USER_QUERY
)"""

#TODO: curate output of sociological output
'''Identify Concept'''
identified_concept = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Identify sociologicial concept based on this user query: {USER_QUERY}. The return value should be simple, e.g. 'Beauty Myth', 'Looking Glass Self', and 'Social Class'"
)
print(identified_concept)
print(identified_concept.text)
