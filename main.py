from flask import Flask, request, render_template_string, send_file
import requests
from bs4 import BeautifulSoup
from xhtml2pdf import pisa
import uuid
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <div>
    {% for p in content %}
        <p>{{ p }}</p>
    {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        wattpad_url = request.form.get("wattpad_url")
        if not wattpad_url:
            return "Falta la URL de Wattpad, mi ciela."

        story_text, title = scrapear_wattpad(wattpad_url)
        if not story_text:
            return "No se pudo obtener el contenido. Asegúrate de que el link sea válido."

        pdf_filename = generar_pdf(title, story_text)
        return send_file(pdf_filename, as_attachment=True)

    return '''
        <form method="post">
            <label for="wattpad_url">Pega la URL de Wattpad:</label><br>
            <input type="text" name="wattpad_url" style="width:400px;">
            <input type="submit" value="Descargar PDF">
        </form>
    '''

def scrapear_wattpad(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.find("title").text.strip()
        paragraphs = soup.find_all("p")

        content = [p.text.strip() for p in paragraphs if p.text.strip()]
        return content, title
    except Exception as e:
        print("Error al scrapear:", e)
        return None, None

def generar_pdf(title, content_list):
    html = render_template_string(HTML_TEMPLATE, title=title, content=content_list)
    filename = f"{title.replace(' ', '_')}.pdf"
    
    with open(filename, "w+b") as result_file:
        pisa.CreatePDF(html, dest=result_file)
    
    return filename

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
