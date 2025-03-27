# mergepdf

**mergepdf** is a simple command-line utility that merges all PDF files in a specified folder into a single PDF. It's fast, easy to use, and ideal for automating document workflows.

---

## 🚀 Features

- Merge all `.pdf` files in a folder
- Automatically sorts files alphabetically
- Simple CLI interface
- Lightweight with minimal dependencies

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

| Argument |	Description|
|---|---|
|folder	| (Required) Path to folder containing PDFs|
|-o, --output	| Name of the output file (default: merged.pdf)|

### Example
```bash
mergepdf ./documents/ -o final-report.pdf
```


⸻

### 🧾 Requirements
	•	Python 3.7+
	•	PyPDF2

Dependencies are automatically installed during pip install.

⸻

## 🔒 License

This project is licensed under the MIT License.




