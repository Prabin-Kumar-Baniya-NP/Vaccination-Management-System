from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from django.http import FileResponse
import io

def generate_pdf(context):
	"""
	Returns File Response with given context
	"""
	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()
	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(buffer, pagesize=A4)
	p.setTitle(context["pdf_title"])
	# Write the date
	p.drawString(40, 800, context["date"])
	# Draw a line
	p.line(20, 795, 570, 795)
	# Write the title
	p.setFont('Helvetica-Bold', 14)
	p.drawCentredString(300, 750, context["title"])
	# Write the subtitle
	p.setFont('Helvetica', 12)
	p.drawCentredString(300, 700, context["subtitle"])
	# Write the paragraph style
	para_style = ParagraphStyle(
        "paraStyle", fontSize=14, leading=20, firstLineIndent=25)
	# Write the paragraph
	para = Paragraph(context["content"], para_style)
	para.wrapOn(p, 500, 200)  # dimension of paragraph (width, height)
	para.drawOn(p, 40, 600)  # location of paragraph (x, y)
	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()
	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=True, filename=context["pdf_title"] + ".pdf")