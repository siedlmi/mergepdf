import argparse
import os
import logging
from PyPDF2 import PdfMerger
from importlib.metadata import version, PackageNotFoundError

logging.basicConfig(level=logging.INFO)

def get_pdfs_from_folder(folder, recursive=False, sort_by="filename", custom_order=None):
    pdfs = []
    walk_fn = os.walk if recursive else lambda f: [(f, [], os.listdir(f))]
    for root, _, files in walk_fn(folder):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, f))
    return sort_pdfs(pdfs, sort_by, custom_order)

def sort_pdfs(pdfs, sort_by, custom_order=None):
    if sort_by == "modified":
        return sorted(pdfs, key=os.path.getmtime)
    elif sort_by == "filesize":
        return sorted(pdfs, key=os.path.getsize)
    elif sort_by == "pagenumber":
        from PyPDF2 import PdfReader
        def get_page_count(f):
            try:
                return len(PdfReader(f).pages)
            except Exception:
                return float("inf")
        return sorted(pdfs, key=get_page_count)
    elif sort_by == "custom" and custom_order:
        files_found = {os.path.basename(f): f for f in pdfs}
        return [files_found[name] for name in custom_order if name in files_found]
    return sorted(pdfs)

def merge_pdfs(pdf_list, output, dry_run=False):
    if not pdf_list:
        logging.warning("No PDF files found to merge.")
        return

    if dry_run:
        logging.info("[Dry Run] The following PDF files would be merged:")
        for pdf in pdf_list:
            logging.info(f"  - {pdf}")
        logging.info(f"[Dry Run] Output file would be: {output}")
        return

    merger = PdfMerger()
    for pdf in pdf_list:
        try:
            logging.info(f"Adding: {pdf}")
            merger.append(pdf)
        except Exception as e:
            logging.warning(f"Skipping '{pdf}' due to error: {e}")

    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    merger.write(output)
    merger.close()
    logging.info(f"Merged PDF saved as: {output}")

def main():
    try:
        pkg_version = version("mergepdf")
    except PackageNotFoundError:
        pkg_version = "unknown"

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
    parser.add_argument(
        "--sort-by",
        choices=["filename", "modified", "filesize", "pagenumber", "custom"],
        default="filename",
        help="Sort PDF files by: filename (default), modified, filesize, pagenumber, or custom"
    )
    parser.add_argument(
        "--custom-order",
        nargs="+",
        help="List of filenames in custom sort order (used only if --sort-by=custom)"
    )
    parser.add_argument(
        "--order-file",
        help="Path to a text file listing PDF filenames in custom sort order (one per line)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {pkg_version}",
        help="Show the version of this program and exit"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.isdir(args.folder):
        logging.error(f"{args.folder} is not a valid directory.")
        return

    custom_order = args.custom_order
    if args.order_file:
        try:
            with open(args.order_file, "r") as f:
                custom_order = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logging.error(f"Error reading order file: {e}")
            return

    pdfs = get_pdfs_from_folder(args.folder, args.recursive, args.sort_by, custom_order)

    output = args.output
    if not output.lower().endswith(".pdf"):
        output += ".pdf"
        logging.debug(f"Adjusted output filename to: {output}")

    merge_pdfs(pdfs, output, args.dry_run)

if __name__ == "__main__":
    main()