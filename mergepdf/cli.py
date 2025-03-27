import argparse
import os
from PyPDF2 import PdfMerger

def get_pdfs_from_folder(folder, recursive=False):
    pdfs = []
    if recursive:
        for root, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(".pdf"):
                    pdfs.append(os.path.join(root, f))
    else:
        pdfs = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith(".pdf")
        ]
    return sorted(pdfs)

def merge_pdfs(pdf_list, output, dry_run=False):
    if not pdf_list:
        print("No PDF files found to merge.")
        return

    if dry_run:
        print("[Dry Run] The following PDF files would be merged:")
        for pdf in pdf_list:
            print(f"  - {pdf}")
        print(f"[Dry Run] Output file would be: {output}")
        return

    merger = PdfMerger()
    for pdf in pdf_list:
        print(f"Adding: {pdf}")
        merger.append(pdf)

    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

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
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively search subfolders for PDF files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the PDF files that would be merged without creating an output file",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Error: {args.folder} is not a valid directory.")
        return

    pdfs = get_pdfs_from_folder(args.folder, args.recursive)
    merge_pdfs(pdfs, args.output, args.dry_run)

if __name__ == "__main__":
    main()