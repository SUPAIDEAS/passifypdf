from pypdf import PdfReader, PdfWriter

def encrypt_pdf(input_pdf, output_pdf, password):

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Add all pages from the reader to the writer
    for page_num in range(len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    # Encrypt with a password
    writer.encrypt(password)

    # Write the encrypted PDF to a new PDF file passed as param
    with open(output_pdf, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    input_pdf = "Sample_PDF.pdf"   # <--- Replace with the path to your input PDF
    output_pdf = "Sample_PDF_protected.pdf"  # <--- Replace with the output file name
    password = "pass111"   # <--- Replace with your own choice of password

    encrypt_pdf(input_pdf, output_pdf, password)
    print(f"Congratulations!\nPDF file encrypted successfully and saved as '{output_pdf}'")
