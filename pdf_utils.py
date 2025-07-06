from fpdf import FPDF
import os

def generate_rfq_pdf(legal_entity_id, item_types, descriptions, quantities):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Request for Quotation (RFQ)", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Legal Entity ID: {legal_entity_id}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Item Type", 1)
    pdf.cell(80, 10, "Description", 1)
    pdf.cell(30, 10, "Quantity", 1)
    pdf.ln()

    pdf.set_font("Arial", '', 12)
    for i in range(len(item_types)):
        pdf.cell(50, 10, item_types[i], 1)
        pdf.cell(80, 10, descriptions[i], 1)
        pdf.cell(30, 10, str(quantities[i]), 1)
        pdf.ln()

    filename = f"rfq_{legal_entity_id}.pdf"
    filepath = os.path.join("private_pdfs", filename)
    pdf.output(filepath)
    return filename
