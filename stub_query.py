import bs4
import torch
import pickle
import ollama
import requests
from IPython import embed
from lxml import etree
from pyfiglet import Figlet
from sentence_transformers import SentenceTransformer, util


f = Figlet(font='slant')
print(f.renderText('Natural Antibody'))
print('v. 0.0.1')

print()
print('This little guy reads the pickle file, and allows you to query it..')
print()


with open("stubs.pkl", "rb") as handle:
    dps = pickle.load(handle)
textos = dps['textos']
embos = dps['embos']

promptacao = input("Dê-me seu prompt:")

# model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode the user input
# input_embedding = model.encode([promptacao])
input_embedding = ollama.embed(
    model='mxbai-embed-large',
    input=promptacao,
)

# embed()
cos_scores = []
for e in embos:
# Compute cosine similarity between the input and vault embeddings
    # cos_scores = util.cos_sim(input_embedding["embeddings"], e["embeddings"])[0]
    cos_scores.append(util.cos_sim(input_embedding["embeddings"], e["embeddings"])[0])
# Adjust top_k if it's greater than the number of available scores
top_k = min(3, len(cos_scores))
# Sort the scores and get the top-k indices
top_indices = torch.topk(torch.Tensor(cos_scores), k=top_k)[1].tolist()
print("top indices")
print(top_indices)
# Get the corresponding context from the vault
relevant_context = [textos[idx].strip() for idx in top_indices]
print("relevant context")
print(relevant_context)

print()