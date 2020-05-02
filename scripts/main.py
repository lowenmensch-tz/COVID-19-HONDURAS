import generate_links
import generate_pdf
import text_analysis
import subprocess
import os 

if __name__ == "__main__":
    py = ['generate_links.py', 'generate_pdf.py', 'text_analysis.py']

    if len(set(py).intersection(set(os.listdir()))) == 3: 

        subprocess.run(["python", "generate_links.py"])
        subprocess.run(["python", "generate_pdf.py"])
        subprocess.run(["python", "text_analysis.py"])

    else: 
        print("No se pudo ejecutar el script, falta un archivo.")
