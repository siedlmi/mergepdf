"""Merge PDF files from a specified folder, with options for sorting and custom order.

This tool allows users to merge multiple PDF files from a directory, with options for recursive searching, sorting by various criteria, and defining a custom order for the files to be merged.
"""

import argparse
import os
import logging
from PyPDF2 import PdfReader, PdfMerger
import getpass
from importlib.metadata import version, PackageNotFoundError

logging.basicConfig(level=logging.INFO)

def get_pdfs_from_folder(folder, recursive=False, sort_by="filename", custom_order=None, reverse=False):
    """
    Retrieve a list of PDF files from the specified folder.

    Parameters:
        folder (str): The path to the folder containing PDF files.
        recursive (bool): Whether to search subfolders recursively.
        sort_by (str): The method to sort the PDF files (filename, modified, filesize, pagenumber, custom).
        custom_order (list): A list of filenames for custom sorting.
        reverse (bool): Whether to reverse the sort order.

    Returns:
        list: A sorted list of PDF file paths.
    """
    pdfs = []
    walk_fn = os.walk if recursive else lambda f: [(f, [], os.listdir(f))]
    for root, _, files in walk_fn(folder):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, f))
    return sort_pdfs(pdfs, sort_by, custom_order, reverse)

def sort_pdfs(pdfs, sort_by, custom_order=None, reverse=False):
    """
    Sort a list of PDF file paths based on the specified criteria.

    Parameters:
        pdfs (list): A list of PDF file paths.
        sort_by (str): The method to sort the PDF files.
        custom_order (list): A list of filenames for custom sorting.
        reverse (bool): Whether to reverse the sort order.

    Returns:
        list: A sorted list of PDF file paths.
    """
    if sort_by == "modified":
        return sorted(pdfs, key=os.path.getmtime, reverse=reverse)
    elif sort_by == "filesize":
        return sorted(pdfs, key=os.path.getsize, reverse=reverse)
    elif sort_by == "pagenumber":
        def get_page_count(f):
            try:
                return len(PdfReader(f).pages)
            except Exception:
                return float("inf")
        return sorted(pdfs, key=get_page_count, reverse=reverse)
    elif sort_by == "custom" and custom_order:
        files_found = {os.path.basename(f): f for f in pdfs}
        return [files_found[name] for name in custom_order if name in files_found]
    return sorted(pdfs, reverse=reverse)

def merge_pdfs(pdf_list, output, dry_run=False):
    """
    Merge a list of PDF files into a single PDF file.

    Parameters:
        pdf_list (list): A list of PDF file paths to merge.
        output (str): The path for the output merged PDF file.
        dry_run (bool): If True, only log the files that would be merged without performing the merge.

    Returns:
        None
    """
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
            reader = PdfReader(pdf)
            if reader.is_encrypted:
                password = getpass.getpass(prompt=f"Enter password for '{pdf}': ")
                try:
                    reader.decrypt(password)
                except Exception as e:
                    logging.warning(f"Skipping '{pdf}' due to decryption error: {e}")
                    continue
            logging.info(f"Adding: {pdf}")
            merger.append(reader)
        except Exception as e:
            logging.warning(f"Skipping '{pdf}' due to error: {e}")

    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    merger.write(output)
    merger.close()
    logging.info(f"Merged PDF saved as: {output}")

def read_order_file(path):
    """
    Read a text file and return a list of filenames for custom sorting.

    Parameters:
        path (str): The path to the text file containing filenames.

    Returns:
        list: A list of filenames if successfully read, None otherwise.
    """
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Error reading order file: {e}")
        return None

def parse_args(pkg_version: str) -> argparse.Namespace:
    """
    Parse command line arguments.

    Parameters:
        pkg_version (str): The version of the package.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="""Merge all PDF files in a folder.

Examples:
  mergepdf ./pdfs -o combined.pdf
  mergepdf ./docs --recursive --sort-by modified
  mergepdf ./invoices --sort-by custom --custom-order A.pdf B.pdf
  mergepdf ./reports --order-file order.txt -o final.pdf
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    input_group = parser.add_argument_group("Input options")
    input_group.add_argument("folder", help="Path to the folder containing PDF files to merge")
    input_group.add_argument("--recursive", action="store_true", help="Recursively search subfolders for PDF files")

    sorting_group = parser.add_argument_group("Sorting options")
    sorting_group.add_argument("--sort-by", choices=["filename", "modified", "filesize", "pagenumber", "custom"],
                               default="filename", help="Sort PDF files by the selected method")
    sorting_group.add_argument("--custom-order", nargs="+", help="List of filenames in custom sort order (use with --sort-by custom)")
    sorting_group.add_argument("--order-file", help="Path to a text file listing filenames for custom sort order")
    sorting_group.add_argument("--reverse", action="store_true", help="Reverse the sort order")

    output_group = parser.add_argument_group("Output options")
    output_group.add_argument("-o", "--output", default="merged.pdf", help="Name of the output merged PDF file")

    misc_group = parser.add_argument_group("Other options")
    misc_group.add_argument("--dry-run", action="store_true", help="Preview the files to be merged without creating output")
    misc_group.add_argument("--verbose", action="store_true", help="Enable verbose output")
    misc_group.add_argument("--version", action="version", version=f"%(prog)s {pkg_version}",
                            help="Show the version of this program and exit")

    return parser.parse_args()

def main():
    """
    The main entry point of the script.

    Parses command line arguments, retrieves PDF files, and performs the merge operation.

    Returns:
        int: Exit status code (0 for success, 1 for failure).
    """
    try:
        pkg_version = version("mergepdf")
    except PackageNotFoundError:
        pkg_version = "unknown"

    args = parse_args(pkg_version)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.isdir(args.folder):
        logging.error(f"{args.folder} is not a valid directory.")
        return 1

    custom_order = args.custom_order
    if args.order_file:
        custom_order = read_order_file(args.order_file)
        if custom_order is None:
            return 1

    pdfs = get_pdfs_from_folder(args.folder, args.recursive, args.sort_by, custom_order, args.reverse)

    output = args.output
    if not output.lower().endswith(".pdf"):
        output += ".pdf"
        logging.debug(f"Adjusted output filename to: {output}")

    merge_pdfs(pdfs, output, args.dry_run)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())