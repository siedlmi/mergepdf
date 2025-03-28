import os
from pathlib import Path
from mergepdf.cli import merge_pdfs

def test_merge_creates_output_file(tmp_path):
    pdf1 = tmp_path / "a.pdf"
    pdf2 = tmp_path / "b.pdf"
    output = tmp_path / "merged.pdf"

    # Write minimal valid PDF content
    pdf1.write_bytes(b"%PDF-1.4\n%%EOF")
    pdf2.write_bytes(b"%PDF-1.4\n%%EOF")

    merge_pdfs([str(pdf1), str(pdf2)], str(output))
    assert output.exists()
    assert output.stat().st_size > 0

def test_merge_skips_invalid_files(tmp_path):
    valid = tmp_path / "valid.pdf"
    invalid = tmp_path / "broken.pdf"
    output = tmp_path / "merged.pdf"

    valid.write_bytes(b"%PDF-1.4\n%%EOF")
    invalid.write_text("This is not a PDF")

    merge_pdfs([str(valid), str(invalid)], str(output))
    assert output.exists()
    assert output.stat().st_size > 0
