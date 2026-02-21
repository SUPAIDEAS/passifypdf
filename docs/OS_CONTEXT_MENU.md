# OS Context Menu Integration

This document explains how to integrate **passifypdf** into your operating system's
right-click context menu so you can encrypt PDFs without opening a terminal.

---

## macOS — Automator Quick Action

1. Open **Automator** (Applications → Automator).
2. Choose **Quick Action** as the document type.
3. Set *Workflow receives current* → **files or folders** in **Finder**.
4. Add a **Run Shell Script** action and paste:

```bash
#!/bin/bash
PASSWORD=$(osascript -e 'Tell application "System Events" to display dialog "Enter encryption password:" default answer "" with hidden answer giving up after 60' -e 'text returned of result')

for f in "$@"; do
    OUTPUT="${f%.pdf}_protected.pdf"
    /usr/local/bin/passifypdf -i "$f" -o "$OUTPUT" -p "$PASSWORD" -f
done

osascript -e 'Tell application "System Events" to display dialog "PDFs encrypted!" giving up after 5'
```

5. Save with a name like **Encrypt PDF with passifypdf**.
6. Right-click any PDF in Finder → **Quick Actions** → **Encrypt PDF with passifypdf**.

> **Note:** Replace `/usr/local/bin/passifypdf` with the output of `which passifypdf` if your shell path differs.

---

## Windows — Send To / Shell Context Menu

### Method A — Add to "Send To"

1. Press `Win+R`, type `shell:sendto`, press Enter.
2. Create a new `.bat` file in that folder:

```bat
@echo off
set /p PASSWORD="Enter password: "
for %%F in (%*) do (
    passifypdf -i "%%F" -o "%%~dpnF_protected.pdf" -p "%PASSWORD%" -f
)
pause
```

3. Right-click any PDF → **Send to** → your script name.

### Method B — Registry Entry (adds to right-click menu)

Create a `.reg` file and double-click to import:

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\EncryptWithPassify]
@="Encrypt PDF with passifypdf"

[HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\EncryptWithPassify\command]
@="cmd.exe /k \"set /p PASSWORD=Enter password: && passifypdf -i \"%1\" -o \"%~dpn1_protected.pdf\" -p \"%PASSWORD%\" -f\""
```

---

## Linux — Nautilus (GNOME Files) Script

1. Create the scripts directory if it doesn't exist:

```bash
mkdir -p ~/.local/share/nautilus/scripts
```

2. Create the script file:

```bash
cat > ~/.local/share/nautilus/scripts/Encrypt\ PDF\ with\ passifypdf << 'EOF'
#!/bin/bash
PASSWORD=$(zenity --password --title="passifypdf" --text="Enter encryption password:")
for f in "$@"; do
    OUTPUT="${f%.pdf}_protected.pdf"
    passifypdf -i "$f" -o "$OUTPUT" -p "$PASSWORD" -f
done
zenity --info --text="PDFs encrypted successfully!"
EOF
chmod +x ~/.local/share/nautilus/scripts/Encrypt\ PDF\ with\ passifypdf
```

3. Right-click a PDF in Files → **Scripts** → **Encrypt PDF with passifypdf**.

> Requires `zenity` (`sudo apt install zenity`) for the password dialog.

---

## KDE / Dolphin (Linux)

1. Open **Settings** → **Configure Dolphin** → **Services**.
2. In the KDE Service Menu Editor (<https://github.com/nicktindall/kde-servicemenus-editor>), add a new entry for `.pdf` files:
   - Name: `Encrypt PDF with passifypdf`
   - Command: `bash -c 'P=$(kdialog --password "Enter password:") && passifypdf -i %F -o "%~dpnF_protected.pdf" -p "$P" -f'`
