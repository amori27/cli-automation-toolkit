from pathlib import Path
from src.processors.cleaner import deduplicate, fillna, filter_rows


class TestDeduplicate:
    def test_removes_duplicate_rows(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,2\n1,2\n3,4\n")
        out = tmp_path / "out.csv"
        deduplicate(str(f), str(out))
        lines = out.read_text().strip().split('\n')
        assert len(lines) == 3
        assert lines[1] == "1,2"
        assert lines[2] == "3,4"

    def test_no_duplicates(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,2\n3,4\n")
        out = tmp_path / "out.csv"
        deduplicate(str(f), str(out))
        lines = out.read_text().strip().split('\n')
        assert len(lines) == 3

    def test_all_duplicates(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a\n1\n1\n1\n")
        out = tmp_path / "out.csv"
        deduplicate(str(f), str(out))
        lines = out.read_text().strip().split('\n')
        assert len(lines) == 2


class TestFillNa:
    def test_fillna_mean(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a\n1\nNA\n3\n")
        out = tmp_path / "out.csv"
        fillna(str(f), "mean", "a", str(out))
        content = out.read_text()
        assert "2.0" in content

    def test_fillna_median(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a\n1\nNA\n10\n")
        out = tmp_path / "out.csv"
        fillna(str(f), "median", "a", str(out))
        content = out.read_text()
        assert "5.5" in content

    def test_fillna_mode(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a\nx\nNA\ny\nx\n")
        out = tmp_path / "out.csv"
        fillna(str(f), "mode", "a", str(out))
        content = out.read_text()
        assert "x" in content.split('\n')[2].split(',')[0]

    def test_fillna_all_numeric_columns(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,\n,4\n")
        out = tmp_path / "out.csv"
        fillna(str(f), "mean", None, str(out))
        content = out.read_text()
        assert "1.0" in content
        assert "4.0" in content

    def test_fillna_handles_all_missing(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a\n\n\n")
        out = tmp_path / "out.csv"
        fillna(str(f), "mean", "a", str(out))
        assert out.exists()


class TestFilterRows:
    def test_filter_by_string_value(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,x\n2,y\n3,x\n")
        out = tmp_path / "out.csv"
        filter_rows(str(f), "b", "x", str(out))
        lines = out.read_text().strip().split('\n')
        assert len(lines) == 3
        assert "y" not in out.read_text()

    def test_filter_no_matches(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,x\n2,y\n")
        out = tmp_path / "out.csv"
        filter_rows(str(f), "b", "z", str(out))
        content = out.read_text().strip()
        assert content == "a,b"

    def test_filter_numeric_value(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,10\n2,20\n3,10\n")
        out = tmp_path / "out.csv"
        filter_rows(str(f), "b", "10", str(out))
        lines = out.read_text().strip().split('\n')
        assert len(lines) == 3
