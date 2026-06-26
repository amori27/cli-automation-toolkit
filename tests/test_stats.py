import json
from pathlib import Path
from src.reporters.stats import generate_stats


class TestGenerateStats:
    def test_basic_statistics(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,2\n3,4\n5,6\n")
        out = tmp_path / "stats.json"
        generate_stats(str(f), str(out))
        data = json.loads(out.read_text())
        assert data['rows'] == 3
        assert data['columns'] == 2
        assert 'column_stats' in data
        assert 'memory_usage' in data

    def test_numeric_column_stats(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("val\n1\n2\n3\n4\n5\n")
        out = tmp_path / "stats.json"
        generate_stats(str(f), str(out))
        data = json.loads(out.read_text())
        col = data['column_stats']['val']
        assert col['mean'] == 3.0
        assert col['min'] == 1.0
        assert col['max'] == 5.0
        assert col['count'] == 5
        assert col['nulls'] == 0

    def test_mixed_column_types(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("name,age,salary\nAlice,30,50000\nBob,25,60000\n")
        out = tmp_path / "stats.json"
        generate_stats(str(f), str(out))
        data = json.loads(out.read_text())
        assert 'age' in data['column_stats']
        assert 'name' in data['column_stats']
        assert data['column_stats']['name']['dtype'] == 'object'
        assert 'mean' not in data['column_stats']['name']

    def test_missing_values(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n1,2\n,3\n,4\n")
        out = tmp_path / "stats.json"
        generate_stats(str(f), str(out))
        data = json.loads(out.read_text())
        assert data['column_stats']['a']['nulls'] == 2
        assert data['column_stats']['a']['null_pct'] > 0

    def test_empty_dataframe(self, tmp_path: Path) -> None:
        f = tmp_path / "in.csv"
        f.write_text("a,b\n")
        out = tmp_path / "stats.json"
        generate_stats(str(f), str(out))
        data = json.loads(out.read_text())
        assert data['rows'] == 0
