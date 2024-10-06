# passifypdf
Use passifypdf to protect your PDF files with a password of your choice. 
Same as encrypt or lock your PDF via a password.

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

## Usage via CLI:

```
python encryptpdf.py
```

Sample Run:
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

## Before & After:
<img width="1534" alt="Pasted Graphic 100" src="https://github.com/user-attachments/assets/ee2ead62-6480-4312-af8b-762ec240cc10">

## Known Issues
If you have nay special chars(example: an emoji like Star 🌟) in the PDF file, it gives a minor complain during execution. 
But it still does the job, so you can ingore that "char or object error" which you see in the output.

## Note:
In general you can use passifypdf to protect your PDF files against an opportunistic attacker. 
But you should not rely on this for mission-critical data.
