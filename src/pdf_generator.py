from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from formulas import *


# -------------------------------------------------------------------------------------------------- #

def getPdf(pdf_filename:str,
                 premium:float,
                 lost:float,
                 res_with_insurance:float,
                 res_without_insurance:float,
                 pl_bar:float,
                 C_f:float,
                 CA:float,
                 start_date:date,
                 end_date:date,
                 year_benchmark:int):
    
    # 📄 Création du document PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter  # Dimensions de la page

    # 📌 Ajouter un titre centré
    title = "Devis d'Assurance"
    c.setFont("Helvetica-Bold", 16)
    text_width = c.stringWidth(title, "Helvetica-Bold", 16)
    c.drawString((width - text_width) / 2, height - 50, title)  # Centrer le titre

    # 🔹 Données du tableau (libellé + valeur en €)
    data = [
        ["Données Financières", "Unité"],  # En-tête
        ["Premium", f"{premium} €"],
        ["Pertes sur l'année", f"{lost} €"],
        ["Résultat Net d'Assurance", f"{res_with_insurance} €"],
        ["Résultat Sans Assurance", f"{res_without_insurance} €"],
        ["Niveau de Pluie Pivot", f"{pl_bar} mm"],
        ["Coût Fixe Journalier", f"{C_f} €"],
        ["Chiffre d'Affaire Journalier Max", f"{CA} €"]
    ]


    # 🔹 Création du tableau avec deux colonnes
    col_widths = [250, 150]  # Largeur des colonnes
    table = Table(data, colWidths=col_widths)

    # 🔹 Style du tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # En-tête en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texte blanc pour l'en-tête
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Tout centrer
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Police en gras pour l'en-tête
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Taille du texte
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Espace sous l'en-tête
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Bordures noires
    ])
    table.setStyle(style)

    # 🔹 Centrer le tableau sur la page
    table_x = (width - sum(col_widths)) / 2  # Position X centrée
    table_y = height - 250  # Ajuster la position verticale

    # 🔹 Dessiner le tableau sur la page
    table.wrapOn(c, width, height)
    table.drawOn(c, table_x, table_y)

    # 📌 Ajouter une note de fin sous le tableau
    note = f"📌 Le premium a été généré sur la base des données climatiques enregistrées entre le {start_date.strftime('%d/%m/%Y')} et le {end_date.strftime('%d/%m/%Y')}"
    c.setFont("Helvetica", 10)
    note_width = c.stringWidth(note, "Helvetica", 10)
    c.drawString((width - note_width) / 2, table_y - 50, note)  # Centrer le texte sous le tableau

    # 🔹 Sauvegarde du PDF
    c.save()
    print(f"✅ PDF généré avec succès : {pdf_filename}")

# 🔹 Exécuter la fonction
getPdf("devis.pdf",2000,9000,10000,6000,10,1000,100,date(2024,1,1),date(2024,12,31),2022)
