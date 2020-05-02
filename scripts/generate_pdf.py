import requests
import os 
import re

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_filename(link): 
    return link.split("/")[-1]

#Diferencia entre enlaces
def compare_current_pdfs(links):
    url = "https://covid19honduras.org/sites/default/files/"
    current_pdf = [ "{}".format(pdf) for pdf in os.listdir() ]
    new_pdfs = list(set(links).difference(set(current_pdf)))
    return new_pdfs

if __name__ == "__main__":

    try: 
        os.chdir(os.getcwd()+"/links")
        links = open("links.txt").read().split("\n")

        os.chdir("..")
        if "comunicados" not in os.listdir(): os.mkdir("comunicados")
        os.chdir(os.getcwd()+"/comunicados")

        links = compare_current_pdfs(links)

        list_files = os.listdir()

        for link in links:
            if link != "":
                filename = get_filename(link)
                if filename not in list_files:
                    if re.search("C((OMUNICADO)|(omunicado))[%\w._-]+", filename):
                        r = requests.get(link, stream=True, verify=False, allow_redirects=True)
                        open(filename, "wb").write(r.content)

    except OSError as e: 
        print("Mensaje de error: {}".format(e))
