from runtime import *
from setup import *
from pathlib import Path
from google import genai

def run():
    USER_QUERY = 'Structure in Society'
    client = genai.Client()

    # pull cache file (ie. Narrative database)
    cacheFile = Path("./embeddingsCache.json")
    searchIndex = loadJSONIndexFromCache(cacheFile=cacheFile)

    # embed the query
    embeddedQuery = embedUserQuery(userQuery=USER_QUERY, client=client)

    # match the embeded query to the embedded narrative
    mostRelatedNarrativeToQuery = findNarrativeUsingDotProduct(embeddedQuery=embeddedQuery, searchIndex=searchIndex)

    return generateFinalOutput(USER_QUERY, mostRelatedNarrativeToQuery, client)

def main():
    print(run())

main()