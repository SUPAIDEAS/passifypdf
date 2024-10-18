import argparse

def get_parser():
    parser = argparse.ArgumentParser(description=("Encrypt a PDF file with a password of your choice."), epilog=("For more information, visit: https://github.com/SUPAIDEAS/passifypdf"))
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("-i", "--input", required=True, help="path to the input pdf file")
    parser.add_argument("-o", "--output", required=True, help="path to the output encrypted pdf file")
    parser.add_argument("-p", "--passwd", required=True, type=str, help="password to encrypt the pdf file")
    return parser