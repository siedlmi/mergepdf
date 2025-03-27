import argparse
import os
from PyPDF2 import PdfMerger

def get_pdfs_from_folder(folder):
    pdfs = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".pdf")
    ]
    return sorted(pdfs)

def merge_pdfs(pdf_list, output):
    if not pdf_list:
        print("No PDF files found to merge.")
        return

    merger = PdfMerger()
    for pdf in pdf_list:
        print(f"Adding: {pdf}")
        merger.append(pdf)

    merger.write(output)
    merger.close()
    print(f"Merged PDF saved as: {output}")

def main():
    parser = argparse.ArgumentParser(description="Merge all PDF files in a folder.")
    parser.add_argument(
        "folder",
        help="Path to the folder containing PDF files to merge",
    )
    parser.add_argument(
        "-o", "--output",
        default="merged.pdf",
        help="Name of the output merged PDF file (default: merged.pdf)",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Error: {args.folder} is not a valid directory.")
        return

    pdfs = get_pdfs_from_folder(args.folder)
    merge_pdfs(pdfs, args.output)

if __name__ == "__main__":
    main()