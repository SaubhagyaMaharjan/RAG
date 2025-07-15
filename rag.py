import sys
import os
import ollama
import numpy as np
import pickle
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python ingest.py kanun.txt")
    sys.exit(1)

input_file = sys.argv[1]

# Load dataset
with open(input_file, 'r', encoding='utf-8') as file:
    full_text = file.read()
print(f"Loaded file size: {len(full_text)} characters")

CHUNK_SIZE = 1000  # target chunk size

# Split into paragraphs (or you can use sentence splitting)
paragraphs = re.split(r'\n\s*\n', full_text)  # split on empty lines

# Group paragraphs into chunks near the target size
dataset = []
current_chunk = ""
for para in paragraphs:
    para = para.strip()
    if not para:
        continue
    if len(current_chunk) + len(para) + 1 <= CHUNK_SIZE:
        current_chunk += para + "\n"
    else:
        dataset.append(current_chunk.strip())
        current_chunk = para + "\n"

if current_chunk:
    dataset.append(current_chunk.strip())

print(f'Split text into {len(dataset)} chunks (avg size: {sum(len(c) for c in dataset)//len(dataset)} chars)')

# Embedding model
EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'

# Build vector DB
VECTOR_DB = []
for i, chunk in enumerate(dataset):
    response = ollama.embed(model=EMBEDDING_MODEL, input=chunk)
    embedding = np.array(response['embedding']) if 'embedding' in response else np.array(response['embeddings'][0])
    VECTOR_DB.append((chunk, embedding))
    print(f'Embedded {i+1}/{len(dataset)} chunks')

# Save vector DB
vector_db_file = Path(input_file).with_suffix('.pkl')
with open(vector_db_file, 'wb') as f:
    pickle.dump(VECTOR_DB, f)

print(f"Saved vector database to {vector_db_file}")
