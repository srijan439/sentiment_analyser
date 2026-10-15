from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_files_exist():
    assert (ROOT / "app" / "app.py").is_file()
    assert (ROOT / "requirements.txt").is_file()


def test_requirements_not_empty():
    assert (ROOT / "requirements.txt").read_text(encoding="utf-8").strip()


def test_monitoring_stack_is_configured():
    assert (ROOT / "docker-compose.yml").is_file()
    assert (ROOT / "monitoring" / "prometheus.yml").is_file()
