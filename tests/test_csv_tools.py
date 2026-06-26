import json
from pathlib import Path
from src.processors.csv_tools import merge_csvs, convert_file


class TestMergeCSVs:
    def test_merge_two_files(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.csv"
        f2 = tmp_path / "b.csv"
        f1.write_text("col\n1\n2\n3\n")
        f2.write_text("col\n4\n5\n6\n")
        out = tmp_path / "merged.csv"
        result = merge_csvs([str(f1), str(f2)], str(out))
        lines = out.read_text().strip().split('\n')
        assert len(lines) == 7
        assert lines[0] == 'col'
        assert lines[1] == '1'
        assert lines[6] == '6'
        assert result == str(out)

    def test_merge_three_files(self, tmp_path: Path) -> None:
        files = []
        for i in range(3):
            f = tmp_path / f"{i}.csv"
            f.write_text(f"val\n{i+1}\n")
            files.append(str(f))
        out = tmp_path / "merged.csv"
        merge_csvs(files, str(out))
        lines = out.read_text().strip().split('\n')
        assert len(lines) == 4

    def test_merge_with_different_columns(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.csv"
        f2 = tmp_path / "b.csv"
        f1.write_text("a,b\n1,2\n")
        f2.write_text("a,c\n3,4\n")
        out = tmp_path / "merged.csv"
        merge_csvs([str(f1), str(f2)], str(out))
        df = __import__('pandas').read_csv(str(out))
        assert list(df.columns) == ['a', 'b', 'c']


class TestConvert:
    def test_csv_to_json(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("a,b\n1,2\n3,4\n")
        out = tmp_path / "out.json"
        convert_file(str(csv_file), "json", str(out))
        data = json.loads(out.read_text())
        assert len(data) == 2
        assert data[0] == {"a": 1, "b": 2}
        assert data[1] == {"a": 3, "b": 4}

    def test_json_to_csv(self, tmp_path: Path) -> None:
        json_file = tmp_path / "test.json"
        json_file.write_text('[{"a":1,"b":2},{"a":3,"b":4}]')
        out = tmp_path / "out.csv"
        convert_file(str(json_file), "csv", str(out))
        content = out.read_text().strip()
        assert "a,b" in content
        assert "1,2" in content
        assert "3,4" in content

    def test_csv_to_json_default_output(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("x\n1\n2\n")
        result = convert_file(str(csv_file), "json")
        assert result.endswith("data.json")

    def test_json_to_csv_default_output(self, tmp_path: Path) -> None:
        json_file = tmp_path / "data.json"
        json_file.write_text('[{"x":1}]')
        result = convert_file(str(json_file), "csv")
        assert result.endswith("data.csv")
