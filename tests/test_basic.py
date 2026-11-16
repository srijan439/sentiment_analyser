from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_files_exist():
    # Backend files
    assert (ROOT / "app" / "__init__.py").is_file()
    assert (ROOT / "app" / "app.py").is_file()
    assert (ROOT / "app" / "main.py").is_file()
    assert (ROOT / "requirements.txt").is_file()

    # ML files
    assert (ROOT / "model").is_dir()
    assert (ROOT / "train.py").is_file()

    # Frontend files
    assert (ROOT / "app" / "static" / "index.html").is_file()
    assert (ROOT / "app" / "static" / "css" / "style.css").is_file()
    assert (ROOT / "app" / "static" / "js" / "app.js").is_file()


def test_requirements_not_empty():
    assert (ROOT / "requirements.txt").read_text(encoding="utf-8").strip()


def test_test_samples_contain_mixed_and_sarcasm():
    samples_text = (ROOT / "test_samples.txt").read_text(encoding="utf-8")
    assert "visual craftsmanship" in samples_text
    assert "narrative that feels hollow" in samples_text
    assert "Oh what an absolute revelation" in samples_text
    assert "paper-thin CGI villains" in samples_text


def test_sarcasm_and_mixed_logic_present_in_backend():
    main_code = (ROOT / "app" / "main.py").read_text(encoding="utf-8")
    assert "detect_sarcasm_and_irony" in main_code
    assert "extract_aspect_themes" in main_code
    assert "SARCASM_DISCOURSE_PATTERNS" in main_code
    assert "split_into_clauses_and_sentences" in main_code
