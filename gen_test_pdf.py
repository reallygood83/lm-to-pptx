from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape

def create_test_pdf(filename="test_slides.pdf"):
    c = canvas.Canvas(filename, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Slide 1
    c.setFont("Helvetica-Bold", 30)
    c.drawString(100, height - 100, "Project Overview")
    c.setFont("Helvetica", 20)
    c.drawString(100, height - 200, "1. Core Objective: PDF to PPTX")
    c.drawString(100, height - 250, "2. AI Integration: Gemini, OpenAI")
    c.drawString(100, height - 300, "3. Status: Testing Phase")
    c.showPage()
    
    # Slide 2
    c.setFont("Helvetica-Bold", 30)
    c.drawString(100, height - 100, "Next Steps")
    c.setFont("Helvetica", 20)
    c.drawString(100, height - 200, "• Verify Image Conversion")
    c.drawString(100, height - 250, "• Check CLI Arguments")
    c.drawString(100, height - 300, "• Validate PPTX Output")
    c.showPage()
    
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_test_pdf()
