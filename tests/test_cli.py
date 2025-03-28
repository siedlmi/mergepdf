import subprocess
from pathlib import Path

def test_mergepdf_cli_dry_run(tmp_path):
    # Setup: Create dummy PDF files
    f1 = tmp_path / "doc1.pdf"
    f2 = tmp_path / "doc2.pdf"
    f1.write_bytes(b"%PDF-1.4\n%%EOF")
    f2.write_bytes(b"%PDF-1.4\n%%EOF")

    # Run CLI tool with --dry-run
    result = subprocess.run(
        ["mergepdf", str(tmp_path), "--dry-run"],
        capture_output=True,
        text=True
    )

    # Assertions
    assert result.returncode == 0
    assert "dry run" in result.stderr.lower()
    assert "merged.pdf" in result.stderr.lower() or "output.pdf" in result.stderr.lower()
