# About passifypdf
Use passifypdf to protect your PDF files with a password of your choice. Same as encrypt your PDF.

# How to use ?

## Clone
```
git clone git@github.com:SUPAIDEAS/passifypdf.git
```
or 
```
git clone https://github.com/SUPAIDEAS/passifypdf.git
```

## Pull Dependencies (install before usage)

```
pip install -r requirements.txt
```

## Usage

Run the "main" from IDE or from CLI:

```
if __name__ == "__main__":
    ...
```

Run from CLI:

```
change dir to "passifypdf/passifypdf", 

Then run, 
python encryptpdf.py

-------------------------Sample output----------------------
$python encryptpdf.py
Congratulations!
PDF file encrypted successfully and saved as 'Sample_PDF_protected.pdf'

$

```

## Disclaimer
In general you can use passifypdf to protect your PDF files against an opportunistic attacker. 
But do not rely on `passifypdf` or generated password-protected PDF file(s) for mission-critical information.
