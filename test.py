import os
import shutil
import tempfile
import unittest
from unittest.mock import call, patch

import lipomerge


class TestLipomerge(unittest.TestCase):
    def setUp(self):
        self.primary_dir = tempfile.mkdtemp()
        self.secondary_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mktemp()

        self.setup_test_files()

    def tearDown(self):
        shutil.rmtree(self.primary_dir, ignore_errors=True)
        shutil.rmtree(self.secondary_dir, ignore_errors=True)
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir, ignore_errors=True)

    def setup_test_files(self):
        os.makedirs(os.path.join(self.primary_dir, "lib"))
        with open(os.path.join(self.primary_dir, "lib", "libtest.a"), "wb") as f:
            f.write(b"primary arch library")

        with open(os.path.join(self.primary_dir, "regular.txt"), "w") as f:
            f.write("regular text file")

        os.makedirs(os.path.join(self.secondary_dir, "lib"))
        with open(os.path.join(self.secondary_dir, "lib", "libtest.a"), "wb") as f:
            f.write(b"secondary arch library")

    @patch("lipomerge.subprocess.run")
    def test_merge_libraries(self, mock_run):
        """Test that libraries are properly merged using lipo"""

        def is_macho_side_effect(filepath):
            return filepath.endswith(".a") or "binary" in filepath

        with patch("lipomerge.is_macho", side_effect=is_macho_side_effect):
            with patch(
                "sys.argv",
                ["lipomerge.py", self.primary_dir, self.secondary_dir, self.output_dir],
            ):
                lipomerge.main()

        mock_run.assert_called_with(
            [
                "lipo",
                "-create",
                os.path.join(self.primary_dir, "lib", "libtest.a"),
                os.path.join(self.secondary_dir, "lib", "libtest.a"),
                "-output",
                os.path.join(self.output_dir, "lib", "libtest.a"),
            ]
        )

        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "regular.txt")))
        with open(os.path.join(self.output_dir, "regular.txt"), "r") as f:
            content = f.read()
        self.assertEqual(content, "regular text file")

    @patch("lipomerge.subprocess.run")
    def test_handle_missing_secondary_file(self, mock_run):
        """Test behavior when a file exists in primary but not in secondary dir"""
        os.remove(os.path.join(self.secondary_dir, "lib", "libtest.a"))

        def is_macho_side_effect(filepath):
            return filepath.endswith(".a") or "binary" in filepath

        with patch("lipomerge.is_macho", side_effect=is_macho_side_effect):
            with patch("builtins.print") as mock_print:
                with patch(
                    "sys.argv",
                    [
                        "lipomerge.py",
                        self.primary_dir,
                        self.secondary_dir,
                        self.output_dir,
                    ],
                ):
                    lipomerge.main()

            expected_message = f"Lib not found in secondary source: {os.path.join(self.secondary_dir, 'lib', 'libtest.a')}"
            mock_print.assert_any_call(expected_message)

        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "regular.txt")))
        self.assertFalse(
            mock_run.called, "lipo should not be called when secondary file is missing"
        )

    def test_macho_binary_detection(self):
        """Test that Mach-O binaries are correctly detected and merged"""
        with open(os.path.join(self.primary_dir, "binary"), "wb") as f:
            f.write(b"fake binary")
        with open(os.path.join(self.secondary_dir, "binary"), "wb") as f:
            f.write(b"fake secondary binary")

        def is_macho_side_effect(filepath):
            return filepath.endswith(".a") or "binary" in filepath

        expected_calls = [
            call(
                [
                    "lipo",
                    "-create",
                    os.path.join(self.primary_dir, "lib", "libtest.a"),
                    os.path.join(self.secondary_dir, "lib", "libtest.a"),
                    "-output",
                    os.path.join(self.output_dir, "lib", "libtest.a"),
                ]
            ),
            call(
                [
                    "lipo",
                    "-create",
                    os.path.join(self.primary_dir, "binary"),
                    os.path.join(self.secondary_dir, "binary"),
                    "-output",
                    os.path.join(self.output_dir, "binary"),
                ]
            ),
        ]

        with patch("lipomerge.is_macho", side_effect=is_macho_side_effect):
            with patch("lipomerge.subprocess.run") as mock_run:
                with patch(
                    "sys.argv",
                    [
                        "lipomerge.py",
                        self.primary_dir,
                        self.secondary_dir,
                        self.output_dir,
                    ],
                ):
                    lipomerge.main()

                self.assertEqual(
                    len(mock_run.call_args_list),
                    2,
                    "lipo should be called exactly twice",
                )
                for expected_call in expected_calls:
                    self.assertIn(expected_call, mock_run.call_args_list)


if __name__ == "__main__":
    unittest.main()
