import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from app import run

ROOT = Path(__file__).resolve().parent

class InputValidationTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))

    def test_root_must_be_object(self):
        for value in (None, [], "texto", 3, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                run(value)

    def test_valid_input_is_not_mutated(self):
        original = copy.deepcopy(self.data)
        run(self.data)
        self.assertEqual(self.data, original)

    def test_rejeita_urls_que_o_parser_aceita_parcialmente(self):
        for url in ("https://@example.com/obra", "https://example.com:65536/obra",
                    "https://example.com/linha\nseguinte", "https://example.com/nome da obra"):
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "HTTPS pública"):
                data = copy.deepcopy(self.data)
                data["obras"][0]["url"] = url
                run(data)

    def test_link_codificado_continua_aceito(self):
        link = "https://example.com:443/nome%20da%20obra"
        self.data["obras"][0]["url"] = link
        self.assertIn(link, [obra["url"] for obra in run(self.data)["obras"]])

    def test_invalid_json_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.json"
            path.write_text('{"incompleto":', encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "app.py"), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_file_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(ROOT / "app.py"), str(Path(tmp) / "missing.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_collection_requires_objects(self):
        for value in ({}, None, "", 42, [None], ["texto"], [[]], [True]):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data['obras'] = value
                with self.assertRaises(ValueError):
                    run(data)

    def test_invalid_collection_cli(self):
        self.data['obras'] = {}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.json"
            path.write_text(json.dumps(self.data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "app.py"), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)
