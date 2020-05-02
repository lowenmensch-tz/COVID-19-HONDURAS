#https://pypi.org/project/PyMuPDF/
import fitz
import re 
import os 

def cases_coronavirus(page, date, regex):
    cases = re.findall(regex, page)
    return [ "{}, {}".format(clean_sentence(data), clean_sentence(date)) for data in cases] if len(cases) > 0 else "0"

def get_date(page):
    regex = re.findall("\d+ [a-zA-Z, ]+ 2020", page)  
    return regex[0].replace(",", "").strip() if len(regex) > 0 else "Sin fecha"

def change_root(folder_name):
    if folder_name not in os.listdir(): os.mkdir(folder_name)
    os.chdir(os.getcwd()+"/{}".format(folder_name))

def clean_text(pages): 
    return [page.replace("\n", "") for page in pages]

#espacios en blanco, ':', ','
def clean_sentence(sentence):
    return " ".join([x for x in sentence.split(" ") if x!=""]).replace(":", "").replace(",", "").replace(".", "").strip()

def create_file(array_text, filename):
    f = open(filename+".txt", "a")
    f.write("\n".join(array_text)) if len(array_text) != 1 else f.write("\n{}\n".format(array_text[0]))
    f.close()

def create_file_by_dates(cases, date):
    for i in range(len(cases)):
            create_file(cases[i], "{}".format(date[i].replace(" ", "-")))

def txt(positive, recovered, deaths, date):
    os.chdir( ".." )
    change_root("archived_daily_case_updates")
    change_root("case_positive_updates")
    
    create_file_by_dates(positive, date)

    os.chdir( ".." )
    change_root("case_recovered_updates")

    create_file_by_dates(recovered, date)


    os.chdir( ".." )
    change_root("case_death_updates")

    create_file_by_dates(deaths, date)

def extract_text_pdf(filename):
    try: 
        pdf_file = fitz.open(filename)
        pages = []

        for page in pdf_file: 
            text = page.getText()
            pages.append(text)

        pages = clean_text(pages)
        text = "".join(pages)

        return text
    except RuntimeError as e: 
        print("Error al leer pdf: {}".format(e))

if __name__ == "__main__":
    try:
        os.chdir(os.getcwd()+'/comunicados')
        filenames =  [filenames for dirpath, dirnames, filenames in os.walk(os.getcwd())] 

        text = []
        date = []
        for i in range(len(filenames[0])): 
            text.append( [ extract_text_pdf(filenames[0][i]) ] )
            if text[i][0] == None: 
                text[i][0] = "Sin informacion"
            date.append(get_date("".join(text[i])))

        positive = []
        recovered = []
        deaths = []

        #cases_coronavirus(page, date, regex)
        for i in range(len(text)):
            if text[i] != None:
                positive.append( cases_coronavirus(text[i][0], date[i], "Paciente \d+:? [a-zA-Zñ \d,áéíóú()]+ [A-Z][a-záéíó]+.?") )
                deaths.append( cases_coronavirus(text[i][0], date[i], "Deceso #\d+: [a-zA-Zñ \d,.áéíóú]+") )
                recovered.append( cases_coronavirus(text[i][0], date[i], "de \d+ pacientes") )

        txt(positive, recovered, deaths, date)

    except OSError as e:
        print("Se detuvo la ejecución; mensaje de error: {}".format(e.errno))
    """
    except TypeError as e: 
        print("Error al leer arhivo: {}".format(e))
    """