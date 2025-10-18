HawkAI 2.1 overview

database: 600 studdent narratives built around sociological concept

input: Sociological Concept

output: 
    - quote from narrative using that concept
    - summary of narrative using that concept
    - description of sociological concept


objective 1: Strip personal information from all student narratives [√]
objective 2: Match sociological concept (ie. the user query) to most relative narrative []
objective 3: Input information into Gemini API[√]
objective 3.5: HawkAI run's all articles []
objective 4: Change summary & concept to bullet points - summary: 3; concept: 4[]
objective 5: If a similarity score is to low, still relate back to most alike narrative, but give preview of synthetic narrative[]


instructions:
Hawk AI Bot Instructions v2
1. The user enters a prompt for helping to understand a learning concept. [√]
2. Bot identifies a narrative in the knowledge corpus that is relevant to that concept. [√]
3. Then generate an output with these elements:
    a. The quote. Word for word from the identified narrative. AI finds a quotable passage (3-5 sentences, but LLM uses discretion) in the narrative where the author expresses their feelings, experiences, or insights that are most relevant to the user query (the inputted sociological concept).

    b. Summary of the narrative that would provide the needed information so that the quote is clear.

    c. Concept. A description of the sociological concept that the user is seeking to understand.
