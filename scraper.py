import datetime as dt
import bs4
# import pypdl
import urllib
import requests
from IPython import embed
from lxml import etree
from pyfiglet import Figlet

f = Figlet(font='slant')
print(f.renderText('Natural Antibody'))
print('v. 0.0.1')

def tentar_baixar(url, i, t):
    print("Dis da fáiou:",url)
    print("i:",i)
    print("t:",t.text)
    baixar = input("Baixar (y/n)?")
    if baixar == 'y':
        print("baixar")
        myfile = requests.get(url)
        open('pdf'+str(i).zfill(4)+'_'+t.text+'.pdf', 'wb').write(myfile.content)

def dom_from_url(url):
    # resp = requests.get('https://naturalantibody.com/resources/research-space/'+str(i)+'/')
    resp = requests.get(url)
    bs = bs4.BeautifulSoup(resp.content, "html.parser")
    return etree.HTML(str(bs))

for i in range(1,11):
    dom = dom_from_url('https://naturalantibody.com/resources/research-space/'+str(i)+'/')
    
    titulo = dom.xpath('/html/body/div/div/div/div/ul/li/div/h3/a')
    # print(f.renderText('titulos p.'+str(i).zfill(2)))
    for t in titulo:
        # print(dt.datetime.now())
        # embed()
        link = t.get('href')
        # print(link)
        if '.pdf' in link or 'pdf?id=' in link:
            tentar_baixar(link,i,t)
            # myfile = requests.get(link)
            # open('pdf'+str(i).zfill(4)+'_'+t.text+'.pdf', 'wb').write(myfile.content)
            # urllib.request.urlretrieve(link, 'pdf'+str(i)+'.pdf')
        else:
            # get page
            resp2 = requests.get(link)
            bs2 = bs4.BeautifulSoup(resp2.content, "html.parser")
            # dom2 = etree.HTML(str(bs2))
            links = bs2.find_all('a')
            for l in links:
                if '.pdf' in l or 'pdf?id=' in l:  # l.endswith('.pdf'):
                    tentar_baixar(link,i,t)
                    # myfile = requests.get(link)
                    # open('pdf'+str(i).zfill(4)+'_'+t.text+'.pdf', 'wb').write(myfile.content)
