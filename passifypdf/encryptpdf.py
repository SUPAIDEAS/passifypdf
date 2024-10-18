from cli import get_parser
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

def main():
    parser = get_parser()
    args = parser.parse_args()
    encrypt_pdf(args.input, args.output, args.passwd)
    print(f"Congratulations!\nPDF file encrypted successfully and saved as '{args.output}'")

if __name__ == "__main__":
    main()