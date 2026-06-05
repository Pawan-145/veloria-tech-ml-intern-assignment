import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

print("=== Step 1: Converting CSV Data into Custom Sentence Format ===")

# Dynamic path directory safety check (handles both task1 and task_1 folder names)
DATA_DIRECTORY = "task1" if os.path.exists("task1") else "task_1"
CSV_FILE_NAME = "match_data.csv"
FULL_CSV_PATH = os.path.join(DATA_DIRECTORY, CSV_FILE_NAME)

# Verify file location stability
if not os.path.exists(FULL_CSV_PATH):
    raise FileNotFoundError(
        f"\n[CRITICAL ERROR]: Could not find '{CSV_FILE_NAME}' in the folder: '{os.path.abspath(DATA_DIRECTORY)}'\n"
        f"Please verify that your data folder exists right next to this script!"
    )

# Load the data and clean hidden whitespace from column headers
df = pd.read_csv(FULL_CSV_PATH)
df.columns = df.columns.str.strip()

match_sentences = []

# Loop through each row and map variables strictly into your format template
for idx, row in df.iterrows():
    team1 = str(row['Team 1 Name']).strip()
    team2 = str(row['Team 2 Name']).strip()
    venue = str(row['Venue']).strip()
    date = str(row['Match Date']).strip()
    result = str(row['Match Result']).strip()
    scorer = str(row['Top Scorer']).strip()
    runs = str(row['Score']).strip()
    
    # Strictly applying your layout: <team1> vs <team2> at <place> on <date>. <result>. Top scorer: <Name> with <number> runs.
    sentence = f"{team1} vs {team2} at {venue} on {date}. {result}. Top scorer: {scorer} with {runs} runs."
    match_sentences.append(sentence)

print(f"Successfully compiled {len(match_sentences)} match narrative records.")

print("\n=== Step 2: Generating Vector Embeddings ===")
model = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = model.encode(match_sentences)
print(f"Embedding matrix signature generated successfully: {doc_embeddings.shape}")

print("\n=== Step 3: Storing Data into Vector DB (ChromaDB) ===")
chroma_client = chromadb.Client()

# FIXED: Safely retrieve or create the collection to prevent memory registry dropping
collection = chroma_client.get_or_create_collection(name="my_collection")

# Clean out any old remaining documents from prior session runs without destroying the collection mapping
try:
    existing_items = collection.get()
    if existing_items and existing_items['ids']:
        collection.delete(ids=existing_items['ids'])
except Exception:
    pass

# Prepare text lists, vector matrices, and required text ID markers for storage
string_ids = [f"id_{i}" for i in range(len(match_sentences))]

# Convert document embedding array format safely into regular python float lists for ChromaDB
embeddings_list = doc_embeddings.tolist()

# Write the data records directly to ChromaDB using our custom generated vectors
collection.add(
    embeddings=embeddings_list,
    documents=match_sentences,
    ids=string_ids
)
print("ChromaDB vector collection compilation complete.")

print("\n=== Step 4: Interactive Semantic Search Engine ===")
print("-------------------------------------------------------------------------")
print("Type your search query below to run a semantic vector comparison lookup.")
print("Examples to try:")
print("  - 'matches where the home team lost'")
print("  - 'big batting performances and huge centuries'")
print("  - 'games played in melbourne'")
print("Type 'exit' or 'quit' to terminate the search engine system interface.")
print("-------------------------------------------------------------------------")

while True:
    user_query = input("\nEnter your search query: ").strip()
    
    # Validation loop exit conditions
    if user_query.lower() in ['exit', 'quit', '']:
        print("Exiting search engine. Goodbye!")
        break
        
    # Vectorize the incoming user input utilizing the same embedding function
    query_vector = model.encode([user_query]).tolist()
    
    # Execute structural database query matching top 3 elements
    results = collection.query(
        query_embeddings=query_vector,
        n_results=min(3, len(match_sentences))
    )
    
    print("\n--- Top Semantically Relevant Matches Found (ChromaDB) ---")
    
    # Parse vector document retrieval objects cleanly down to terminal printing text
    documents = results['documents'][0]
    distances = results['distances'][0] if 'distances' in results and results['distances'] else [0.0]*len(documents)
    
    for rank, (doc, dist) in enumerate(zip(documents, distances), 1):
        # Note: Proximity Margin indicates distance metric alignment (closer to 0.0 is a stronger match)
        print(f"\n[Rank {rank}] (Distance Proximity: {dist:.4f})")
        print(f"  {doc}")
    print("-" * 73)
