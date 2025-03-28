import os
import time
from mergepdf.cli import sort_pdfs
from PyPDF2 import PdfWriter

def test_sort_by_filename(tmp_path):
    file1 = tmp_path / "a.pdf"
    file2 = tmp_path / "b.pdf"
    file1.write_text("PDF A")
    file2.write_text("PDF B")
    sorted_files = sort_pdfs([str(file2), str(file1)], "filename")
    assert sorted_files == [str(file1), str(file2)]

def test_sort_by_custom_order(tmp_path):
    file1 = tmp_path / "x.pdf"
    file2 = tmp_path / "y.pdf"
    file1.write_text("X")
    file2.write_text("Y")
    files = [str(file1), str(file2)]
    order = ["y.pdf", "x.pdf"]
    sorted_files = sort_pdfs(files, "custom", custom_order=order)
    assert [os.path.basename(f) for f in sorted_files] == order

def test_dry_run_output(tmp_path, caplog):
    from mergepdf.cli import merge_pdfs

    file1 = tmp_path / "doc1.pdf"
    file2 = tmp_path / "doc2.pdf"
    file1.write_bytes(b"%PDF-1.4\n%%EOF")
    file2.write_bytes(b"%PDF-1.4\n%%EOF")

    with caplog.at_level("INFO"):
        merge_pdfs([str(file1), str(file2)], "output.pdf", dry_run=True)
        assert "Dry Run" in caplog.text
        assert "output.pdf" in caplog.text

def test_sort_by_filesize(tmp_path):
    small = tmp_path / "small.pdf"
    large = tmp_path / "large.pdf"
    small.write_bytes(b"A" * 10)
    large.write_bytes(b"A" * 100)
    sorted_files = sort_pdfs([str(large), str(small)], "filesize")
    assert sorted_files == [str(small), str(large)]

def test_sort_by_modified(tmp_path):
    old = tmp_path / "old.pdf"
    new = tmp_path / "new.pdf"
    old.write_text("Old")
    new.write_text("New")
    old_time = time.time() - 1000
    os.utime(old, (old_time, old_time))
    sorted_files = sort_pdfs([str(new), str(old)], "modified")
    assert sorted_files == [str(old), str(new)]

def test_sort_by_pagenumber(tmp_path):
    f1 = tmp_path / "one_page.pdf"
    f2 = tmp_path / "two_pages.pdf"

    writer1 = PdfWriter()
    writer1.add_blank_page(width=595.2, height=841.8)
    with open(f1, "wb") as f:
        writer1.write(f)

    writer2 = PdfWriter()
    writer2.add_blank_page(width=595.2, height=841.8)
    writer2.add_blank_page(width=595.2, height=841.8)
    with open(f2, "wb") as f:
        writer2.write(f)

    sorted_files = sort_pdfs([str(f2), str(f1)], "pagenumber")
    assert sorted_files == [str(f1), str(f2)]

def test_sort_reverse_by_filename(tmp_path):
    f1 = tmp_path / "A.pdf"
    f2 = tmp_path / "B.pdf"
    f1.write_text("File A")
    f2.write_text("File B")
    pdfs = [str(f1), str(f2)]
    sorted_files = sort_pdfs(pdfs, sort_by="filename", reverse=True)
    assert sorted_files == [str(f2), str(f1)]

def test_sort_reverse_custom_ignored(tmp_path):
    f1 = tmp_path / "file1.pdf"
    f2 = tmp_path / "file2.pdf"
    f1.write_text("A")
    f2.write_text("B")
    pdfs = [str(f1), str(f2)]
    custom = ["file1.pdf", "file2.pdf"]
    result = sort_pdfs(pdfs, sort_by="custom", custom_order=custom, reverse=True)
    assert result == [str(f1), str(f2)]  # no effect expected

def test_sort_reverse_by_modified(tmp_path):
    file1 = tmp_path / "file1.pdf"
    file2 = tmp_path / "file2.pdf"
    file1.write_text("Older file")
    file2.write_text("Newer file")
    old_time = time.time() - 1000
    os.utime(file1, (old_time, old_time))
    sorted_files = sort_pdfs([str(file1), str(file2)], sort_by="modified", reverse=True)
    assert sorted_files == [str(file2), str(file1)]

def test_sort_reverse_by_pagenumber(tmp_path):
    file1 = tmp_path / "short.pdf"
    file2 = tmp_path / "long.pdf"

    writer1 = PdfWriter()
    writer1.add_blank_page(width=595.2, height=841.8)
    with open(file1, "wb") as f:
        writer1.write(f)

    writer2 = PdfWriter()
    writer2.add_blank_page(width=595.2, height=841.8)
    writer2.add_blank_page(width=595.2, height=841.8)
    with open(file2, "wb") as f:
        writer2.write(f)

    sorted_files = sort_pdfs([str(file1), str(file2)], sort_by="pagenumber", reverse=True)
    assert sorted_files == [str(file2), str(file1)]