import os
import shutil
import tempfile
import unittest

from main import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_redoc_html_generation(self):
        source = "example/openapi.json"
        save_to = self.temp_dir
        save_type = "redoc"
        auto_latest = False

        main(source, save_to, save_type, auto_latest)

        expected_file_path = os.path.join(save_to, "test_api_100.html")
        self.assertTrue(os.path.exists(expected_file_path))

        with open(expected_file_path, "r") as f:
            contents = f.read()
            self.assertIn("Test API", contents)
            self.assertIn("1.0.0", contents)

    def test_swagger_html_generation(self):
        source = "example/openapi.json"
        save_to = self.temp_dir
        save_type = "swagger"
        auto_latest = False

        main(source, save_to, save_type, auto_latest)

        expected_file_path = os.path.join(save_to, "test_api_100.html")
        self.assertTrue(os.path.exists(expected_file_path))

        with open(expected_file_path, "r") as f:
            contents = f.read()
            self.assertIn("Test API", contents)
            self.assertIn("1.0.0", contents)

    def test_auto_latest_generation(self):
        source = "example/openapi.json"
        save_to = self.temp_dir
        save_type = "redoc"
        auto_latest = True

        main(source, save_to, save_type, auto_latest)

        expected_latest_file_path = os.path.join(save_to, "test_api_latest.html")
        self.assertTrue(os.path.exists(expected_latest_file_path))

        with open(expected_latest_file_path, "r") as f:
            contents = f.read()
            self.assertIn("Test API", contents)

        expected_versioned_file_path = os.path.join(save_to, "test_api_100.html")
        self.assertTrue(os.path.exists(expected_versioned_file_path))

        with open(expected_versioned_file_path, "r") as f:
            contents = f.read()
            self.assertIn("Test API", contents)
            self.assertIn("1.0.0", contents)


if __name__ == "__main__":
    unittest.main()
