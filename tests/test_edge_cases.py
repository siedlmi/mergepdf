import logging
from mergepdf.cli import merge_pdfs

def test_empty_directory(tmp_path, caplog):
    output = tmp_path / "output.pdf"
    with caplog.at_level(logging.WARNING):
        merge_pdfs([], str(output))
        assert "No PDF files found to merge" in caplog.text
        assert not output.exists()

def test_directory_with_non_pdfs(tmp_path, caplog):
    txt = tmp_path / "file.txt"
    md = tmp_path / "readme.md"
    txt.write_text("Text file")
    md.write_text("Markdown file")
    output = tmp_path / "output.pdf"
    with caplog.at_level(logging.WARNING):
        merge_pdfs([], str(output))
        assert "No PDF files found to merge" in caplog.text
        assert not output.exists()

def test_long_filename_pdf(tmp_path):
    long_name = "a" * 250 + ".pdf"
    file_path = tmp_path / long_name
    file_path.write_bytes(b"%PDF-1.4\n%%EOF")
    output = tmp_path / "output.pdf"
    merge_pdfs([str(file_path)], str(output))
    assert output.exists()
    assert output.stat().st_size > 0

def test_corrupted_pdf_skipped(tmp_path, caplog):
    valid = tmp_path / "valid.pdf"
    corrupted = tmp_path / "corrupted.pdf"
    valid.write_bytes(b"%PDF-1.4\n%%EOF")
    corrupted.write_text("not a pdf")
    output = tmp_path / "merged.pdf"
    with caplog.at_level(logging.WARNING):
        merge_pdfs([str(valid), str(corrupted)], str(output))
        assert output.exists()
        assert "Skipping" in caplog.text