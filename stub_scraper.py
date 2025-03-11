import bs4
import torch
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
print('This little guy pulls the thingies on each paper.')
print()

textos = []
embos = []

for i in range(1,11):
    resp = requests.get('https://naturalantibody.com/resources/research-space/'+str(i)+'/')
    bs = bs4.BeautifulSoup(resp.content, "html.parser")
    dom = etree.HTML(str(bs))

    data = dom.xpath('/html/body/div/div/div/div/ul/li/div/p')
    # print(f.renderText('data'))
    for d in data:
        # print(d.text)
        pass
        # não vou pegar embeddings desses caras...
    titulo = dom.xpath('/html/body/div/div/div/div/ul/li/div/h3/a')
    # print(f.renderText('titulo'))
    for t in titulo:
        # print(t.text)
        textos.append(t.text)
        a = ollama.embed(
            model='mxbai-embed-large',
            input=t.text,
            )
        # print(a)
        embos.append(a)
    
    keys = dom.xpath('/html/body/div/div/div/div/ul/li/div/ul/li/span')
    # print(f.renderText('keys'))
    for s in keys:
        # print(s.text)
        textos.append(s.text)
        a = ollama.embed(
            model='mxbai-embed-large',
            input=s.text,
            )
        # print(a)
        embos.append(a)
    assert len(textos)==len(embos)

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
# Get the corresponding context from the vault
relevant_context = [textos[idx].strip() for idx in top_indices]
print(relevant_context)

print()