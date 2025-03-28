import getpass
import builtins
from pathlib import Path
from PyPDF2 import PdfWriter
from mergepdf.cli import merge_pdfs

def create_encrypted_pdf(path: Path, password: str):
    writer = PdfWriter()
    writer.add_blank_page(width=595.2, height=841.8)
    writer.encrypt(password)
    with open(path, "wb") as f:
        writer.write(f)

def test_merge_with_correct_password(tmp_path, monkeypatch):
    encrypted = tmp_path / "secret.pdf"
    create_encrypted_pdf(encrypted, password="1234")
    output = tmp_path / "merged.pdf"

    # Simulate password input
    monkeypatch.setattr(getpass, "getpass", lambda prompt: "1234")

    merge_pdfs([str(encrypted)], str(output))
    assert output.exists()
    assert output.stat().st_size > 0

def test_merge_with_wrong_password(tmp_path, monkeypatch, caplog):
    encrypted = tmp_path / "secret.pdf"
    create_encrypted_pdf(encrypted, password="1234")
    output = tmp_path / "merged.pdf"

    # Simulate wrong password
    monkeypatch.setattr(getpass, "getpass", lambda prompt: "wrong")

    with caplog.at_level("WARNING"):
        merge_pdfs([str(encrypted)], str(output))
        # Instead of expecting size 0, we expect a minimal PDF file (e.g. less than 400 bytes)
        assert output.exists()
        assert output.stat().st_size < 400  
        assert "file has not been decrypted" in caplog.text.lower()