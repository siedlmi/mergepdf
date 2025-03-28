import os
import pytest
from mergepdf.cli import read_order_file, parse_args

def test_read_order_file_valid(tmp_path):
    order_file = tmp_path / "order.txt"
    order_file.write_text("file1.pdf\nfile2.pdf\n")
    result = read_order_file(order_file)
    assert result == ["file1.pdf", "file2.pdf"]

def test_read_order_file_missing():
    result = read_order_file("non_existent.txt")
    assert result is None

def test_parse_args_defaults(monkeypatch):
    monkeypatch.setattr("sys.argv", ["mergepdf", "some/folder"])
    args = parse_args("0.0.0")
    assert args.folder == "some/folder"
    assert args.output == "merged.pdf"
    assert not args.recursive
    assert args.sort_by == "filename"
