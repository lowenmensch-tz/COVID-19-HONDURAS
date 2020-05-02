from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def num_pages(soup): 
    return int(re.search("\d+", soup.findAll("li", {"class":"pager-last last"})[0].select("a")[0].get("href"))[0])

#/?q=Comunicados&page=1
def soup(page=""):
    if page == "&page=0": page="" 
    html = urlopen("https://covid19honduras.org/?q=Comunicados{}".format(page))
    return BeautifulSoup(html.read(),"html5lib")

#redirecciones los enlaces
def shortener(tag):
    return (tag.select("iframe")[0].get("src").
                                    replace("//docs.google.com/viewer?embedded=true&url=https%3A", "https:").
                                    replace("%2F", "/")).replace("25", "")

#Diferencia entre enlaces
def compare_new_links(links):
    f = open("links.txt", "r").read().split("\n")
    new_links = list(set(links).difference(set(f)))
    return new_links


#guarda nuevos enlaces en al archivo "links.txt"
def generate_link_files(links): 
    f = open("links.txt", "a")
    for link in links: 
        f.write(str(link)+"\n")
    f.close()   

if __name__ == "__main__":
    links = []
    response = soup() 

    for i in range(0, num_pages(response)+1): 
        div = soup("&page={}".format(i)).findAll("div", {"class":"field-item even"})

        links.append(
            [
                shortener(tag)
                for tag in div 
                if len(tag.select("iframe")) != 0
            ]
        )
    
    if "links" not in os.listdir(): os.mkdir("links")
    os.chdir(os.getcwd()+"/links")
    
    if "links.txt" not in os.listdir(): 
        [
            generate_link_files(link) for link in links
        ]
    else:
        [
            generate_link_files( compare_new_links(link) ) for link in links
        ] 
        
    os.chdir("..")