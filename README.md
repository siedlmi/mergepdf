# mergepdf

**mergepdf** is a simple command-line utility that merges all PDF files in a specified folder into a single PDF. It's fast, easy to use, and ideal for automating document workflows.

---

## 🚀 Features

- Merge all `.pdf` files in a folder (with optional recursion)
- Supports multiple sort options: filename, modification date, file size, and page count
- Skip corrupted PDF files during merge
- Preview files before merging with a dry-run mode
- Specify custom output paths (directories + filenames)

---

## 📦 Installation

Clone the repository and install using `pip`:

```bash
git clone https://github.com/yourusername/mergepdf.git
cd mergepdf
pip install .
```
After installation, the command mergepdf will be available in your terminal.

⸻

## 🛠 Usage

```bash
mergepdf /path/to/pdf/folder -o output.pdf
```

### Arguments

| Argument        | Description                                             |
|-----------------|---------------------------------------------------------|
| folder          | (Required) Path to folder containing PDFs               |
| -o, --output    | Name of the output file (default: merged.pdf)          |
| --recursive      | Recursively search subfolders for PDF files            |
| --dry-run       | Preview which files would be merged without creating output |
| --sort-by       | Sort files by: name (default), modified, filesize, or pagenumber |

### Example
```bash
mergepdf ./documents/ --recursive --sort-by pagenumber --dry-run -o output/combined.pdf
```

⸻

### 🧾 Requirements
	•	Python 3.7+
	•	PyPDF2
    •   pycryptodome

Dependencies are automatically installed during pip install.

⸻

## 🔒 License

This project is licensed under the MIT License.