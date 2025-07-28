from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import os
import uuid

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        wattpad_url = request.form.get("wattpad_url")
        if not wattpad_url:
            return "Falta la URL de Wattpad, mi ciela."

        story_text, title = scrapear_wattpad(wattpad_url)
        if not story_text:
            return "No se pudo obtener el contenido. Asegúrate de que el link sea válido."

        filename = generar_epub(title, story_text)
        return send_file(filename, as_attachment=True)

    return render_template("index.html")


def scrapear_wattpad(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.find("title").text.strip()
        paragraphs = soup.find_all("p")

        content = "\n\n".join(p.text for p in paragraphs if p.text.strip())
        return content, title
    except Exception as e:
        print("Error al scrapear:", e)
        return None, None


def generar_epub(title, content):
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('es')

    chapter = epub.EpubHtml(title='Chapter 1', file_name='chap_01.xhtml', lang='es')
    chapter.content = f'<html><head></head><body><h1>{title}</h1><div>{content.replace(chr(10), "</p><p>")}</div></body></html>'
    
    book.add_item(chapter)
    book.toc = (epub.Link("chap_01.xhtml", title, "chap_01"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    book.spine = ['nav', chapter]
    
    filename = f"{title.replace(' ', '_')}.epub"
    epub.write_epub(filename, book, {})
    
    return filename


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
