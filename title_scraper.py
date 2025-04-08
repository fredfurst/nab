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
print('This little guy pulls the thingies on each paper and saves it to a pickle file.')
print()

textos = []
embos = []

for i in range(1,11):
    resp = requests.get('https://naturalantibody.com/resources/research-space/'+str(i)+'/')
    bs = bs4.BeautifulSoup(resp.content, "html.parser")
    dom = etree.HTML(str(bs))
    # /html/body/div/div[1]/div[4]/div/ul/li[6]/div[1]/h3/a
    # /html/body/div/div[1]/div[4]/div/ul/li[7]/div[1]/h3/a
    titulo = dom.xpath('/html/body/div/div[1]/div[4]/div/ul/li/div[1]/h3/a')
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
    assert len(textos)==len(embos)

dados_pra_salvar = {
    'textos': textos,
    'embos': embos,
}
with open("titles.pkl", "wb") as handle:
    pickle.dump(dados_pra_salvar, handle)
print("hoje nao tem promptacao")
