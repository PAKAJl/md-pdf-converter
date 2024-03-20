from markdown import markdown
from xhtml2pdf import pisa
from os import path
import os
import shutil
from typing import Optional, List
from pathlib import Path
import sys
from markdown.extensions.tables import TableExtension

# Должна быть в файле, на месте пути к шрифтам
PLACEHOLDER = "<--!-->"
DEFAULT_FONT = "Roboto-Regular.ttf"
PATH_MD_FILES = '/Users/pakajl/ObsidainVault/Robocode/Планы уроков'
PATH_PDF_FILES = '/Users/pakajl/Планы УроковPy'
STYLE_PATH = '/Users/pakajl/Projects/Python/md-pdf-converter-master/style.html'
FONT_PATH = '/Users/pakajl/Projects/Python/md-pdf-converter-master/Roboto-Regular.ttf'



def convert_md_to_pdf(
    md_path: str,
    style_path: str,
    pdf_path: str,
    font_path: str,
    pdf_name: Optional[str]=None
) -> str:
    """
    Функция для создания pdf из MD файла
    """

    style_file = Path(style_path)

    if style_file.exists():
        with open(style_file, "r") as file:
            style = file.read()
    else:
        return "Не найден файл стилей!"

    font_file = Path(font_path)

    if font_file.exists():
        style = style.replace(PLACEHOLDER, str(font_file.absolute()))
    else:
        return "Не найден файл шрифтов!"

    md_file = Path(md_path)

    if pdf_name is None:
        pdf_name = md_file.parts[-1]
        pdf_file = Path(pdf_path + pdf_name + ".pdf")
        
    else:
        print(Path(pdf_path.split('.md')[0] + '.pdf'))
        pdf_file = Path(pdf_path.split('.md')[0] + '.pdf')

    if md_file.exists():
        with open(md_file, "r", encoding="utf-8") as file:
            html = style +'<h1>'+ pdf_name + '</h1>'+ markdown(file.read(), extensions=[TableExtension(use_align_attribute=True), 'fenced_code'])
    else:
        return "Не найден файл для конвертации!"

    
    with open(pdf_file, "w+b") as file:
        pisa.CreatePDF(
            html.encode("utf-8"),
            encoding="utf-8",
            dest=file
        )

    return ""


def main():
    parse_from_dir()

def parse_from_dir():
    if path.exists(PATH_PDF_FILES):
        shutil.rmtree(PATH_PDF_FILES)
    os.mkdir(PATH_PDF_FILES)
    dirs = []
    dirs += os.listdir(PATH_MD_FILES)
    for dir in dirs:
        if (dir != '.DS_Store'):
            dir_pdf_path = PATH_PDF_FILES+ '/' + dir
            dir_md_path = PATH_MD_FILES + '/' + dir
            os.mkdir(dir_pdf_path)
            for file in os.listdir(dir_md_path):
                
                convert_md_to_pdf(
                    dir_md_path + '/' + file, #путь к md файлу
                    STYLE_PATH,               #путь к файлу стилей
                    dir_pdf_path+ '/' + file, #путь, куда сохранить исходный файл
                    FONT_PATH,                #путь, шрифту
                    pdf_name=file.split('.md')[0] + '.pdf'
                )   
                        

if __name__ == "__main__":
    main()
