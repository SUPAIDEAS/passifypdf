import argparse


def get_arg_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(
        description="Encrypt a PDF file with a password of your choice.",
        epilog="For more information, visit: https://github.com/SUPAIDEAS/passifypdf"
    )
    arg_parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    arg_parser.add_argument("-i", "--input", required=True, help="Path to the input PDF file to be encrypted")
    arg_parser.add_argument("-o", "--output", required=True, help="Path where the encrypted PDF file will be saved")
    arg_parser.add_argument("-p", "--passwd", required=True, type=str, help="Password to encrypt the PDF file with")
    return arg_parser