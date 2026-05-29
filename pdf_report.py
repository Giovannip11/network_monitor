from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle

from reportlab.lib import colors

import json
import os

from datetime import datetime


def generate_pdf(json_file="data/devices.json"):

    with open(json_file, "r") as f:
        devices = json.load(f)

    
    os.makedirs("history", exist_ok=True)

  
    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    
    pdf_path = f"history/relatorio_{timestamp}.pdf"

    pdf = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    titulo = Paragraph(
        "Relatorio de Monitoramento de Rede",
        styles['Title']
    )

    data = Paragraph(
        f"Gerado em {datetime.now()}",
        styles['Normal']
    )

    elements.append(titulo)
    elements.append(Spacer(1, 20))
    elements.append(data)
    elements.append(Spacer(1, 20))

    tabela = [["IP", "Hostname", "Fabricante", "SO"]]

    for d in devices:
        tabela.append([
            d.get("ip", ""),
            d.get("hostname", ""),
            d.get("vendor", ""),
            d.get("os", "")
        ])

    table = Table(
        tabela,
        colWidths=[90, 120, 140, 140]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
    ]))

    elements.append(table)

    pdf.build(elements)

    print(f"PDF gerado: {pdf_path}")